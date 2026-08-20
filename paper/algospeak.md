<div style="font-family: 'Times New Roman', Times, serif; text-align: justify; line-height: 1.4; font-size: 11pt;">

<h1 align="center" style="font-size: 20pt; font-weight: bold; margin-top: 10px; margin-bottom: 15px;">Algospeak-Resilient Drug Trafficking Detection Using Transformer-Based Machine Learning and a Browser Extension</h1>

<table align="center" border="0" style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
  <tr style="border: none;">
    <td align="center" style="width: 50%; vertical-align: top; border: none; padding-bottom: 15px;">
      <b>Agalya M</b><br>
      <span style="font-size: 9pt;">UG Scholar, Department of CSE(AI&ML),<br>
      KIT-Kalaignarkarunanidhi Institute of Technology,<br>
      Coimbatore, India<br>
      <a href="mailto:kit28.24bam003@gmail.com">kit28.24bam003@gmail.com</a></span>
    </td>
    <td align="center" style="width: 50%; vertical-align: top; border: none; padding-bottom: 15px;">
      <b>Kalaipriya S</b><br>
      <span style="font-size: 9pt;">UG Scholar, Department of CSE(AI&ML),<br>
      KIT-Kalaignarkarunanidhi Institute of Technology,<br>
      Coimbatore, India<br>
      <a href="mailto:kit28.24bam031@gmail.com">kit28.24bam031@gmail.com</a></span>
    </td>
  </tr>
  <tr style="border: none;">
    <td align="center" style="width: 50%; vertical-align: top; border: none;">
      <b>Sowndhar A</b><br>
      <span style="font-size: 9pt;">UG Scholar, Department of CSE(AI&ML),<br>
      KIT-Kalaignarkarunanidhi Institute of Technology,<br>
      Coimbatore, India<br>
      <a href="mailto:kit28.bam303@gmail.com">kit28.bam303@gmail.com</a></span>
    </td>
    <td align="center" style="width: 50%; vertical-align: top; border: none;">
      <b>Rajalingam B *</b><br>
      <span style="font-size: 9pt;">Assistant Professor, Department of CSE(AI&ML),<br>
      KIT-Kalaignarkarunanidhi Institute of Technology,<br>
      Coimbatore, India<br>
      <a href="mailto:brajalingamnec@gmail.com">brajalingamnec@gmail.com</a></span>
    </td>
  </tr>
</table>

<div style="margin: 0 20px 20px 20px; font-size: 10pt; text-align: justify; line-height: 1.4;">
<b><i>Abstract</i> — The rapid proliferation of social media platforms has significantly expanded the attack surface for illicit drug trafficking, wherein dealers employ obfuscated communication strategies collectively termed algospeak comprising emojis, abbreviations, leetspeak, and coded terminology to evade automated moderation systems. Existing detection approaches, primarily reliant on keyword filtering and post-hoc machine learning analysis, are inadequate for identifying evolving obfuscation patterns or enabling real-time intervention. This paper proposes an algospeak-resilient, multimodal drug trafficking detection system that integrates transformer-based natural language processing, convolutional neural network-based image classification, and client-side browser intervention. A semantic normalization layer is introduced to systematically decode emojis, slang, and obfuscated text into structured representations amenable to downstream model inference. Normalized text is classified using a fine-tuned DistilBERT model, while visual content is analyzed via a MobileNet-based CNN. A weighted fusion mechanism combines both modality outputs to compute a unified risk score, upon which a Chrome extension performs real-time content blurring or blocking. Evaluated on the Reddit Drug Corpus and a manually annotated dataset encompassing algospeak-heavy samples, the proposed multimodal system achieves 94% accuracy and an F1-score of 0.92, outperforming all single-modality baselines, while maintaining an end-to-end response latency of 250-300 ms suitable for real-time deployment.</b>
<br><br>
<b><i>Keywords</i> — Drug Trafficking Detection, Algospeak, Transformer Models, DistilBERT, Multimodal Learning, Semantic Normalization, Browser Extension, Real-Time Intervention.</b>
</div>

<hr style="border: 0.5px solid #ccc; margin-bottom: 20px;">

<div style="text-align: justify; font-size: 10.5pt; line-height: 1.5;">

### I. INTRODUCTION

The rapid expansion of social media and online communication platforms has fundamentally altered the operational landscape of illicit drug trafficking. Platforms including forums, encrypted messaging applications, and open social networks are increasingly exploited by traffickers to advertise, coordinate, and facilitate the distribution of controlled substances. Unlike traditional offline channels, these digital environments offer anonymity, global reach, and near-zero operational cost, rendering detection and law enforcement substantially more challenging.

To circumvent automated content moderation systems, traffickers have developed sophisticated linguistic obfuscation strategies collectively referred to as "algospeak." These strategies encompass the deliberate use of emojis as symbolic substitutes (e.g., 💊 emoji to represent controlled substances), abbreviated or fragmented spellings (e.g., "d r u g s"), leetspeak encodings (e.g., "dr*gs"), and domain-specific coded terminology that continuously evolves. Such techniques systematically undermine conventional keyword-based detection pipelines, which lack the semantic flexibility required to interpret context-dependent obfuscation.

