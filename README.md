# 🛡️ DrugGuard: Algospeak-Resilient Multimodal Drug Trafficking Detection System

<!-- DrugGuard Banner -->
<p align="center">
  <h1 align="center">🛡️ DrugGuard Detection System</h1>
  <p align="center"><strong>Algospeak-Resilient Multimodal Drug Trafficking Detection & Real-Time Intervention</strong></p>
</p>

[![IEEE Paper PDF](https://img.shields.io/badge/IEEE%20Paper-PDF%20Format-red?style=for-the-badge&logo=adobeacrobatreader)](file:///d:/Project/DrugGuard-Detection-System/paper/algospeak_paper.pdf)
[![IEEE Paper MD](https://img.shields.io/badge/IEEE%20Paper-Markdown%20Format-blue?style=for-the-badge&logo=markdown)](file:///d:/Project/DrugGuard-Detection-System/paper/algospeak.md)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![ONNX Runtime](https://img.shields.io/badge/ML%20Inference-ONNX%20Runtime-blueviolet?style=for-the-badge&logo=onnx)](https://onnxruntime.ai/)
[![Manifest V3](https://img.shields.io/badge/Chrome%20Extension-Manifest%20V3-4285F4?style=for-the-badge&logo=googlechrome)](https://developer.chrome.com/docs/extensions/mv3/intro/)

**Real-time client-side intervention system combining NLP Algospeak resilience, Computer Vision, and Chrome Extension DOM moderation.**

---

## 📌 System Overview & Methodology

**DrugGuard** addresses the rapid growth of illicit drug trafficking on social media platforms, where sellers use evasive communication tactics—collectively known as **algospeak** (emojis like ❄️🍃💊, leetspeak, intentional misspellings like `x*nax`, `p1lls`, and coded jargon). Conventional keyword moderation filters fail against these obfuscation techniques, and platform-level moderation is often post-hoc (reactive).

DrugGuard solves this with a **hybrid multimodal detection architecture** operating in real-time with **sub-300ms latency**.

```
[ Web Page DOM Content ]
        │
        ├──► Extract Text ──► [ Semantic Normalization ] ──► [ DistilBERT (ONNX) ] ┐
        │                                                                           ├─► [ Multimodal Fusion ] ──► [ Chrome Extension Overlay ]
        └──► Extract Images ───────────────────────────────► [ MobileNetV2 (ONNX) ] ┘
```

### 1. Semantic Normalization Layer
Before machine learning classification, raw text passes through a deterministic normalization pipeline:
- **Emoji Decoding**: Maps contextual drug emojis (e.g., ❄️ $\rightarrow$ cocaine, 🍃 $\rightarrow$ cannabis, 💊 $\rightarrow$ pills) into explicit semantic tokens.
- **Leetspeak & Character De-obfuscation**: Resolves obfuscated spellings (`x*nax` $\rightarrow$ `xanax`, `p1lls` $\rightarrow$ `pills`, `dr*gs` $\rightarrow$ `drugs`).
- **Slang Jargon Translation**: Normalizes underground trade jargon into standard vocabulary for transformer processing.

### 2. Transformer NLP Text Classifier (DistilBERT ONNX)
- Uses a fine-tuned **DistilBERT** model converted to **ONNX Runtime** format for ultra-fast local inference.
- Evaluates contextual semantics and algospeak patterns, returning a text risk probability score $S_{text} \in [0, 1]$ and identified risk keywords.
- *Fallback Mechanism*: Includes a TF-IDF + Logistic Regression secondary pipeline if ONNX runtime is unavailable.

### 3. Computer Vision Image Classifier (MobileNetV2 ONNX)
- Analyzes visual content (images, post attachments, thumbnails) using a fine-tuned **MobileNetV2** CNN exported to ONNX format.
- Detects illicit substance imagery, pill press shapes, and drug paraphernalia, producing a vision risk probability score $S_{vision} \in [0, 1]$.

### 4. Multimodal Fusion Engine
Integrates text and image probability scores via a weighted decision algorithm:

$$\text{Risk Score} = w_t \cdot S_{text} + w_v \cdot S_{vision}$$

- **High Risk ($\ge 0.70$ or explicit drug match)**: Triggers **BLOCK** action.
- **Medium Risk ($0.35 - 0.69$)**: Triggers **WARN** action.
- **Low Risk ($< 0.35$)**: Allows content as **SAFE**.

### 5. Client-Side Browser Intervention (Chrome Extension v4.0)
- **Non-intrusive DOM Blurring**: High-risk posts and illicit images are automatically blurred with heavy CSS filter (`blur(16px)`).
- **Top-Bar Action Banners**: Displays a sleek red top banner (`🛡️ Blocked: Coded drug content detected`) with a prominent **REVEAL** button.
- **Red Highlight on Reveal**: Clicking **REVEAL** un-blurs the content and highlights dangerous text in a distinct red left border and light red background.
- **Warning Highlight**: Medium-risk content is highlighted with a yellow background and border (no blur) with a **DISMISS** button.

---

## 📂 File & Project Structure

```
DrugGuard-Detection-System/
├── assets/                                    # Project Visual Assets
│   ├── logo.png                               # DrugGuard Shield Logo
│   └── banner.png                             # GitHub Repository Banner
├── extension/                                 # Chrome Extension (Manifest V3)
│   ├── manifest.json                          # Manifest V3 configuration (v4.0.0)
│   ├── content_script.js                      # DOM scraper & v4.0 overlay injector
│   ├── background.js                          # Service worker & extension coordinator
│   ├── popup.html                             # Control panel popup UI (v4.0 Indigo Theme)
│   └── popup.js                               # Real-time toggle & threshold slider controls
├── backend/                                   # FastAPI Machine Learning Server
│   ├── server.py                              # REST API endpoint with ONNX inference engine
│   ├── requirements.txt                       # Python dependencies
│   ├── setup_dataset_v3.py                    # Algospeak dataset generator script
│   ├── train_text_model.py                    # Local DistilBERT ONNX training pipeline
│   ├── train_image_model.py                   # Local MobileNetV2 ONNX vision training pipeline
│   ├── evaluate_models.py                     # Model benchmark & accuracy evaluation
│   ├── DrugGuard_Text_Training.ipynb          # DistilBERT Colab notebook
│   └── DrugGuard_Image_Training.ipynb         # MobileNetV2 Colab notebook
├── train/                                     # Exported ONNX & Model Artifacts
│   ├── text_model.onnx                        # Fine-tuned DistilBERT ONNX model
│   ├── text_model.onnx.data                   # Transformer weights binary
│   ├── image_model.onnx                       # MobileNetV2 vision ONNX model
│   ├── image_model.onnx.data                  # Vision model weights binary
│   ├── vectorizer.pkl                         # TF-IDF feature extractor fallback
│   ├── text_model.pkl                         # Logistic Regression fallback model
│   └── image_classes.json                     # Vision class mapping dictionary
├── paper/                                     # IEEE Academic Research Paper
│   ├── algospeak.md                           # Full IEEE formatted research paper (Markdown)
│   ├── algospeak_paper.pdf                    # Published IEEE format paper (PDF document)
│   └── image/                                 # System architecture diagrams & paper figures
├── test_page.html                             # End-to-End Verification Test Suite Webpage
└── README.md                                  # Project Documentation
```

---

## 🚀 How to Run the Project

### Step 1: Clone the Repository & Setup Python Environment
```bash
git clone https://github.com/Sowndhar-2005/DrugGuard-Detection-System.git
cd DrugGuard-Detection-System
```

Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate
```

Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start the FastAPI Backend Server
Run the FastAPI inference server:
```bash
python server.py
```
- The backend server will load the ONNX models (`text_model.onnx` and `image_model.onnx`) from the `train/` directory.
- The server listens at `http://localhost:8000`. You can verify API health by navigating to `http://localhost:8000/docs` in your browser.

### Step 3: Load the Chrome Extension (Manifest V3)
1. Open **Google Chrome**.
2. Navigate to `chrome://extensions/` in the address bar.
3. Enable **Developer mode** using the toggle switch in the top-right corner.
4. Click the **Load unpacked** button in the top-left corner.
5. Select the `extension/` directory from this project folder.
6. The **DrugGuard Protection System (v4.0.0)** extension icon will appear in your extensions bar!

---

## 🧪 How to Test the System

1. Ensure the backend server is running (`python server.py` at `http://localhost:8000`).
2. Open `test_page.html` in Chrome (or via a local HTTP server like Live Server `http://127.0.0.1:5500/test_page.html`).
3. Observe real-time intervention across the 3 test sections:

| Test Section | Content Type | Expected Behavior | Visual Result |
|---|---|---|---|
| **🚨 1. High Risk (Block)** | Emojis (🔌, ❄️, 🍃), Leetspeak (`x*nax`, `p1lls`), Opioids, Illicit Images | **BLOCKED** | Heavy blur + Red top banner (`🛡️ Blocked: Coded drug content detected`) + Image top banner |
| **⚠️ 2. Medium Risk (Warn)** | Prescription queries, dental postoperative painkiller questions | **WARNED** | Yellow background highlight + border + `Dismiss` button (No blur) |
| **✅ 3. Low Risk (Safe)** | FDA clinical news, gym fitness posts, medical pill images | **SAFE** | Clean display, no interventions |

### Testing Interactive Features:
- **Reveal Content**: Click the **REVEAL** button on any blocked text post. The blur disappears, and the text highlights with a red left border and subtle red background.
- **Reveal Image**: Click the **REVEAL** button at the top of any blocked image to reveal the image.
- **Extension Popup Control**: Click the DrugGuard extension icon to open the Control Panel:
  - Toggle protection ON/OFF.
  - Adjust sensitivity threshold slider ($0.10 - 0.90$).
  - View live session statistics (Texts scanned, Images scanned, Blocked count, Warned count).

---

## 📄 IEEE Academic Research Paper

This project is backed by comprehensive academic research published in IEEE format:

> **Title**: *Algospeak-Resilient Drug Trafficking Detection Using Transformer-Based Machine Learning and a Browser Extension*  
> **Authors**: Agalya M, Kalaipriya S, Sowndhar A, Rajalingam B  
> **Affiliation**: Department of CSE (AI & ML), KIT - Kalaignarkarunanidhi Institute of Technology, Coimbatore, India  
> **Keywords**: Drug Trafficking Detection, Algospeak, Transformer Models, DistilBERT, Multimodal Learning, Semantic Normalization, Browser Extension, Real-Time Intervention.

### Access Paper Formats:
- 📖 **Markdown Format**: [paper/algospeak.md](file:///d:/Project/DrugGuard-Detection-System/paper/algospeak.md)
- 📄 **PDF Format**: [paper/algospeak_paper.pdf](file:///d:/Project/DrugGuard-Detection-System/paper/algospeak_paper.pdf)

### Benchmark Results:
| Metric | Single-Modality Text | Single-Modality Vision | **DrugGuard Multimodal Fusion** |
|---|---|---|---|
| **Accuracy** | 88.4% | 85.2% | **94.0%** |
| **F1-Score** | 0.86 | 0.83 | **0.92** |
| **Precision** | 0.87 | 0.84 | **0.93** |
| **Recall** | 0.85 | 0.82 | **0.91** |
| **Latency** | 120 ms | 150 ms | **250–300 ms** (Sub-second real-time) |

---

## 🛡️ License

This project is developed for academic research and educational demonstration purposes. All rights reserved &copy; 2026.
