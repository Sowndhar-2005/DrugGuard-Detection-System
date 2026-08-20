import os, json, pickle, time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")

# --- 1. TF-IDF + Logistic Regression (Text Fallback) ---
df = pd.read_csv(os.path.join(BASE, "dataset.csv"))
X = df["text"].astype(str).str.lower()
y = df["label"]
_, X_test, _, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

with open(os.path.join(BASE, "text_model.pkl"), "rb") as f:
    text_model = pickle.load(f)
with open(os.path.join(BASE, "vectorizer.pkl"), "rb") as f:
    vectorizer = pickle.load(f)

X_test_vec = vectorizer.transform(X_test)

# Latency measurement for TF-IDF (single sample)
single_vec = vectorizer.transform(X_test.iloc[:1])
start = time.perf_counter()
for _ in range(1000):
    text_model.predict(single_vec)
tfidf_latency = (time.perf_counter() - start) / 1000 * 1000  # ms

y_pred_tfidf = text_model.predict(X_test_vec)
tfidf_acc = accuracy_score(y_test, y_pred_tfidf)
tfidf_f1 = f1_score(y_test, y_pred_tfidf)
tfidf_prec = precision_score(y_test, y_pred_tfidf)
tfidf_rec = recall_score(y_test, y_pred_tfidf)

print("=== TF-IDF + Logistic Regression (Text) ===")
print(f"  Accuracy:  {tfidf_acc*100:.2f}%")
print(f"  F1-Score:  {tfidf_f1:.4f}")
print(f"  Precision: {tfidf_prec:.4f}")
print(f"  Recall:    {tfidf_rec:.4f}")
print(f"  Avg Latency: {tfidf_latency:.2f} ms")

# --- 2. DistilBERT ONNX (Text) ---
TRAIN_DIR = os.path.join(BASE, "train")
onnx_text_path = os.path.join(TRAIN_DIR, "text_model.onnx")
has_onnx_text = os.path.exists(onnx_text_path)

if has_onnx_text:
    import onnxruntime as ort
    from transformers import DistilBertTokenizerFast
    
    sess_text = ort.InferenceSession(onnx_text_path)
    tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
    
    all_preds = []
    all_true = []
    
    for text_val, label_val in zip(X_test.values, y_test.values):
        enc = tokenizer(str(text_val), return_tensors="np", padding="max_length", truncation=True, max_length=128)
        inp = {"input_ids": enc["input_ids"].astype(np.int64), "attention_mask": enc["attention_mask"].astype(np.int64)}
        logits = sess_text.run(None, inp)[0]
        pred = int(np.argmax(logits, axis=1)[0])
        all_preds.append(pred)
        all_true.append(label_val)
    
    distil_acc = accuracy_score(all_true, all_preds)
    distil_f1 = f1_score(all_true, all_preds)
    distil_prec = precision_score(all_true, all_preds)
    distil_rec = recall_score(all_true, all_preds)
    
    # Latency (single sample)
    sample_enc = tokenizer("test sample text for latency measurement", return_tensors="np", padding="max_length", truncation=True, max_length=128)
    sample_inp = {"input_ids": sample_enc["input_ids"].astype(np.int64), "attention_mask": sample_enc["attention_mask"].astype(np.int64)}
    start = time.perf_counter()
    for _ in range(50):
        sess_text.run(None, sample_inp)
    distil_latency = (time.perf_counter() - start) / 50 * 1000
    
    print("\n=== DistilBERT ONNX (Text) ===")
    print(f"  Accuracy:  {distil_acc*100:.2f}%")
    print(f"  F1-Score:  {distil_f1:.4f}")
    print(f"  Precision: {distil_prec:.4f}")
    print(f"  Recall:    {distil_rec:.4f}")
    print(f"  Avg Latency: {distil_latency:.0f} ms")
else:
    print("\n=== DistilBERT ONNX (Text) === SKIPPED (model not found)")