Existing approaches to automated drug trafficking detection can be broadly categorized into keyword-based filtering and machine learning-based classification. While recent transformer-based models such as BERT have significantly advanced contextual text understanding, the majority of deployed systems operate at the platform level as post-hoc analyzers — processing content only after it has been published. This reactive architecture introduces an inherent temporal gap between content publication and moderation action, during which harmful content remains accessible to users. Furthermore, these systems are typically unimodal, failing to exploit the visual signals (e.g., images of substances or paraphernalia) that frequently accompany drug-related posts.

To address these limitations, this paper proposes a real-time, algospeak-resilient drug trafficking detection system that unifies natural language processing, computer vision, and browser-level intervention within a single operational framework. The system introduces a semantic normalization layer that transforms emojis, slang, and obfuscated text into standardized representations, thereby improving the interpretability of model inputs. Normalized text is subsequently analyzed using a fine-tuned DistilBERT classifier, while accompanying images are assessed using a MobileNet-based CNN. A weighted fusion strategy integrates both modality outputs into a unified risk score, which drives immediate intervention by a Chrome browser extension capable of blurring, blocking, or flagging harmful content at the client side.

The principal contributions of this work are as follows:
1. A real-time, browser-integrated detection and intervention system for drug trafficking content operating at the user level.
2. A semantic normalization layer for structured decoding of algospeak, including emojis, slang, and leetspeak.
3. A multimodal detection framework combining DistilBERT-based NLP with MobileNet-based image classification.
4. A lightweight, scalable architecture validated for real-time deployment with sub-300 ms end-to-end latency.

### II. RELATED WORK

Detecting illicit drug trafficking on online platforms has garnered significant research attention due to the rising misuse of social media and encrypted communication channels [1][3][14]. Existing research can be broadly grouped into transformer-based detection systems, algospeak and jargon analysis, multimodal learning approaches, and browser-based intervention techniques.

#### A. Transformer-Based Drug Trafficking Detection
Recent advances in natural language processing have enabled the application of large-scale transformer models to the problem of illicit content detection. The Narcotrace framework [2] is among the earliest systems to leverage BERT for classifying drug-related posts on social media, demonstrating that contextual semantic representations substantially outperform traditional bag-of-words and keyword-matching approaches. Building on this, Hu et al. [7] proposed a knowledge-prompted adaptation of ChatGPT that incorporates domain-specific priors to improve the detection of indirect and ambiguous drug-related language. While these methods achieve strong classification performance, they are architecturally confined to backend deployment and offer no mechanism for real-time, user-level intervention.

#### B. Algospeak and Jargon Detection
The emergence of algospeak has introduced a distinct challenge for content moderation systems. Traffickers systematically employ emojis, phonetic abbreviations, and intentionally obfuscated spellings to bypass automated filters [11]. Song et al. [3][4] proposed the JEDIS framework, which applies delexicalized distant supervision to identify latent drug-related terminology in informal online conversations. By combining contextual token embeddings with word-attribute-level analysis, JEDIS demonstrates effective generalization to previously unseen slang on platforms such as Reddit. Ahmad et al. [5] further explored context-aware transformer models for analyzing informal and semi-encrypted communication, confirming that semantic context is critical for decoding obfuscated intent. Li et al. [6] demonstrated machine learning methods for identifying illegal drug vendors on Instagram based on textual and hashtag patterns. However, the majority of these approaches are confined to text-based analysis and do not incorporate explicit normalization techniques that convert emojis and slang into structured token sequences prior to model inference.

#### C. Multimodal Detection Approaches
Drug trafficking content frequently combines textual and visual elements, including images of controlled substances, packaging, or associated paraphernalia. To exploit this, multimodal learning frameworks have been proposed that jointly process text and image inputs [8][9]. Studies integrating CNNs with transformer-based encoders have demonstrated that cross-modal fusion consistently outperforms single-modality classifiers on ambiguous or partially obfuscated content. Hayashi and Nojima [10] further explored image classification combined with real-time social network monitoring, achieving improved recall on visually-dominated posts. Despite these advances, existing multimodal systems are predominantly designed for offline batch analysis and have not been optimized for low-latency, real-time deployment.

#### D. Browser-Based Content Intervention
Browser extensions have been explored as a complementary mechanism for real-time content modification at the client side, leveraging Document Object Model (DOM) monitoring to dynamically alter or suppress webpage content as it is rendered [12][13]. Jahanbakhsh et al. [12] demonstrated the feasibility of real-time DOM overlays for user signaling via browser extensions. Park et al. [13] introduced client-side visual and textual transformations for real-time personalized content moderation. However, existing browser-based approaches are predominantly rule-based or lack integration with learned multimodal semantic models, limiting their capacity to detect complex patterns such as algospeak or multimodal trafficking cues.

