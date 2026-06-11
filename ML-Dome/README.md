# 🔍 Algospeak-Resilient Semantic Detection of Illicit Drug Content Using TF-IDF and Real-Time Browser Extension Architecture

An NLP-based machine learning system that analyzes text messages and classifies them as **Drug Trafficking (Illicit)** or **Safe (Normal)** using Natural Language Processing and Naive Bayes classification. Includes **emoji-coded message detection** — identifying drug emojis like 🍃💊❄️🍄💉 used as code on social media.

This repository also features a **Pill Dataset Visualization & Live OCR Scanning Dashboard** to browse and test model classification on real pill image datasets.

---

## 📌 About the Project

This project detects potential drug trafficking activity from plain text — such as social media posts, chat messages, or online listings. It uses a **Multinomial Naive Bayes** classifier trained on text data to identify suspicious language patterns commonly associated with illegal drug trade.

* **Algospeak / Emoji Detection:** The model recognizes emoji-coded drug messages — a common real-world tactic where dealers use emojis like 🍃 (marijuana), ❄️ (cocaine), 💊 (pills), 🍄 (mushrooms), and 🔌 (dealer/plug) to evade filters.
* **Multimodal Image OCR:** The backend exposes a `/predict_image` endpoint using `RapidOCR` to extract text from image advertisements and classify the extracted content.

---

## 🖼️ Pill Dataset Explorer & OCR Inspector

An interactive, high-fidelity visualizer dashboard is available to browse Legitimate Reference and Consumer-grade pill images of **Fluoxetine 10 MG (NDC 00781-2823-13)**.

### Features
1. **Reference Image Resolution Inspector**:
   - Side-by-side comparison of **RxNav API** catalog images vs **NLM Base** reference images.
   - Interactive slider to switch resolutions: `120px`, `300px`, `600px`, `800px`, `1024px`, and `Original`.
   - Hover zoom effect to inspect capsule marking details.
2. **Consumer Image Gallery**:
   - Filter and search through 17 consumer-grade photos taken under various lighting and layouts.
   - Elegant placeholders and handling for RAW camera files (`.CR2`) which browsers cannot render natively.
3. **Live Model OCR Scanner**:
   - Integrates directly with the FastAPI backend `/predict_image` endpoint.
   - Converts standard images to base64, runs OCR extraction, and renders the model’s prediction label (`Safe` 🟢, `Warn` 🟡, `Block` 🔴), risk score, and triggered drug keywords dynamically.

---

## 📁 Project Structure

```
Ml-Project/
│
├── ML-Dome/                  → Backend ML & Server code
│   ├── app.py                → Interactive CLI app to test predictions
│   ├── server.py             → FastAPI backend server (port 8000)
│   ├── setup_dataset_v2.py   → Generates synthetic dataset with hard negatives
│   ├── train_model.py        → Trains the Multinomial Naive Bayes classifier
│   ├── dataset.csv           → Training data (1200 rows, text + emoji)
│   ├── text_model.pkl        → Saved trained Naive Bayes model (.pkl)
│   ├── vectorizer.pkl        → Saved CountVectorizer (.pkl)
│   └── README.md             → Server and model documentation
│
├── sampleData/               → Pill images dataset (Fluoxetine 10mg)
│   ├── consumer/             → 17 consumer-grade pill images
│   ├── reference/            → Legitimate NLM and RxNav images at 6 resolutions
│   └── metadata.json         → Consolidated JSON metadata of the dataset
│
├── test_page.html            → Chrome extension test web page
├── data_visualizer.html      → Pill dataset explorer & live OCR scanner
└── drug_image.png / safe_image.png → Generated test flyers for OCR
```

---

## 🚀 How to Run

### Step 1: Install Dependencies
Make sure you have Python 3.8+ installed, then install the required packages:
```bash
pip install pandas scikit-learn fastapi uvicorn pillow openpyxl rapidocr-onnxruntime
```

### Step 2: Start the Backend Server
Navigate to the `ML-Dome` directory and run the FastAPI server:
```bash
cd ML-Dome
python server.py
```
* The server will start on `http://localhost:8000`.
* Check health at `http://localhost:8000/health`.

### Step 3: Launch the Visualizer Page
With the backend server running, open your browser and navigate to:
👉 **`http://localhost:8000/static/data_visualizer.html`**

You can use the slider to inspect reference resolutions and click **"Run OCR Scan"** on any consumer image card to see the backend OCR model classify it in real-time.

---

## 📊 Model Performance

Trained using `MultinomialNB` on 1,200 rows containing balanced safe text, hard negatives (medical, news, marketplace contexts), and illicit trafficking messages:

| Metric | Score |
| :--- | :--- |
| **Accuracy** | **98.33%** |
| **F1-Score** | **0.98** |

---

## 🔤 Emoji Code Reference

Common emojis used as drug codes on social media:

| Emoji | Drug Code Meaning |
| :--- | :--- |
| 🍃🌿 | Marijuana / Weed |
| ❄️ | Cocaine |
| 💊 | Pills / MDMA / Xanax |
| 🍄 | Mushrooms / Psychedelics |
| 💉 | Heroin / Injectables |
| 🔌 | Plug / Dealer |
| 📦 | Package / Shipment |
| 💰💵 | Money / Payment |
| 🔥 | High Quality |
| ⚡ | Fast Delivery |
| 🤫 | Secrecy / Discreet |