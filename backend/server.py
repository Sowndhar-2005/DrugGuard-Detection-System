"""
server.py
DrugGuard API Server — Rebuilt from Scratch

Provides:
  - Text classification via fine-tuned DistilBERT (ONNX) with fallback to TF-IDF + LogisticRegression
  - Visual content classification via MobileNetV2 (ONNX)
  - Text-in-image extraction using RapidOCR (ONNX)
  - Multimodal fusion to compute composite risk scores
"""

import os
import io
import json
import base64
import numpy as np
import pickle
from typing import Optional
from PIL import Image
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rapidocr_onnxruntime import RapidOCR

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(
    title="DrugGuard ML Server",
    description="Multimodal detection of drug trafficking content",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ─── Model Paths ───
TRAIN_DIR = os.path.join(BASE_DIR, "train")
ROOT_TRAIN_DIR = os.path.join(BASE_DIR, "..", "train")

def get_path(filename, default_filename):
    train_path = os.path.join(TRAIN_DIR, filename)
    if os.path.exists(train_path):
        return train_path
    root_path = os.path.join(ROOT_TRAIN_DIR, filename)
    if os.path.exists(root_path):
        return root_path
    return os.path.join(BASE_DIR, default_filename)

TEXT_ONNX_PATH = get_path("text_model.onnx", "text_model.onnx")
TEXT_PKL_PATH = get_path("text_model.pkl", "text_model.pkl")
VECTORIZER_PATH = get_path("vectorizer.pkl", "vectorizer.pkl")
IMAGE_ONNX_PATH = get_path("image_model.onnx", "image_model.onnx")
IMAGE_CLASSES_PATH = get_path("image_classes.json", "image_classes.json")
DISTILBERT_DIR = os.path.join(BASE_DIR, "text_model_distilbert")

# Global Sessions & Models
text_onnx_session = None
text_tokenizer = None
text_fallback_model = None
text_fallback_vectorizer = None
text_model_status = "Not Loaded"

image_onnx_session = None
image_classes = None
image_model_status = "Not Loaded"

ocr_engine = None

# ─── Model Initializations ───

def init_text_model():
    global text_onnx_session, text_tokenizer, text_fallback_model, text_fallback_vectorizer, text_model_status
    
    # 1. DistilBERT ONNX
    if os.path.exists(TEXT_ONNX_PATH):
        try:
            import onnxruntime as ort
            from transformers import DistilBertTokenizerFast
            text_onnx_session = ort.InferenceSession(TEXT_ONNX_PATH)
            
            # Load tokenizer
            if os.path.exists(DISTILBERT_DIR):
                text_tokenizer = DistilBertTokenizerFast.from_pretrained(DISTILBERT_DIR)
            else:
                text_tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
                
            text_model_status = "DistilBERT (ONNX)"
            print(f"✅ Text model initialized: {text_model_status}")
            return
        except Exception as e:
            print(f"⚠️ Failed to load ONNX text model: {e}")

    # 2. Fallback Pickle model
    if os.path.exists(TEXT_PKL_PATH) and os.path.exists(VECTORIZER_PATH):
        try:
            with open(TEXT_PKL_PATH, "rb") as f:
                text_fallback_model = pickle.load(f)
            with open(VECTORIZER_PATH, "rb") as f:
                text_fallback_vectorizer = pickle.load(f)
            text_model_status = "TF-IDF + LR (Fallback)"
            print(f"✅ Text model initialized: {text_model_status}")
            return
        except Exception as e:
            print(f"⚠️ Failed to load fallback text model: {e}")

    text_model_status = "No Text Model Loaded (Inference Unusable)"
    print("❌ No text models available.")

def init_image_model():
    global image_onnx_session, image_classes, image_model_status
    if os.path.exists(IMAGE_ONNX_PATH):
        try:
            import onnxruntime as ort
            image_onnx_session = ort.InferenceSession(IMAGE_ONNX_PATH)
            
            if os.path.exists(IMAGE_CLASSES_PATH):
                with open(IMAGE_CLASSES_PATH, "r") as f:
                    image_classes = json.load(f)
            else:
                image_classes = {"classes": ["drug", "safe"], "class_to_idx": {"drug": 0, "safe": 1}}
                
            image_model_status = "MobileNetV2 (ONNX)"
            print(f"✅ Image model initialized: {image_model_status}")
            return
        except Exception as e:
            print(f"⚠️ Failed to load ONNX image model: {e}")

    image_model_status = "No Image Model Loaded (OCR Fallback Only)"
    print("⚠️ No image model available. OCR fallback will be utilized.")

def init_ocr():
    global ocr_engine
    try:
        ocr_engine = RapidOCR()
        print("✅ RapidOCR engine initialized")
    except Exception as e:
        print(f"⚠️ Failed to load OCR engine: {e}")

# Load models on server bootup
print("="*60)
print("Initializing DrugGuard Inference Pipeline...")
print("="*60)
init_text_model()
init_image_model()
init_ocr()
print("="*60)

# ─── Algospeak Normalization mappings ───
EMOJI_MAP = {
    "🍃": " marijuana ", "🌿": " marijuana ", "❄️": " cocaine ",
    "💊": " pills ", "🔌": " plug ", "🍄": " mushrooms ",
    "💉": " heroin ", "📦": " package ", "💰": " cash ",
    "🔥": " fire ", "⚡": " fast ", "🧊": " ice ",
    "🌬️": " smoke ", "🎱": " eightball ", "🏔️": " mountain ",
    "🍬": " candy ", "🧪": " lab ", "🔬": " tested ", "💯": " hundred ",
}

LEETSPEAK_MAP = {
    "dr*gs": "drugs", "dr*g": "drug",
    "d r u g s": "drugs", "d r u g": "drug",
    "x*nax": "xanax", "x@nax": "xanax", "x@n@x": "xanax",
    "c*caine": "cocaine", "c0ca1ne": "cocaine",
    "h*roin": "heroin", "h.e.r.o.i.n": "heroin",
    "f*ntanyl": "fentanyl", "f3nt@nyl": "fentanyl",
    "m3th": "meth", "p1lls": "pills", "p3rc0c3t": "percocet",
    "w33d": "weed", "mar1juana": "marijuana",
    "k3tam1ne": "ketamine", "c@nnab!s": "cannabis",
    "g@nja": "ganja", "0xy": "oxy",
}

def normalize_text(text: str) -> str:
    for emoji, replacement in EMOJI_MAP.items():
        text = text.replace(emoji, replacement)
    for pattern, replacement in LEETSPEAK_MAP.items():
        text = text.replace(pattern, replacement)
    return text.strip()

# ─── Inference Workers ───

def run_text_inference(text: str) -> tuple[int, float]:
    """Runs prediction on text returning (label, risk_score)"""
    norm = normalize_text(text).lower()
    
    if text_onnx_session is not None:
        inputs = text_tokenizer(
            norm, return_tensors="np", padding="max_length", truncation=True, max_length=128
        )
        ort_inputs = {
            "input_ids": inputs["input_ids"].astype(np.int64),
            "attention_mask": inputs["attention_mask"].astype(np.int64)
        }
        logits = text_onnx_session.run(None, ort_inputs)[0]
        # Softmax computation
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / exp_logits.sum(axis=-1, keepdims=True)
        label = int(np.argmax(probs[0]))
        risk_score = float(probs[0][1]) # Class 1 = drug
        return label, risk_score
        
    if text_fallback_model is not None:
        vec = text_fallback_vectorizer.transform([norm])
        label = int(text_fallback_model.predict(vec)[0])
        probs = text_fallback_model.predict_proba(vec)[0]
        risk_score = float(probs[1])
        return label, risk_score
        
    return 0, 0.0

def run_image_inference(image: Image.Image) -> tuple[int, float]:
    """Runs MobileNetV2 ONNX visual classification returning (label, risk_score)"""
    if image_onnx_session is None:
        return 0, 0.0
        
    img = image.resize((224, 224)).convert("RGB")
    arr = np.array(img, dtype=np.float32) / 255.0
    
    # ImageNet stats normalization
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    arr = (arr - mean) / std
    
    # Transform shape to channel-first (1, 3, 224, 224)
    arr = np.transpose(arr, (2, 0, 1))
    arr = np.expand_dims(arr, axis=0).astype(np.float32)
    
    input_name = image_onnx_session.get_inputs()[0].name
    logits = image_onnx_session.run(None, {input_name: arr})[0]
    
    exp_logits = np.exp(logits - np.max(logits))
    probs = exp_logits / exp_logits.sum(axis=-1, keepdims=True)
    
    classes = image_classes.get("classes", ["drug", "safe"])
    drug_idx = classes.index("drug") if "drug" in classes else 0
    
    risk_score = float(probs[0][drug_idx])
    label = 1 if risk_score >= 0.30 else 0
    return label, risk_score

def get_triggered_words(text: str) -> list[str]:
    """Identifies highly indicative words in the phrase"""
    norm = normalize_text(text).lower()
    words = norm.split()
    
    # Simple lexicon scan for response details
    keywords = ["pill", "drugs", "weed", "cocaine", "heroin", "fentanyl", "xanax", "plug", "cash", "marijuana"]
    found = [w for w in words if w in keywords]
    return list(set(found))

def score_to_action(score: float) -> str:
    if score < 0.15:
        return "safe"
    elif score < 0.35:
        return "warn"
    else:
        return "block"


# ─── Pydantic Schemas ───

class TextRequest(BaseModel):
    text: str
    url: Optional[str] = None

class ImageRequest(BaseModel):
    image: str
    url: Optional[str] = None

class PredictResponse(BaseModel):
    action: str
    risk_score: float
    confidence: float
    label: int
    triggered_words: list[str]
    website_url: Optional[str] = None

# ─── API Routes ───

@app.get("/health")
def health():
    return {
        "status": "ok",
        "text_model": text_model_status,
        "image_model": image_model_status,
        "ocr_engine": "RapidOCR" if ocr_engine is not None else "Not Available"
    }

@app.post("/predict", response_model=PredictResponse)
def predict_text(request: TextRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Empty text input")
        
    site_info = f" [URL: {request.url}]" if request.url else ""
    print(f"🔍 [Backend] Text scan request{site_info}: {request.text[:60]}...")

    label, score = run_text_inference(request.text)
    action = score_to_action(score)
    triggered = get_triggered_words(request.text) if label == 1 else []
    
    return PredictResponse(
        action=action,
        risk_score=round(score, 4),
        confidence=round(score * 100, 2),
        label=label,
        triggered_words=triggered,
        website_url=request.url
    )

@app.post("/predict_image", response_model=PredictResponse)
def predict_image(request: ImageRequest):
    img_data = request.image.strip()
    if not img_data:
        raise HTTPException(status_code=400, detail="Empty image data")
        
    site_info = f" [URL: {request.url}]" if request.url else ""
    print(f"📷 [Backend] Image photo scan request{site_info}")

        
    if "," in img_data:
        img_data = img_data.split(",", 1)[1]
        
    try:
        img_bytes = base64.b64decode(img_data)
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {e}")

    # 1. Image Classification (MobileNetV2)
    visual_label = 0
    visual_score = 0.0
    if image_onnx_session is not None:
        try:
            visual_label, visual_score = run_image_inference(image)
            print(f"   ↳ Visual MobileNetV2 score: {visual_score:.4f} (label: {visual_label})")
        except Exception as e:
            print(f"Image inference error: {e}")

    # 2. Text extraction via OCR + Text inference
    ocr_score = 0.0
    triggered = []
    if ocr_engine is not None:
        try:
            res, _ = ocr_engine(np.array(image))
            if res:
                extracted_text = " ".join([line[1] for line in res if line[1]]).strip()
                if extracted_text:
                    _, ocr_score = run_text_inference(extracted_text)
                    triggered = get_triggered_words(extracted_text)
                    print(f"   ↳ OCR Extracted Text score: {ocr_score:.4f}")
        except Exception as e:
            print(f"OCR inference error: {e}")

    # 3. Multimodal Fusion (Preserves high visual detection score when OCR is empty)
    if image_onnx_session is not None:
        if ocr_score > 0.0:
            final_score = max(visual_score, (0.6 * visual_score) + (0.4 * ocr_score))
        else:
            final_score = visual_score
    else:
        final_score = ocr_score

    final_label = 1 if (final_score >= 0.30 or visual_label == 1) else 0
    
    if final_score >= 0.30 or visual_label == 1:
        action = "block"
    elif final_score >= 0.20:
        action = "warn"
    else:
        action = "safe"

    
    return PredictResponse(
        action=action,
        risk_score=round(final_score, 4),
        confidence=round(final_score * 100, 2),
        label=final_label,
        triggered_words=triggered,
        website_url=request.url
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