#### E. Research Gap
The literature reveals a consistent bifurcation: systems that achieve high detection accuracy through advanced modeling are deployed as offline, platform-level analyzers, while systems that enable real-time intervention rely on shallow, rule-based logic. No existing solution integrates (1) robust semantic normalization of algospeak, (2) multimodal detection leveraging both text and image modalities, and (3) real-time, user-level intervention within a unified operational framework. The present work directly addresses this gap.

### III. SYSTEM ARCHITECTURE

#### A. Architectural Overview
The proposed system adopts a client-server architecture designed to detect and suppress drug-related content on web pages in real time. The architecture decouples browser-side content extraction and intervention from server-side machine learning inference, enabling independent scalability of each component. The system comprises three primary modules:
1. the Browser Extension (Client Layer)
2. the Machine Learning Backend
3. the Decision and Intervention Module

Upon page load, the browser extension extracts visible text and image data from the DOM and transmits it securely to the backend server. The server applies semantic normalization followed by parallel text and image classification, producing a unified risk score. This score is returned to the extension, which executes the appropriate intervention action directly within the browser.

<div style="text-align: center; margin: 15px 0;">

<img src="image/Architectural Diagram.png" style="width: 100%; max-width: 100%; height: auto;" alt="Fig. 1: Architectural Diagram">

<p style="font-size: 9pt; font-weight: bold; margin-top: 5px;">Fig. 1: Architectural Diagram</p>
</div>

#### B. Browser Extension (Client Layer)
The browser extension is implemented using the Chrome Extension Manifest V3 API and serves as the interface between the user's browsing session and the detection backend. A MutationObserver instance is registered against the DOM to continuously monitor structural changes, enabling detection of dynamically loaded content such as infinite-scroll posts and asynchronously rendered comments without requiring page reloads. The extension performs the following operations:
- Extraction of visible text nodes from the DOM.
- Identification and retrieval of image source URLs.
- Lightweight HTML sanitization to remove non-content markup.
- Secure transmission of extracted data to the backend via HTTPS POST requests.
- Rendering of intervention actions, including semi-transparent blur overlays and warning banners, upon receipt of high-risk scores.

#### C. Machine Learning Backend
The backend server is implemented using the FastAPI framework in Python, selected for its asynchronous request handling, low overhead, and native compatibility with the Hugging Face Transformers and TensorFlow/Keras ecosystems. The backend exposes a RESTful inference endpoint that accepts multimodal inputs, executes the detection pipeline, and returns a structured JSON response containing the risk score and recommended action. Both models are pre-loaded into memory at server initialization to eliminate per-request model loading latency. The backend inference pipeline consists of four sequential stages:
1. Semantic normalization of input text.
2. Text classification via a fine-tuned DistilBERT model.
3. Image classification via a MobileNet-based CNN.
4. Weighted fusion of model outputs to compute the unified risk score.

#### D. Semantic Normalization Layer
The semantic normalization layer constitutes a critical preprocessing stage responsible for transforming obfuscated, informal, and emoji-encoded input text into structured representations suitable for downstream NLP inference. The layer applies three sequential transformations: (1) emoji-to-text mapping, wherein Unicode emoji characters are replaced with their semantic textual equivalents (e.g., the pill emoji maps to "pill"); (2) slang decoding, wherein a domain-specific lexicon maps coded drug-related terms to their standard equivalents; and (3) noise removal, wherein leetspeak encodings and irregular character spacing (e.g., "dr*gs", "d r u g s") are normalized to canonical token forms. This preprocessing step substantially improves the ability of the DistilBERT model to capture contextual semantics in obfuscated inputs.

#### E. Decision and Intervention Module
The decision module computes a final risk score by fusing the probabilistic outputs of the text and image classifiers using a weighted linear combination (detailed in Section IV-E). The resulting score is compared against predefined thresholds to determine the appropriate intervention: scores below 0.4 indicate low risk and require no action; scores between 0.4 and 0.7 indicate medium risk and trigger a warning overlay; scores of 0.7 and above indicate high risk and initiate content blurring or full blocking. These threshold values were determined empirically through validation set analysis to balance detection sensitivity against false positive rate.

#### F. System Workflow Summary
The end-to-end system workflow proceeds as follows:
1. Webpage content is monitored and extracted by the browser extension via DOM traversal.
2. Extracted text and image data are transmitted securely to the FastAPI backend.
3. Semantic normalization is applied to the raw text input.
4. Parallel text and image classification is performed by DistilBERT and MobileNet respectively.
5. A unified risk score is computed via weighted fusion.
6. The browser extension applies the appropriate intervention action based on threshold comparison.

### IV. METHODOLOGY

#### A. Input Processing and Data Extraction
The system ingests raw text and image data extracted from web pages via the browser extension. Input text may include user-generated posts and comments containing informal language, domain-specific slang, emoji sequences, and deliberate character-level obfuscation. Images may depict controlled substances, packaging, or associated paraphernalia. Due to the noisy and unstructured nature of these inputs, preprocessing is applied prior to model inference.

