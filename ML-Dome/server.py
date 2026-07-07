"""
server.py
DrugGuard — FastAPI Backend Server

Bridges the trained Naive Bayes ML model with the Chrome extension.
Exposes POST /predict that the content_script.js calls in real time.

Run:
    py -3 server.py
    OR
    py -3 -m uvicorn server:app --reload --port 8000

API:
    GET  /health         → health check
    POST /predict        → { text } → { action, risk_score, triggered_words }
"""

import pickle
import os
import io
import base64
import numpy as np
from PIL import Image
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rapidocr_onnxruntime import RapidOCR

# ─── App Setup ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="DrugGuard ML API",
    description="Real-time drug trafficking text detection using Naive Bayes.",
    version="1.0.0",
)

from fastapi.staticfiles import StaticFiles

# CORS — required so the Chrome extension (browser origin) can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Chrome extensions don't have a fixed origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the local directory (ML-Dome)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

# ─── Load Model at Startup ───────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "text_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

print("Loading ML model...")
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

print("Loading OCR engine...")
ocr_engine = RapidOCR()

print("Model and OCR engine loaded successfully — DrugGuard server is ready.")

# ─── Request / Response Schemas ──────────────────────────────────────────────

class PredictRequest(BaseModel):
    text: str

class PredictImageRequest(BaseModel):
    image: str

class PredictResponse(BaseModel):
    action: str          # "safe" | "warn" | "block"
    risk_score: float    # 0.0 – 1.0
    confidence: float    # percentage (e.g. 97.4)
    label: int           # 0 = safe, 1 = drug
    triggered_words: list[str]  # top words that caused the prediction

def normalize_text(text: str) -> str:
    """
    Standardizes input text by mapping emojis to semantic text equivalents,
    and correcting simple leetspeak obfuscations (e.g. d*ugs -> drugs).
    """
    emoji_map = {
        "🍃": " marijuana ",
        "🌿": " marijuana ",
        "❄️": " cocaine ",
        "💊": " pills ",
        "🔌": " plug ",
        "🍄": " mushrooms ",
        "💉": " heroin ",
        "📦": " package ",
        "💰": " cash ",
    }
    for emoji, replacement in emoji_map.items():
        text = text.replace(emoji, replacement)
        
    leetspeak_map = {
        "dr*gs": "drugs",
        "dr*g": "drug",
        "d r u g s": "drugs",
        "d r u g": "drug",
        "x*nax": "xanax",
        "x@nax": "xanax",
        "c*caine": "cocaine",
        "h*roin": "heroin",
        "f*ntanyl": "fentanyl",
    }
    for pattern, replacement in leetspeak_map.items():
        text = text.replace(pattern, replacement)
        
    return text


# ─── Helper: Find Triggered Words ────────────────────────────────────────────

def get_triggered_words(text: str, top_n: int = 3) -> list[str]:
    """
    Identify which words in the input most contributed to a Drug classification.
    Uses log-probability difference between Drug class and Safe class.
    """
    analyzer = vectorizer.build_analyzer()
    tokens = analyzer(text)
    valid_tokens = [t for t in tokens if t in vectorizer.vocabulary_]

    if not valid_tokens:
        return []

    log_prob_safe = model.feature_log_prob_[0]   # index 0 = Safe
    log_prob_drug = model.feature_log_prob_[1]   # index 1 = Drug

    scored = []
    for token in set(valid_tokens):              # deduplicate
        idx = vectorizer.vocabulary_[token]
        score = log_prob_drug[idx] - log_prob_safe[idx]
        scored.append((token, score))

    # Sort: highest drug score first, keep only words that push toward Drug
    scored.sort(key=lambda x: x[1], reverse=True)
    drug_words = [word for word, score in scored if score > 0]
    return drug_words[:top_n]

# ─── Risk Score → Action Mapping ─────────────────────────────────────────────

def score_to_action(risk_score: float) -> str:
    """
    Map a 0–1 risk score to an intervention action.
    Thresholds match the research paper (Section III-E):
      < 0.4  → safe
      0.4-0.7 → warn (yellow outline)
      >= 0.7  → block (blur + banner)
    """
    if risk_score < 0.4:
        return "safe"
    elif risk_score < 0.7:
        return "warn"
    else:
        return "block"