# --- 3. MobileNetV2 ONNX (Vision) ---
onnx_img_path = os.path.join(TRAIN_DIR, "image_model.onnx")
has_onnx_img = os.path.exists(onnx_img_path)

if has_onnx_img:
    import onnxruntime as ort
    from PIL import Image
    
    # Load class mapping from training
    classes_path = os.path.join(TRAIN_DIR, "image_classes.json")
    with open(classes_path, "r") as f:
        class_info = json.load(f)
    # class_to_idx: {"drug": 0, "safe": 1}
    print(f"\n=== MobileNetV2 ONNX (Vision) ===")
    print(f"  [DEBUG] class_to_idx mapping: {class_info['class_to_idx']}")
    
    sess_img = ort.InferenceSession(onnx_img_path)
    input_name = sess_img.get_inputs()[0].name
    input_shape = sess_img.get_inputs()[0].shape
    
    # ImageNet normalization (same as training)
    MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    
    img_dir = os.path.join(BASE, "image")
    if os.path.isdir(img_dir):
        img_preds = []
        img_labels = []
        
        # Folders: safe/, unsafe/
        # Model classes: drug=0, safe=1
        folder_to_label = {
            "safe": 1,    # safe class index = 1
            "unsafe": 0,  # drug class index = 0
            "drug": 0,    # drug class index = 0 (alternative)
        }
        
        for label_name in sorted(os.listdir(img_dir)):
            label_dir = os.path.join(img_dir, label_name)
            if not os.path.isdir(label_dir):
                continue
            
            label_val = folder_to_label.get(label_name.lower(), 0)
            
            for fname in sorted(os.listdir(label_dir)):
                fpath = os.path.join(label_dir, fname)
                try:
                    img = Image.open(fpath).convert("RGB").resize((224, 224))
                    arr = np.array(img, dtype=np.float32) / 255.0
                    # Apply ImageNet normalization
                    arr = (arr - MEAN) / STD
                    # NCHW format
                    arr = arr.transpose(2, 0, 1)
                    arr = np.expand_dims(arr, axis=0)
                    logits = sess_img.run(None, {input_name: arr})[0]
                    pred = int(np.argmax(logits, axis=1)[0])
                    img_preds.append(pred)
                    img_labels.append(label_val)
                    
                    status = "[PASS]" if pred == label_val else "[FAIL]"
                    pred_name = "safe" if pred == 1 else "drug"
                    true_name = "safe" if label_val == 1 else "drug"
                    print(f"    {status} {fname}: predicted={pred_name}, actual={true_name}")
                except Exception as e:
                    print(f"    [ERROR] Error processing {fname}: {e}")
        
        if len(img_preds) > 0:
            img_acc = accuracy_score(img_labels, img_preds)
            # Use 'drug' (0) as positive class for F1/Precision/Recall
            img_f1 = f1_score(img_labels, img_preds, pos_label=0, zero_division=0)
            img_prec = precision_score(img_labels, img_preds, pos_label=0, zero_division=0)
            img_rec = recall_score(img_labels, img_preds, pos_label=0, zero_division=0)
            
            # Latency
            dummy = np.random.randn(1, 3, 224, 224).astype(np.float32)
            start = time.perf_counter()
            for _ in range(100):
                sess_img.run(None, {input_name: dummy})
            img_latency = (time.perf_counter() - start) / 100 * 1000
            
            print(f"  Accuracy:  {img_acc*100:.2f}%")
            print(f"  F1-Score:  {img_f1:.4f}")
            print(f"  Precision: {img_prec:.4f}")
            print(f"  Recall:    {img_rec:.4f}")
            print(f"  Avg Latency: {img_latency:.0f} ms")
            print(f"  Total images evaluated: {len(img_preds)}")
        else:
            print("  SKIPPED (no images found)")
    else:
        print(f"  SKIPPED (image dir not found at {img_dir})")
else:
    print("\n=== MobileNetV2 ONNX (Vision) === SKIPPED (model not found)")

print("\n=== EVALUATION COMPLETE ===\n")