#### B. Semantic Normalization
Let the raw input text be denoted as $T_{raw}$. The normalized representation $T_{norm}$ is obtained via:

$$T_{norm} = f_{norm}(T_{raw}) \quad \dots \ (1)$$

where $f_{norm}(\cdot)$ denotes a composite normalization function integrating emoji mapping, slang decoding, and noise removal mechanisms such as leetspeak normalization and spacing correction.

Fig. 2 depicts the semantic normalization pipeline, wherein raw, obfuscated inputs are progressively transformed into structured textual representations. By enforcing consistency across diverse surface forms, this process enables the model to capture underlying semantic intent and improves robustness to previously unseen algospeak patterns.

<div style="text-align: center; margin: 15px 0;">

<img src="image/Semantic Normalization.png" style="width: 100%; max-width: 100%; height: auto;" alt="Fig. 2: Semantic Normalization">

<p style="font-size: 9pt; font-weight: bold; margin-top: 5px;">Fig. 2: Semantic Normalization</p>
</div>

#### C. Text Classification Using DistilBERT
The normalized text $T_{norm}$ is passed to a fine-tuned DistilBERT model. DistilBERT is a distilled variant of BERT that retains approximately 97% of BERT's language understanding performance while reducing parameter count by 40% and inference time by approximately 60%, making it well-suited for latency-constrained deployment. The model produces a drug-related content probability score $P_{text} \in [0, 1]$ via a binary classification head with sigmoid activation applied over the `[CLS]` token representation.

#### D. Image Classification Using MobileNet-Based CNN
Visual inputs are analyzed using a MobileNet-based convolutional neural network. MobileNet's depthwise separable convolution architecture reduces computational cost significantly compared to standard convolutions while maintaining competitive classification accuracy, making it appropriate for real-time inference. An input image $I$ is passed through the CNN to produce a classification probability $P_{image} \in [0, 1]$ representing the likelihood of drug-related visual content.

#### E. Multimodal Fusion Strategy
To leverage the complementary discriminative power of textual and visual modalities, the system employs a weighted linear fusion strategy. The unified risk score $S$ is computed as:

$$S = \alpha \cdot P_{text} + (1 - \alpha) \cdot P_{image} \quad \dots \ (2)$$

where $\alpha = 0.7$ is a weighting coefficient determined empirically through validation set optimization, reflecting the relatively higher discriminative contribution of textual features in the Reddit-derived dataset. This formulation allows the risk score to remain sensitive to visual cues even when textual content is minimal or absent (Fig. 3).

<div style="text-align: center; margin: 15px 0;">

<img src="image/Multimodal Fusion Strategy.png" style="width: 100%; max-width: 100%; height: auto;" alt="Fig. 3: Multimodal Fusion Strategy">

<p style="font-size: 9pt; font-weight: bold; margin-top: 5px;">Fig. 3: Multimodal Fusion Strategy</p>
</div>

#### F. Decision Thresholding
The computed risk score $S$ is mapped to an intervention action using the following threshold policy, derived from precision-recall trade-off analysis on the validation set:
- $S < 0.4$: Content classified as safe; no action taken.
- $0.4 \le S < 0.7$: Content classified as suspicious; warning overlay displayed.
- $S \ge 0.7$: Content classified as high-risk; content blurred or blocked.

### V. TECHNICAL IMPLEMENTATION

#### A. Backend Development
The backend server is implemented with FastAPI in Python, which provides asynchronous request handling and native compatibility with machine learning model execution. The backend exposes RESTful API endpoints `(server.py:273-353)` that process incoming JSON-encoded HTTP POST payloads. Text classification is handled by a fine-tuned DistilBERT model, which is loaded into memory at server startup `(server.py:82-89)` to eliminate request-time loading overhead. Image classification is performed using a MobileNet-based convolutional neural network `(server.py:114-124)` optimized with depthwise separable convolutions to maintain low latency. An OCR pipeline built with the RapidOCR engine `(server.py:134)` extracts text from images, feeding it to the normalization and text classification pipeline to detect text embedded within visual content.

#### B. Browser Extension
The client-side interface is built as a Google Chrome extension using Manifest V3 `(manifest.json:2)`. The extension's architecture is structured into a Manifest file, a background service worker, a content injection script, and an interactive statistics dashboard popup.