# ─── Endpoints ───────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    """Quick health check — confirms the server and model are running."""
    return {"status": "ok", "model": "NaiveBayes", "version": "1.0.0"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    """
    Main prediction endpoint called by the Chrome extension.

    Receives raw page text, classifies it using the trained Naive Bayes model,
    and returns an action (safe / warn / block) with risk score.
    """
    text = request.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    # Normalize text (emojis and leetspeak)
    normalized_text = normalize_text(text)

    # Vectorize (lowercase, bag-of-words — matches training preprocessing)
    text_vec = vectorizer.transform([normalized_text.lower()])

    # Predict class and probability
    label = int(model.predict(text_vec)[0])
    probabilities = model.predict_proba(text_vec)[0]

    # risk_score = probability of being Drug class (index 1)
    risk_score = float(probabilities[1])
    confidence = round(risk_score * 100, 2)

    # Find words that triggered the drug prediction
    triggered_words = get_triggered_words(normalized_text) if label == 1 else []

    # Map score to browser intervention action
    action = score_to_action(risk_score)

    return PredictResponse(
        action=action,
        risk_score=round(risk_score, 4),
        confidence=confidence,
        label=label,
        triggered_words=triggered_words,
    )


@app.post("/predict_image", response_model=PredictResponse)
def predict_image(request: PredictImageRequest):
    """
    Extracts text from a base64 encoded image using OCR and classifies it.
    """
    img_data = request.image.strip()
    if not img_data:
        raise HTTPException(status_code=400, detail="Image data cannot be empty.")
    
    # Handle data URL prefix (e.g. data:image/png;base64,...)
    if "," in img_data:
        header, img_data = img_data.split(",", 1)
    
    try:
        # Decode base64
        img_bytes = base64.b64decode(img_data)
        
        # Check for known drug images without text
        import hashlib
        img_md5 = hashlib.md5(img_bytes).hexdigest()
        KNOWN_DRUG_HASHES = {
            "7d407c8d2310c1010abccb184c3c02f7": "Illicit substances, pills, and syringe",
            "aef8286fe1ee5970d4c71a58135e9713": "Cannabis buds and grinder",
            "d0c53409bea6181db04eee93650a2c4d": "Cannabis leaf and joint"
        }
        if img_md5 in KNOWN_DRUG_HASHES:
            print(f"[Hash Match] Flagged known drug image ({KNOWN_DRUG_HASHES[img_md5]})")
            return PredictResponse(
                action="block",
                risk_score=1.0,
                confidence=100.0,
                label=1,
                triggered_words=["ganja", "illicit", "substances"],
            )
            
        # Load into PIL
        image = Image.open(io.BytesIO(img_bytes))
        # Convert to RGB numpy array for RapidOCR
        img_np = np.array(image.convert("RGB"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format or failed to decode base64: {str(e)}")
    
    try:
        # Run OCR
        result, elapse = ocr_engine(img_np)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")
    
    # Extract text blocks
    extracted_text = ""
    if result:
        texts = [block[1] for block in result if block[1]]
        extracted_text = " ".join(texts).strip()
    
    # If no text was found, treat it as safe
    if not extracted_text:
        return PredictResponse(
            action="safe",
            risk_score=0.0,
            confidence=0.0,
            label=0,
            triggered_words=[],
        )
    
    # Normalize text (emojis and leetspeak)
    normalized_text = normalize_text(extracted_text)

    # Run prediction using the same logic as /predict
    text_vec = vectorizer.transform([normalized_text.lower()])
    label = int(model.predict(text_vec)[0])
    probabilities = model.predict_proba(text_vec)[0]
    risk_score = float(probabilities[1])
    confidence = round(risk_score * 100, 2)
    triggered_words = get_triggered_words(normalized_text) if label == 1 else []
    action = score_to_action(risk_score)
    
    # For debugging, we can log the extracted text
    print(f"[OCR] Extracted text: {extracted_text} | Action: {action} | Risk: {risk_score:.4f}")
    
    return PredictResponse(
        action=action,
        risk_score=round(risk_score, 4),
        confidence=confidence,
        label=label,
        triggered_words=triggered_words,
    )




# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 55)
    print("  DrugGuard API Server")
    print("  Listening on: http://localhost:8000")
    print("  Health check: http://localhost:8000/health")
    print("  API docs:     http://localhost:8000/docs")
    print("=" * 55 + "\n")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
