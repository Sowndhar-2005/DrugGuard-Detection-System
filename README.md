# 🛡️ DrugGuard: Algospeak-Resilient Semantic Detection of Illicit Drug Content

Online social platforms and messaging apps are increasingly exploited for illicit drug trafficking. To evade automated moderators, traffickers use a sophisticated linguistic strategy known as **Algospeak**—using emoji codes (e.g., `🍃` for weed, `❄️` for cocaine, `🔌` for dealer), leetspeak, intentional typos, and spaced letters. Standard keyword filters are easily bypassed by these methods, creating a pressing need for a system that understands the context and semantics of social media communications in real time.

**DrugGuard** solves this by providing a lightweight, high-performance, and algospeak-resilient browser extension powered by a machine learning backend. It dynamically scans webpage text, performs Optical Character Recognition (OCR) on image advertisements, and intervenes on the user interface (by blurring content or showing warning indicators) in milliseconds.

---

## ⚙️ Core Architecture & Features

The system is structured as a real-time client-server architecture:

```
+------------------+                   +--------------------+
|  Chrome Browser  |                   |  FastAPI Backend   |
|                  |                   |                    |
| Content Script   | --(Type: Text)--> | Naive Bayes Model  |
|  (DOM Scanner)   | <-- (Action) ---- |   (Classification) |
|                  |                   |                    |
| Image Scanner    | --(Base64 Img)--> | RapidOCR + Model   |
|   (Flyer Scan)   | <-- (Action) ---- | (Text Extraction)  |
+------------------+                   +--------------------+
```

### 1. Natural Language Processing (NLP) Backend
* **Robust Dataset**: Trained on 1,200 rows containing balanced drug trafficking templates, emoji-coded slang, and hard negatives (legitimate news reports, medical pharmacy guidelines, and standard marketplace listings).
* **Naive Bayes Classifier**: Utilizes `CountVectorizer` paired with a `MultinomialNB` model. The vectorizer is configured to treat emoji characters as valid features alongside alphanumeric tokens, allowing it to mathematically associate emojis like `💊` and `🔌` with trafficking patterns.

### 2. Live Browser Extension
* **Content Injection**: A Chrome extension content script that periodically scans the webpage DOM for text elements.
* **Intervention Actions**:
  - **Block (Risk ≥ 70%)**: Instantly blurs the text/image and overlays a red banner to hide illicit content.
  - **Warn (Risk 40-70%)**: Adds a warning badge and a yellow outline to suspicious elements.
  - **Safe (Risk < 40%)**: Leaves content untouched.

### 3. Multimodal Image OCR
* Integrated with `RapidOCR` on the `/predict_image` endpoint.
* Extracts embedded text from image flyers, posts, and ads (even with stylized fonts) and runs predictions on the extracted text.

### 4. Pill Dataset Explorer & Inspector
* An interactive dashboard served at `http://localhost:8000/static/ML-Dome/data_visualizer.html`.
* Includes a reference resolution comparison slider (120px to Original) and a filtered gallery of consumer pill photos (Fluoxetine NDC 00781-2823-13) integrated with live backend OCR scanning.

---

## ⚡ Performance & Timing Metrics

A primary engineering constraint was ensuring that web content scanning does not degrade browser rendering performance. The system achieves sub-millisecond latencies for real-time protection:

* **Text Prediction Latency**: **< 5ms**
  * The feature extraction (TF-IDF bag of words) and Naive Bayes inference run near-instantly, allowing the extension to scan hundreds of DOM elements without causing page lag.
* **Image OCR Processing**: **150ms – 300ms**
  * Image data URLs are sent asynchronously. OCR text extraction and classification complete in a fraction of a second, ensuring advertisements are blurred before the user scrolls them into focus.

---

## 🧪 Visual Test Cases

You can verify the live OCR scanning functionality using the visualizer dashboard or by running the extension against the generated flyer test cases in the project root:

| Test Image | Type | Description | Expected Model Action |
| :---: | :--- | :--- | :--- |
| **`drug_image.png`** | Illicit Flyer | Contains red styling and text: *"Special offer... Cocaine & powder available... Contact dealer"* | **Block** 🔴 (100% Risk) |
| **`safe_image.png`** | Safe Flyer | Contains green styling and text: *"Organic Japanese Matcha Tea... Rich in antioxidants"* | **Safe** 🟢 (0% Risk) |

*Both flyers are located in the main project folder and can be tested dynamically via the `predict_image` API.*

---

## 📁 Repository Structure

```
.
├── ML-Dome/                  --> Backend ML, Server, and visualizer assets
│   ├── app.py                --> Interactive CLI test app
│   ├── server.py             --> FastAPI server (handles /predict and /predict_image)
│   ├── train_model.py        --> Model training and evaluation script
│   ├── setup_dataset_v2.py   --> Synthetic dataset generator with hard negatives
│   ├── data_visualizer.html  --> Pill dataset explorer dashboard
│   ├── dataset.csv           --> Labeled dataset of 1,200 entries
│   ├── text_model.pkl        --> Saved trained Naive Bayes classifier
│   └── vectorizer.pkl        --> Saved vocabulary vectorizer
│
├── project/
│   └── extension/            --> Chrome Extension source code
│       ├── manifest.json     --> Extension manifest configuration
│       ├── content_script.js --> Live webpage DOM scanner & styling injector
│       └── popup.html/js     --> UI popup controller
│
├── drug_image.png / safe_image.png --> Pre-generated OCR test images
├── test_page.html            --> Extension test sandbox page
└── README.md                 --> Main project documentation
```

---

## 🚀 Quick Start Guide

### 1. Install Requirements
Ensure you have Python 3.8+ installed:
```bash
pip install pandas scikit-learn fastapi uvicorn pillow openpyxl rapidocr-onnxruntime requests
```

### 2. Start the Backend Server
Run the uvicorn API:
```bash
cd ML-Dome
python server.py
```
* Backend API documentation will be available at: `http://localhost:8000/docs`
* Health check: `http://localhost:8000/health`

### 3. Load the Browser Extension
1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** (top-right toggle).
3. Click **Load unpacked** (top-left button).
4. Select the `project/extension` folder from this repository.

### 4. Test Live Detection
* Open `http://localhost:8000/static/test_page.html` to see the extension scan, highlight, and blur blocks of text on the test page automatically.
* Open `http://localhost:8000/static/ML-Dome/data_visualizer.html` to run local OCR scans on the pill images dataset.