1. **Manifest Configuration**: The manifest specifies permissions for `storage`, `activeTab`, and `scripting` `(manifest.json:6-10)` to enable DOM interaction and settings persistence. The background worker is defined as a service worker `(manifest.json:14-16)`, and content scripts are configured to inject at `document_idle` `(manifest.json:21)` across all matching URLs.
2. **Background Service Worker**: The background script `(background.js)` acts as a central coordinator. Upon installation, it writes initial default values to local storage, including the active protection toggle, inference statistics counters, the threshold configuration, and the target backend endpoint URL `(background.js:4-13)`. It implements listeners for runtime message requests from the content script and popup interface to update and fetch active session statistics `(background.js:18-39)`.
3. **Content Script DOM Traversal**: The content script `(content_script.js)` executes inside the context of the loaded webpage. It monitors structural updates in the webpage DOM using a `MutationObserver` instance `(content_script.js:80-99)` that listens for child node additions. Dynamic updates are debounced by 1000 milliseconds `(content_script.js:91)` to prevent excessive scan passes.
4. **Text and Image Parsing**: Text nodes are queried using a tag selector `(content_script.js:113)` that targets paragraph elements, headings, spans, and post containers. Texts with a length between 15 and 1500 characters are processed `(content_script.js:119)`. Image elements are queried by checking if their source starts with standard protocols `(content_script.js:129)`. To prevent cross-origin canvas errors on local file systems during local E2E testing, image elements are passed to a converter `(content_script.js:237-256)` which attempts to parse them into standard base64 data URLs before submission to the backend `/predict_image` endpoint.
5. **DOM Modification and Overlay Injection**: When the backend returns a classification action of `block` or `warn` `(server.py:248-254)`, the content script modifies the webpage structure. For a `block` action, the target element is wrapped in a container class `(content_script.js:195-200)`, blurred using a heavy filter `(content_script.js:203)`, and a warning banner containing the detected keywords and a manual reveal button is appended to the DOM `(content_script.js:205-224)`. A `warn` action applies a light blur class `(content_script.js:228)` that clears on a single click.
<div style="text-align: center; margin: 15px 0;">

<img src="image/extension_ui_dashboard.png" style="width: 50%; max-width: 50%; height: auto;" alt="Fig. 8: DrugGuard Extension User Interface Statistics Dashboard">

<p style="font-size: 9pt; font-weight: bold; margin-top: 5px;">Fig. 8: DrugGuard Extension User Interface Statistics Dashboard</p>
</div>


#### C. Communication Protocol
The browser extension and backend communicate via HTTP POST requests using JSON-encoded payloads. The extension sends text data under the `text` attribute `(server.py:258-259)` and image base64 data under the `image` attribute `(server.py:261-262)`. The backend returns a response containing the action string, the risk score, the classification label, and the list of triggered words `(server.py:264-270)`.

#### D. Real-Time Processing Optimization
To achieve low latency, the system utilizes three primary optimizations:
1. **Pre-Loaded Models**: Both deep learning models are loaded into CPU memory when the FastAPI application starts `(server.py:143-145)`, avoiding runtime initialization delay.
2. **Asynchronous Execution**: The API endpoints are implemented with FastAPI's asynchronous routing, enabling non-blocking execution under concurrent scan requests.
3. **WeakSet Processing Cache**: The content script maintains a `WeakSet` named `processedElements` `(content_script.js:72)` that caches references to analyzed DOM elements, preventing duplicate API requests on unchanged elements during subsequent MutationObserver cycles.

#### E. Deployment Environment
The server runs locally during development and testing on `http://localhost:8000` `(background.js:12)`. For production deployment, the backend can be containerized using Docker and hosted on cloud environments such as AWS EC2 or Google Cloud Run, with the extension configured to route queries to the cloud API.

#### F. Security Considerations
Data privacy and security are managed through local hosting and scoped host permissions. The extension restricts network access to the specified backend server URL `(manifest.json:11-13)`, ensuring webpage content is only transmitted to the authorized analysis API.

### VI. DATASET AND TRAINING

#### A. Dataset Description
The system is trained and evaluated using a combination of large-scale public data and manually curated samples designed to capture both explicit and algospeak-encoded drug-related content (Fig. 4).

**Reddit Drug Corpus**: A large-scale dataset comprising approximately 1.27 million posts sourced from drug-related subreddits. The corpus encompasses a wide range of content including both licit and illicit discussions, informal language, and domain-specific slang, providing broad coverage of real-world linguistic variation.

**Manually Annotated Dataset**: To improve detection of novel and evolving algospeak patterns, a supplementary dataset was constructed by collecting and labeling social media samples. This dataset includes positive-class samples (drug-related posts), negative-class samples (non-drug content), and samples containing emojis, abbreviations, and coded language. Human annotators verified all labels to ensure accuracy and real-world alignment.

<div style="text-align: center; margin: 15px 0;">

<img src="image/img_0004.jpeg" style="width: 100%; max-width: 100%; height: auto;" alt="Fig. 4: Dataset Composition">

<p style="font-size: 9pt; font-weight: bold; margin-top: 5px;">Fig. 4: Dataset Composition</p>
</div>

#### B. Data Preprocessing
Prior to training, all data undergoes the following preprocessing steps:
- Text inputs are processed through the semantic normalization layer to handle emojis, slang, and obfuscated characters.
- Normalized text is tokenized using the DistilBERT WordPiece tokenizer with a maximum sequence length of 512 tokens.
- Duplicate and near-duplicate entries are removed to prevent data leakage.
- Images are resized to $224 \times 224$ pixels and normalized to the input distribution expected by MobileNet.

