"""
train_text_model.py
DrugGuard — Local Text Model Trainer

Trains a TF-IDF Vectorizer + Logistic Regression classifier on dataset.csv
and exports it as a fallback pickle model.
"""

import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset.csv")

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
    return text

def main():
    if not os.path.exists(DATASET_PATH):
        print(f"❌ Dataset not found at: {DATASET_PATH}. Please run setup_dataset_v3.py first.")
        return

    print("Loading dataset...")
    df = pd.read_csv(DATASET_PATH)
    
    print("Normalizing corpus text...")
    df["normalized_text"] = df["text"].astype(str).apply(normalize_text).str.lower()
    
    X = df["normalized_text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print("Fitting TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Training Logistic Regression fallback model...")
    model = LogisticRegression(class_weight="balanced", C=1.0, max_iter=1000, random_state=42)
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print("\n" + "="*50)
    print(f"Fallback Model Trained Successfully:")
    print(f"Accuracy: {acc * 100:.2f}%")
    print(f"F1 Score: {f1 * 100:.2f}%")
    print("="*50)
    print(classification_report(y_test, y_pred, target_names=["Safe", "Drug"]))
    print("="*50)

    # Save models
    model_out = os.path.join(BASE_DIR, "text_model.pkl")
    vec_out = os.path.join(BASE_DIR, "vectorizer.pkl")
    
    with open(model_out, "wb") as f:
        pickle.dump(model, f)
    with open(vec_out, "wb") as f:
        pickle.dump(vectorizer, f)

    print(f"Saved: {model_out}")
    print(f"Saved: {vec_out}")

if __name__ == "__main__":
    main()
