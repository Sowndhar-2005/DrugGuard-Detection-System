# 🔍 DrugGuard: Naive Bayes NLP Model & FastAPI Server

This directory contains the machine learning backend and API server for the DrugGuard extension. It handles real-time text classification and image OCR scanning.

---

## 📁 Directory Structure

* `train_model.py` — Loads the dataset, trains a Multinomial Naive Bayes classifier, evaluates performance, and serializes the model and vectorizer.
* `setup_dataset_v2.py` — Generates a robust synthetic training dataset (`dataset.csv`) of 1,200 samples with hard negatives (news, medical, e-commerce) and emoji-coded slang.
* `server.py` — FastAPI server exposing `/predict` (for page text) and `/predict_image` (for base64 images via OCR) endpoints.
* `app.py` — Simple CLI program to manually test text predictions.
* `dataset.csv` — Labeled training data.
* `text_model.pkl` & `vectorizer.pkl` — Trained Naive Bayes model and fitted count vectorizer (CountVectorizer).

---

## ⚡ API Endpoints

### 1. `GET /health`
Quick health check to verify the server and model are running.

### 2. `POST /predict`
Used by the browser extension to scan raw text blocks in real time.
* **Request Body**: `{ "text": "string" }`
* **Response**:
  ```json
  {
    "action": "block", // "safe" | "warn" | "block"
    "risk_score": 0.941,
    "confidence": 94.1,
    "label": 1,
    "triggered_words": ["powder", "pickup"]
  }
  ```

### 3. `POST /predict_image`
Used to extract text from a base64 encoded image (such as advertisement flyers) using `RapidOCR` and classify it.
* **Request Body**: `{ "image": "data:image/png;base64,..." }`
* **Response**: Same as `/predict` response schema.

---

## ⚙️ How to Setup and Train

1. **Install Dependencies**:
   ```bash
   pip install pandas scikit-learn fastapi uvicorn pillow rapidocr-onnxruntime
   ```

2. **Generate the Dataset**:
   ```bash
   python setup_dataset_v2.py
   ```

3. **Train the Model**:
   ```bash
   python train_model.py
   ```

4. **Run Backend API Server**:
   ```bash
   python server.py
   ```
   * The API server runs on `http://localhost:8000`.
   * Check interactive documentation at `http://localhost:8000/docs`.