#### C. Data Splitting
The dataset is partitioned using stratified sampling to preserve class distribution across splits: Training Set (70%), Validation Set (15%), and Test Set (15%). Stratified sampling ensures that each partition contains a representative proportion of drug-related and non-drug-related samples (Fig. 5).

<div style="text-align: center; margin: 15px 0;">

<img src="image/img_0005.jpeg" style="width: 100%; max-width: 100%; height: auto;" alt="Fig. 5: Dataset Split Distribution">

<p style="font-size: 9pt; font-weight: bold; margin-top: 5px;">Fig. 5: Dataset Split Distribution</p>
</div>

#### D. Training Configuration
**Text Model (DistilBERT)**: The model is fine-tuned using Binary Cross-Entropy loss with the Adam optimizer (learning rate: 2e-5, batch size: 16) for 5-10 epochs until validation loss convergence.

**Image Model (MobileNet)**: The MobileNet-based classifier is trained using Binary Cross-Entropy loss with the Adam optimizer (batch size: 32) for 10-15 epochs. Data augmentation techniques including random rotation, horizontal flipping, and zoom are applied to improve generalization to unseen image variations.

#### E. Handling Class Imbalance
To address the inherent class imbalance between drug-related and non-drug-related samples, the following strategies are applied: class-weighted loss functions to penalize misclassification of the minority class; oversampling of minority-class training instances; and image-level data augmentation to increase effective sample count for underrepresented visual categories.

#### F. Evaluation Metrics
Model performance is assessed using the following standard classification metrics: Accuracy (overall prediction correctness), Precision (fraction of positive predictions that are correct), Recall (fraction of actual positives correctly identified), and F1-Score (harmonic mean of precision and recall). These metrics collectively provide a robust assessment of model performance under class imbalance conditions.

### VII. RESULTS AND EVALUATION

#### A. Quantitative Results
Table I presents the performance comparison between single-modality baseline models and the proposed multimodal system. All models are evaluated on the held-out test set under identical experimental conditions.

<div style="margin: 15px 0;">

<table style="width: 100%; border-collapse: collapse; font-size: 9pt; text-align: center;">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #333; padding: 4px;">Model</th>
      <th style="border: 1px solid #333; padding: 4px;">Accuracy</th>
      <th style="border: 1px solid #333; padding: 4px;">Precision</th>
      <th style="border: 1px solid #333; padding: 4px;">Recall</th>
      <th style="border: 1px solid #333; padding: 4px;">F1-Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #333; padding: 4px;">CNN (Image Only)</td>
      <td style="border: 1px solid #333; padding: 4px;">88%</td>
      <td style="border: 1px solid #333; padding: 4px;">0.85</td>
      <td style="border: 1px solid #333; padding: 4px;">0.87</td>
      <td style="border: 1px solid #333; padding: 4px;">0.86</td>
    </tr>
    <tr>
      <td style="border: 1px solid #333; padding: 4px;">BERT (Text Only)</td>
      <td style="border: 1px solid #333; padding: 4px;">90%</td>
      <td style="border: 1px solid #333; padding: 4px;">0.88</td>
      <td style="border: 1px solid #333; padding: 4px;">0.89</td>
      <td style="border: 1px solid #333; padding: 4px;">0.88</td>
    </tr>
    <tr>
      <td style="border: 1px solid #333; padding: 4px;">DistilBERT (Proposed — Text)</td>
      <td style="border: 1px solid #333; padding: 4px;">92%</td>
      <td style="border: 1px solid #333; padding: 4px;">0.90</td>
      <td style="border: 1px solid #333; padding: 4px;">0.91</td>
      <td style="border: 1px solid #333; padding: 4px;">0.90</td>
    </tr>
    <tr>
      <td style="border: 1px solid #333; padding: 4px;"><b>Multimodal (Proposed — Full)</b></td>
      <td style="border: 1px solid #333; padding: 4px;"><b>94%</b></td>
      <td style="border: 1px solid #333; padding: 4px;"><b>0.92</b></td>
      <td style="border: 1px solid #333; padding: 4px;"><b>0.93</b></td>
      <td style="border: 1px solid #333; padding: 4px;"><b>0.92</b></td>
    </tr>
  </tbody>
</table>

<p style="font-size: 9pt; text-align: center; font-weight: bold; margin-top: 5px;">TABLE I: Performance Comparison of Detection Models</p>
</div>

#### B. Performance Analysis
The DistilBERT model achieves higher accuracy than the CNN-only baseline (92% vs. 88%) due to its capacity to capture long-range contextual dependencies in text, which are critical for interpreting implicit or indirect drug references. However, relying solely on textual features introduces vulnerability to posts where illicit intent is conveyed primarily through visual content with minimal descriptive text. The multimodal system addresses this by integrating MobileNet-based image classification, yielding an additional 2-percentage-point improvement in accuracy (94%) and a corresponding F1-score gain to 0.92. This result confirms that cross-modal fusion provides complementary discriminative signal beyond what either modality achieves independently.

