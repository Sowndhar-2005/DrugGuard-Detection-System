"""
evaluate_models.py
DrugGuard — Model Evaluation Report Runner

Calculates confusion matrix metrics and sample predictions.
"""

import os
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset.csv")

TEST_CASES = [
    ("Want premium quality weed? DM me for delivery", 1),
    ("Got pills on deck tonight, cash only", 1),
    ("The doctor prescribed ibuprofen for my leg inflammation", 0),
    ("I need to study the chemistry of Lisinopril for the test", 0),
    ("⚡🔌 got the best cocaine in town, hit my inbox", 1),
    ("Looking for a running partner to train for a marathon", 0)
]

def main():
    if not os.path.exists(DATASET_PATH):
        print(f"❌ Dataset not found at: {DATASET_PATH}")
        return

    # Check for models
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

    model_path = get_path("text_model.pkl", "text_model.pkl")
    vec_path = get_path("vectorizer.pkl", "vectorizer.pkl")

    if not os.path.exists(model_path) or not os.path.exists(vec_path):
        print("❌ Model or vectorizer not found. Please train models first.")
        return

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(vec_path, "rb") as f:
        vectorizer = pickle.load(f)

    # Evaluate on full dataset split
    df = pd.read_csv(DATASET_PATH)
    X = df["text"].astype(str).str.lower()
    y = df["label"]

    _, X_test, _, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    X_test_vec = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_vec)

    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print("\n" + "="*60)
    print("  DRUGGUARD ML MODEL EVALUATION REPORT")
    print("="*60)
    print(f"  Accuracy:  {accuracy*100:.2f}%")
    print(f"  F1-Score:  {f1*100:.2f}%")
    print(f"  Precision: {precision*100:.2f}%")
    print(f"  Recall:    {recall*100:.2f}%")
    print("-"*60)
    print("  Confusion Matrix:")
    print(f"    True Negative (Safe):  {cm[0][0]:5d}  | False Positive (Error): {cm[0][1]:5d}")
    print(f"    False Negative (Error): {cm[1][0]:5d}  | True Positive (Drug):   {cm[1][1]:5d}")
    print("="*60)

    print("\nCurated Test Samples Verification:")
    print("-"*60)
    correct_samples = 0
    for text, expected in TEST_CASES:
        vec = vectorizer.transform([text.lower()])
        pred = int(model.predict(vec)[0])
        prob = float(model.predict_proba(vec)[0][1])
        status = "✅ PASS" if pred == expected else "❌ FAIL"
        label_str = "DRUG" if pred == 1 else "SAFE"
        print(f"  [{status}] {label_str} (Risk: {prob*100:5.1f}%): '{text}'")
        if pred == expected:
            correct_samples += 1

    print("-"*60)
    print(f"Summary: {correct_samples}/{len(TEST_CASES)} passed ({correct_samples/len(TEST_CASES)*100:.1f}%)")
    print("="*60 + "\n")

    # Save metrics JSON report
    report = {
        "accuracy": round(accuracy, 4),
        "f1_score": round(f1, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "confusion_matrix": cm.tolist()
    }
    with open(os.path.join(BASE_DIR, "evaluation_report.json"), "w") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    main()