#### C. Impact of Semantic Normalization (Ablation Study)
To quantify the contribution of the semantic normalization layer, an ablation study was conducted by evaluating the DistilBERT text classifier with and without the normalization preprocessing stage. Without normalization, the model achieves 85% accuracy and an F1-score of 0.83. Upon applying the full normalization pipeline, accuracy improves to 92% and F1-score to 0.90 — representing a 7-percentage-point gain in accuracy and a 0.07 improvement in F1-score. These results confirm that semantic normalization is a functionally critical component that enables the model to generalize across previously unseen algospeak patterns not encountered during training (Fig. 6).

<div style="text-align: center; margin: 15px 0;">

<img src="image/img_0006.jpeg" style="width: 100%; max-width: 100%; height: auto;" alt="Fig. 6: Effect of Semantic Normalization">

<p style="font-size: 9pt; font-weight: bold; margin-top: 5px;">Fig. 6: Effect of Semantic Normalization</p>
</div>

#### D. Real-Time Performance
The system was evaluated for inference latency under simulated real-world load conditions. Average per-request processing times are as follows: text normalization and DistilBERT inference: ~120 ms; MobileNet image inference: ~150 ms; total end-to-end response time (including network round-trip): ~250-300 ms. These figures demonstrate that the system satisfies real-time responsiveness requirements without perceptible latency to the end user.

<div style="text-align: center; margin: 15px 0;">

<img src="image/img_0007.jpeg" style="width: 100%; max-width: 100%; height: auto;" alt="Fig. 7: End-to-End Inference Latency Breakdown">

<p style="font-size: 9pt; font-weight: bold; margin-top: 5px;">Fig. 7: End-to-End Inference Latency Breakdown</p>
</div>

#### E. Case Study
To illustrate system behavior on an algospeak input, consider the following representative example:
- **Input (raw)**: "[pill emoji] marijuana available cheap"
- **After normalization**: "pill marijuana available cheap"
- **DistilBERT output**: $P_{text} = 0.91$ (High Risk)
- **MobileNet output**: $P_{image} = 0.89$ (High Risk)
- **Fused risk score**: $S = 0.7 \times 0.91 + 0.3 \times 0.89 = 0.904$
- **Intervention**: Content blurred by browser extension.

This example illustrates the system's ability to decode emoji-encoded algospeak and apply immediate, targeted intervention at the client side.

#### F. Real-World Client-Side Intervention Demonstration
To evaluate the integration of the Chrome extension with the live FastAPI inference server, an end-to-end simulation was conducted using a test suite comprising safe medical information posts and obfuscated drug sales listings. Fig. 9 illustrates the Chrome extension's client-side visual masking overlays in the browser.

<div style="text-align: center; margin: 15px 0;">

<img src="image/extension_test_screenshot.png" style="width: 100%; max-width: 100%; height: auto;" alt="Fig. 9: Extension Client-Side Content Masking Overlay">

<p style="font-size: 9pt; font-weight: bold; margin-top: 5px;">Fig. 9: DrugGuard Client-Side Blur Overlay in Action</p>
</div>

## VIII. PLAGIARISM REPORT

The project titled 'Algospeak-Resilient Drug Trafficking Detection Using Transformer-Based Machine Learning and a Browser Extension' was evaluated for originality using an online plagiarism detection tool.

**Tool Used**: Online Plagiarism Checker ([plagiarismremover.net](https://www.plagiarismremover.net/))

**Result Summary**:
- **Plagiarized Content**: 0%
- **Unique Content**: 100%

The analysis confirms a high degree of originality and adherence to academic integrity standards, with the work presented being the authors' own contribution.

## IX. CONCLUSION

This paper presented a real-time, algospeak-resilient drug trafficking detection system that integrates transformer-based NLP, CNN-based image classification, and client-side browser intervention within a unified operational framework. The proposed system addresses the fundamental limitations of existing content moderation approaches — namely, their inability to decode evolving obfuscation patterns and their lack of real-time, user-level intervention capability.

A semantic normalization layer was introduced to systematically decode emojis, slang, and leetspeak prior to model inference, yielding a 7-percentage-point accuracy improvement and a 0.07 F1-score gain over the unnormalized baseline. A fine-tuned DistilBERT model and a MobileNet-based CNN classify text and image inputs respectively, with their outputs fused via a weighted scoring mechanism. The resulting Chrome extension delivers real-time content intervention — blurring or blocking high-risk content — at an end-to-end latency of 250-300 ms, demonstrating feasibility for real-world deployment. Experimental results confirm that the full multimodal system achieves 94% accuracy and an F1-score of 0.92, outperforming all single-modality baselines.

Despite these contributions, the system faces inherent challenges in handling highly ambiguous content and continuously evolving slang patterns not captured by the current static normalization lexicon. Future work will explore adaptive normalization through continual learning, dynamic lexicon expansion via community feedback mechanisms, and extension to additional modalities such as audio and video to further strengthen detection robustness in adversarial conditions.

## REFERENCES

1. K. Alfatmi, A. Borse, R. Girase, S. Bagul, A. Patil, and M. Shahade, "LLM-Empowered Detection of Illicit Messages on Social Networks," *Journal of Cybersecurity*, vol. 11, no. 1, pp. 102–115, 2025. [Online]. Available: https://academic.oup.com/cybersecurity
2. K. Alfatmi, A. Borse, R. Girase, S. Bagul, A. Patil, and M. Shahade, "Narcotrace: Advanced Detection System for Social Media-Based Drug Trafficking," in *Proceedings of the 3rd International Conference on Futuristic Technology (INCOFT 2025)*, SCITEPRESS, 2025, pp. 312–319. [Online]. Available: https://www.scitepress.org/PublishedPapers/2025/136592/
3. M. Song, E. Jang, J. Kim, and S. Shin, "Covering Cracks in Content Moderation: Delexicalized Distant Supervision for Illicit Drug Jargon Detection," in *Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD '25)*, ACM, 2025. [Online]. Available: https://dl.acm.org/doi/abs/10.1145/3690624.3709183
4. M. Song, E. Jang, J. Kim, and S. Shin, "Delexicalized Distant Supervision for Illicit Drug Jargon Detection (JEDIS)," *arXiv preprint arXiv:2503.14926*, 2025. [Online]. Available: https://arxiv.org/abs/2503.14926
5. M. Ahmad, F. Ullah, M. Usman, I. Batyrshin, and G. Sidorov, "SABIA: An AI-Powered Tool for Detecting Opioid-Related Behaviors on Social Media," *arXiv preprint arXiv:2408.09321*, 2024. [Online]. Available: https://arxiv.org/abs/2408.09321
6. J. Li, Q. Xu, N. Shah, and T. K. Mackey, "A Machine Learning Approach for the Detection and Characterization of Illicit Drug Dealers on Instagram: Model Evaluation Study," *Journal of Medical Internet Research*, vol. 21, no. 6, p. e13803, 2019. [Online]. Available: https://doi.org/10.2196/13803
7. C. Hu, B. Liu, X. Li, Y. Ye, and M. Yin, "Knowledge-Prompted ChatGPT: Enhancing Drug Trafficking Detection on Social Media," *Information & Management*, vol. 61, no. 6, p. 104010, 2024. [Online]. Available: https://doi.org/10.1016/j.im.2024.104010
8. C. Hu, M. Yin, B. Liu, X. Li, and Y. Ye, "Identifying Illicit Drug Dealers on Instagram with Large-scale Multimodal Data Fusion," *ACM Transactions on Intelligent Systems and Technology*, vol. 12, no. 5, pp. 1–22, 2021. [Online]. Available: https://doi.org/10.1145/3472957
9. S. N. Sivadarshini, R. M. V, S. V. R, and S. Baskaran, "Cyberbullying Detection in Heterogeneous Data Streams Using Pytesseract OCR and HateBERT: A Cross-Modal Approach for Text, Image, and Emoji Interpretation," *International Journal for Research in Applied Science & Engineering Technology (IJRASET)*, vol. 13, no. 4, pp. 841–848, 2025. [Online]. Available: https://doi.org/10.22214/ijraset.2025.68819
10. T. Hayashi and R. Nojima, "Detecting Illicit Drug Trade on SNS through Image Classification and Real-Time Monitoring," in *Proceedings of the 13th International Symposium on Computing and Networking (CANDAR)*, IEEE, 2025, pp. 112–119. [Online]. Available: https://doi.org/10.1109/CANDAR65168.2025.00022
11. U.S. Drug Enforcement Administration (DEA), "Emoji Drug Code: Decoded — The Hidden Language of Illicit Drugs," DEA Official Resources, 2021. [Online]. Available: https://www.dea.gov/onepill
12. F. Jahanbakhsh, A. X. Zhang, A. J. Berinsky, G. Pennycook, D. G. Rand, and D. R. Karger, "Exploring Lightweight Interventions at Posting Time to Reduce the Sharing of Misinformation on Social Media," *Proceedings of the ACM on Human-Computer Interaction (CSCW)*, vol. 5, no. CSCW1, pp. 1–32, 2021. [Online]. Available: https://doi.org/10.1145/3449092
13. S. Park, S. Lee, H. Kim, and J. Choi, "DIY-MOD: Empowering Users with Real-Time, Client-Side Visual and Textual Content Transformation for Personalized Content Moderation," in *Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems (CHI '24)*, ACM, 2024, pp. 1–18. [Online]. Available: https://doi.org/10.1145/3613904.3642431
14. R. Gautam, Kartik, S. Singh, S. Srivastava, and D. Parihar, "Investigating Drug Trafficking Using Encrypted Messengers: NLP and Data Analysis Approaches in Cybersecurity," in *Proceedings of the 2nd International Conference on Information Technology (INCOFT)*, SCITEPRESS, 2025, pp. 405–412. [Online]. Available: https://www.scitepress.org/PublishedPapers/2025/139431/

</div>