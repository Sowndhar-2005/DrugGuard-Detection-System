
## Algospeak-Resilient Drug Trafficking Detection Using Transformer-Based


## Machine Learning and a Browser Extension


**Agalya M,  Kalaipriya S,  Sowndhar A, Er.K.Daniel Raj**

Department of CSE (AI & ML)  
Kalaignarkarunanidhi Institute of Technology, Coimbatore, India  
Abstract – The rapid proliferation of social media  
platforms has significantly expanded the attack surface for  
illicit drug trafficking, wherein dealers employ obfuscated  
communication strategies collectively termed algospeak  
comprising emojis, abbreviations, leetspeak, and coded  
terminology to evade automated moderation systems.  
Existing detection approaches, primarily reliant on keyword  
filtering and post-hoc machine learning analysis, are  
inadequate for identifying evolving obfuscation patterns or  
enabling real-time intervention. This paper proposes an  
algospeak-resilient, multimodal drug trafficking detection  
system that integrates transformer-based natural language  
processing, convolutional neural network-based image  
classification, and client-side browser intervention. A  
semantic normalization layer is introduced to systematically  
decode emojis, slang, and obfuscated text into structured  
representations amenable to downstream model inference.  
Normalized text is classified using a fine-tuned DistilBERT  
model,  
while  
visual  
content  
is  
analyzed  
via  
a  
MobileNet-based CNN. A weighted fusion mechanism  
combines both modality outputs to compute a unified risk  
score, upon which a Chrome extension performs real-time  
content blurring or blocking. Evaluated on the Reddit Drug  
Corpus and a manually annotated dataset encompassing  
algospeak-heavy samples, the proposed multimodal system  
achieves 94% accuracy and an F1-score of 0.92,  
outperforming  
all  
single-modality  
baselines,  
while  
maintaining an end-to-end response latency of 250-300 ms  
suitable for real-time deployment.  
Keywords — Drug Trafficking Detection, Algospeak,  
Transformer Models, DistilBERT, Multimodal Learning,  
Semantic Normalization, Browser Extension, Real-Time  
Intervention.  

**I. INTRODUCTION**

The  
rapid  
expansion of social media and online  
communication platforms has fundamentally altered the  
operational landscape of illicit drug trafficking. Platforms  
including forums, encrypted messaging applications, and  
open social networks are increasingly exploited by  
traffickers to advertise, coordinate, and facilitate the  
distribution of controlled substances. Unlike traditional  
offline channels, these digital environments offer anonymity,  
global reach, and near-zero operational cost, rendering  
detection  
and  
law  
enforcement  
substantially  
more  
challenging.  
To circumvent automated content moderation systems,  
traffickers  
have  
developed  
sophisticated  
linguistic  
obfuscation  
strategies  
collectively  
referred  
to  
as  
"algospeak." These strategies encompass the deliberate use  
of emojis as symbolic substitutes (e.g., 💊 emoji to represent  
controlled substances), abbreviated or fragmented spellings  
(e.g., "d r u g s"), leetspeak encodings (e.g., "dr*gs"), and  
domain-specific coded terminology that continuously  
evolves.  
Such  
techniques  
systematically  
undermine  
conventional keyword-based detection pipelines, which lack  
the  
semantic  
flexibility  
required  
to  
interpret  
context-dependent obfuscation.  
Existing approaches to automated drug trafficking detection  
can be broadly categorized into keyword-based filtering and  
machine  
learning-based  
classification.  
While  
recent  
transformer-based models such as BERT have significantly  
advanced contextual text understanding, the majority of  
deployed systems operate at the platform level as post-hoc  
analyzers — processing content only after it has been  
published. This reactive architecture introduces an inherent  
temporal gap between content publication and moderation  
action, during which harmful content remains accessible to  
users. Furthermore, these systems are typically unimodal,  
failing to exploit the visual signals (e.g., images of  
substances or paraphernalia) that frequently accompany  
drug-related posts .  
To address these limitations, this paper proposes a real-time,  
algospeak-resilient drug trafficking detection system that  
unifies natural language processing, computer vision, and  
browser-level intervention within a single operational  
framework. The system introduces a semantic normalization  
layer that transforms emojis, slang, and obfuscated text into  
standardized  
representations,  
thereby  
improving  
the  
interpretability of model inputs. Normalized text is  
subsequently analyzed using a fine-tuned DistilBERT  
classifier, while accompanying images are assessed using a  
MobileNet-based CNN. A weighted fusion strategy  
integrates both modality outputs into a unified risk score,  
which drives immediate intervention by a Chrome browser  
extension capable of blurring, blocking, or flagging harmful  
content at the client side.  
The principal contributions of this work are as follows:  
1.​  
A real-time, browser-integrated detection and  
intervention system for drug trafficking content  
operating at the user level.  


---

2.​  
A semantic normalization layer for structured  
decoding of algospeak, including emojis, slang, and  
leetspeak.  
3.​  
A multimodal detection framework combining  
DistilBERT-based NLP with MobileNet-based  
image classification.  
4.​  
A lightweight, scalable architecture validated for  
real-time deployment with sub-300 ms end-to-end  
latency.  

**II. RELATED WORK**

Detecting illicit drug trafficking on online platforms has  
garnered significant research attention due to the rising  
misuse of social media and encrypted communication  
channels[1][3]. Existing research can be broadly grouped  
into transformer-based detection systems, algospeak and  
jargon analysis, multimodal learning approaches, and  
browser-based intervention techniques.  
A. Transformer-Based Drug Trafficking Detection  
Recent advances in natural language processing have  
enabled the application of large-scale transformer models to  
the problem of illicit content detection. The Narcotrace  
framework [2] is among the earliest systems to leverage  
BERT for classifying drug-related posts on social media,  
demonstrating that contextual semantic representations  
substantially outperform traditional bag-of-words and  
keyword-matching approaches. Building on this, Hu et al.  
[7] proposed a knowledge-prompted adaptation of ChatGPT  
that incorporates domain-specific priors to improve the  
detection of indirect and ambiguous drug-related language.  
While  
these  
methods  
achieve  
strong  
classification  
performance, they are architecturally confined to backend  
deployment and offer no mechanism for real-time, user-level  
intervention.  
B. Algospeak and Jargon Detection  
The emergence of algospeak has introduced a distinct  
challenge for content moderation systems. Traffickers  
systematically employ emojis, phonetic abbreviations, and  
intentionally obfuscated spellings to bypass automated  
filters [11]. Song et al. [4][5] proposed the JEDIS  
framework, which applies delexicalized distant supervision  
to identify latent drug-related terminology in informal online  
conversations. By combining contextual token embeddings  
with word-attribute-level analysis, JEDIS demonstrates  
effective generalization to previously unseen slang on  
platforms such as Reddit. Ahmad et al. [6] further explored  
context-aware transformer models for analyzing informal  
and  
semi-encrypted  
communication,  
confirming  
that  
semantic context is critical for decoding obfuscated intent.  
However, the majority of these approaches are confined to  
text-based analysis and do not incorporate explicit  
normalization techniques that convert emojis and slang into  
structured token sequences prior to model inference.  
C. Multimodal Detection Approaches  
Drug trafficking content frequently combines textual and  
visual elements, including images of controlled substances,  
packaging, or associated paraphernalia. To exploit this,  
multimodal learning frameworks have been proposed that  
jointly process text and image inputs [9]. Studies integrating  
CNNs with transformer-based encoders have demonstrated  
that  
cross-modal  
fusion  
consistently  
outperforms  
single-modality classifiers on ambiguous or partially  
obfuscated content. Hayashi and Nojima [10] further  
explored image classification combined with real-time social  
network  
monitoring,  
achieving  
improved  
recall  
on  
visually-dominated posts. Despite these advances, existing  
multimodal systems are predominantly designed for offline  
batch analysis and have not been optimized for low-latency,  
real-time deployment.  
D. Browser-Based Content Intervention  
Browser extensions have been explored as a complementary  
mechanism for real-time content modification at the client  
side,  
leveraging  
Document  
Object  
Model  
(DOM)  
monitoring to dynamically alter or suppress webpage  
content as it is rendered [12][13]. Jahanbakhsh et al. [12]  
demonstrated the feasibility of real-time DOM overlays for  
user signaling via browser extensions. However, existing  
browser-based approaches are predominantly rule-based and  
lack integration with learned semantic models, limiting their  
capacity to detect complex patterns such as algospeak or  
multimodal trafficking cues.  
E. Research Gap  
The literature reveals a consistent bifurcation: systems that  
achieve high detection accuracy through advanced modeling  
are deployed as offline, platform-level analyzers, while  
systems that enable real-time intervention rely on shallow,  
rule-based logic. No existing solution integrates (1) robust  
semantic normalization of algospeak, (2) multimodal  
detection leveraging both text and image modalities, and (3)  
real-time,  
user-level  
intervention  
within  
a  
unified  
operational framework. The present work directly addresses  
this gap.  

**III. SYSTEM ARCHITECTURE**

A. Architectural Overview  
The proposed system adopts a client-server architecture  
designed to detect and suppress drug-related content on web  
pages in real time. The architecture decouples browser-side  
content extraction and intervention from server-side  
machine learning inference, enabling independent scalability  
of each component. The system comprises three primary  
modules :  
(i) the Browser Extension (Client Layer)  
(ii) the Machine Learning Backend  
(iii) the Decision and Intervention Module  


---

Fig. 1: Architectural Diagram  
Upon page load, the browser extension extracts visible text  
and image data from the DOM and transmits it securely to  
the  
backend  
server.  
The  
server  
applies  
semantic  
normalization followed by parallel text and image  
classification, producing a unified risk score. This score is  
returned to the extension, which executes the appropriate  
intervention action directly within the browser.  
B. Browser Extension (Client Layer)  
The browser extension is implemented using the Chrome  
Extension Manifest V3 API and serves as the interface  
between the user's browsing session and the detection  
backend. A MutationObserver instance is registered against  
the DOM to continuously monitor structural changes,  
enabling detection of dynamically loaded content such as  
infinite-scroll posts and asynchronously rendered comments  
without requiring page reloads. The extension performs the  
following operations:  
•​  
Extraction of visible text nodes from the DOM.  
•​  
Identification and retrieval of image source URLs.  
•​  
Lightweight HTML sanitization to remove  
non-content markup.  
•​  
Secure transmission of extracted data to the  
backend via HTTPS POST requests.  
•​  
Rendering of intervention actions, including  
semi-transparent blur overlays and warning  
banners, upon receipt of high-risk scores.  
C. Machine Learning Backend  
The backend server is implemented using the FastAPI  
framework in Python, selected for its asynchronous request  
handling, low overhead, and native compatibility with the  
Hugging  
Face  
Transformers  
and  
TensorFlow/Keras  
ecosystems. The backend exposes a RESTful inference  
endpoint that accepts multimodal inputs, executes the  
detection pipeline, and returns a structured JSON response  
containing the risk score and recommended action. Both  
models are pre-loaded into memory at server initialization to  
eliminate per-request model loading latency. The backend  
inference pipeline consists of four sequential stages:  
1.​  
Semantic normalization of input text.  
2.​  
Text classification via a fine-tuned DistilBERT  
model.  
3.​  
Image classification via a MobileNet-based CNN.  
4.​  
Weighted fusion of model outputs to compute the  
unified risk score.  
D. Semantic Normalization Layer  
The semantic normalization layer constitutes a critical  
preprocessing stage responsible for transforming obfuscated,  
informal, and emoji-encoded input text into structured  
representations suitable for downstream NLP inference. The  
layer  
applies  
three  
sequential  
transformations:  
(1)  
emoji-to-text mapping, wherein Unicode emoji characters  
are replaced with their semantic textual equivalents (e.g., the  
pill emoji maps to "pill"); (2) slang decoding, wherein a  
domain-specific lexicon maps coded drug-related terms to  
their standard equivalents; and (3) noise removal, wherein  
leetspeak encodings and irregular character spacing (e.g.,  
"dr*gs", "d r u g s") are normalized to canonical token  
forms. This preprocessing step substantially improves the  
ability of the DistilBERT model to capture contextual  
semantics in obfuscated inputs.  
E. Decision and Intervention Module  
The decision module computes a final risk score by fusing  
the probabilistic outputs of the text and image classifiers  
using a weighted linear combination (detailed in Section  
IV-E). The resulting score is compared against predefined  
thresholds to determine the appropriate intervention: scores  
below 0.4 indicate low risk and require no action; scores  
between 0.4 and 0.7 indicate medium risk and trigger a  
warning overlay; scores of 0.7 and above indicate high risk  
and initiate content blurring or full blocking. These  
threshold values were determined empirically through  
validation set analysis to balance detection sensitivity  
against false positive rate.  
F. System Workflow Summary  
The end-to-end system workflow proceeds as follows:  
1.​  
Webpage content is monitored and extracted by the  
browser extension via DOM traversal.  
2.​  
Extracted text and image data are transmitted  
securely to the FastAPI backend.  
3.​  
Semantic normalization is applied to the raw text  
input.  
4.​  
Parallel text and image classification is performed  
by DistilBERT and MobileNet respectively.  
5.​  
A unified risk score is computed via weighted  
fusion.  
6.​  
The browser extension applies the appropriate  
intervention action based on threshold comparison.  

**IV. METHODOLOGY**

A. Input Processing and Data Extraction  
The system ingests raw text and image data extracted from  
web pages via the browser extension. Input text may include  
user-generated posts and comments containing informal  
language, domain-specific slang, emoji sequences, and  
deliberate character-level obfuscation. Images may depict  


---

controlled  
substances,  
packaging,  
or  
associated  
paraphernalia. Due to the noisy and unstructured nature of  
these inputs, preprocessing is applied prior to model  
inference.  
B. Semantic Normalization  
Let the raw input text be denoted as T_raw. The normalized  
representation T_norm is obtained via:  
T_norm  =  f_norm( T_raw )   ... (1)  
where f_norm( . ) denotes a composite normalization  
function integrating emoji mapping, slang decoding, and  
noise removal mechanisms such as leetspeak normalization  
and spacing correction.  
Fig. 2 depicts the semantic normalization pipeline, wherein  
raw, obfuscated inputs are progressively transformed into  
structured textual representations. By enforcing consistency  
across diverse surface forms, this process enables the model  
to capture underlying semantic intent and improves  
robustness to previously unseen algospeak patterns.  
Fig. 2 : Semantic Normalization  
C. Text Classification Using DistilBERT  
The normalized text T_norm is passed to a fine-tuned  
DistilBERT model. DistilBERT is a distilled variant of  
BERT that retains approximately 97% of BERT's language  
understanding performance while reducing parameter count  
by 40% and inference time by approximately 60%, making  
it well-suited for latency-constrained deployment. The  
model produces a drug-related content probability score  
P_text in [0, 1] via a binary classification head with sigmoid  
activation applied over the [CLS] token representation.  
D. Image Classification Using MobileNet-Based CNN  
Visual inputs are analyzed using a MobileNet-based  
convolutional neural network. MobileNet's depthwise  
separable convolution architecture reduces computational  
cost significantly compared to standard convolutions while  
maintaining competitive classification accuracy, making it  
appropriate for real-time inference. An input image I is  
passed through the CNN to produce a classification  
probability P_image in [0, 1] representing the likelihood of  
drug-related visual content.  
E. Multimodal Fusion Strategy  
To leverage the complementary discriminative power of  
textual and visual modalities, the system employs a  
weighted linear fusion strategy. The unified risk score S is  
computed as:  
S  =  alpha * P_text  +  ( 1 - alpha ) *  
P_image   ... (2)  
where alpha = 0.7 is a weighting coefficient determined  
empirically through validation set optimization, reflecting  
the relatively higher discriminative contribution of textual  
features in the Reddit-derived dataset. This formulation  
allows the risk score to remain sensitive to visual cues even  
when textual content is minimal or absent (Fig. 3).  
Fig. 3 : Multimodal Fusion Strategy  
F. Decision Thresholding  
The computed risk score S is mapped to an intervention  
action using the following threshold policy, derived from  
precision-recall trade-off analysis on the validation set:  
•​  
S < 0.4:  Content classified as safe; no action taken.  
•​  
0.4 <= S < 0.7:  Content classified as suspicious;  
warning overlay displayed.  
•​  
S >= 0.7:  Content classified as high-risk; content  
blurred or blocked.  

**V. TECHNICAL IMPLEMENTATION**

A. Backend Development  
The backend is implemented with FastAPI in Python,  
selected for its asynchronous request handling, low latency  
overhead, and native compatibility with the Hugging Face  


---

Transformers and TensorFlow/Keras ecosystems. The  
backend exposes RESTful APIs that receive multimodal  
data from the browser extension, execute the detection  
pipeline, and return structured JSON responses. The text  
processing module uses the Hugging Face Transformers  
library with a pre-trained DistilBERT model fine-tuned on  
drug-related corpora; the model is pre-loaded into server  
memory at startup to minimize per-request inference latency.  
The  
image  
classification  
module  
employs  
a  
MobileNet-based  
neural  
network  
implemented  
in  
TensorFlow/Keras, optimized through parameter reduction  
and  
depthwise  
separable convolutions for real-time  
throughput.  
B. Browser Extension  
The frontend is implemented as a Google Chrome extension  
using Manifest V3. A MutationObserver API instance is  
registered against the page DOM to monitor structural  
changes in real time, enabling detection of asynchronously  
loaded content without page reloads. The extension extracts  
visible text nodes and image sources, transmits the sanitized  
data to the backend via HTTPS, receives the risk score and  
recommended action, and renders visual interventions  
including blur overlays and warning banners directly within  
the page DOM.  
C. Communication Protocol  
The  
browser  
extension  
and  
backend  
communicate  
exclusively via HTTPS using JSON-encoded payloads. Each  
request contains the extracted text content and image URLs  
or base64-encoded image data. Each response contains a  
normalized risk score in the range [0, 1] and a recommended  
action label (safe, warn, or block). This structured protocol  
ensures minimal serialization overhead and seamless  
integration between the client and server components.  
D. Real-Time Processing Optimization  
To satisfy real-time responsiveness requirements, the  
following optimizations are applied: models are pre-loaded  
into memory at server startup to eliminate initialization  
latency; FastAPI's asynchronous request handling enables  
concurrent inference without thread blocking; lightweight  
architectures  
(DistilBERT  
and  
MobileNet)  
constrain  
per-request computation; and MutationObserver is used for  
efficient incremental DOM scanning rather than full-page  
polling. These measures collectively enable the system to  
process the majority of requests within the 250-300 ms  
end-to-end latency target.  
E. Deployment Environment  
The  
system  
supports  
deployment  
on  
both  
cloud  
infrastructure (e.g., AWS EC2, Google Cloud Run) and local  
servers. The backend is containerizable and designed for  
independent horizontal scaling. The browser extension is  
distributed directly to the user's Chrome browser and  
communicates with the configured backend endpoint.  
F. Security Considerations  
Security is enforced at multiple layers: all data transmission  
between the extension and backend is encrypted via  
HTTPS/TLS; server-side input validation is applied to  
prevent malicious payloads; and backend API access is  
controlled to prevent unauthorized inference requests.  

**VI. DATASET AND TRAINING**

A. Dataset Description  
The system is trained and evaluated using a combination of  
large-scale public data and manually curated samples  
designed to capture both explicit and algospeak-encoded  
drug-related content (Fig. 4).  
Reddit Drug Corpus: A large-scale dataset comprising  
approximately 1.27 million posts sourced from drug-related  
subreddits. The corpus encompasses a wide range of content  
including both licit and illicit discussions, informal  
language, and domain-specific slang, providing broad  
coverage of real-world linguistic variation.  
Manually Annotated Dataset: To improve detection of  
novel and evolving algospeak patterns, a supplementary  
dataset was constructed by collecting and labeling social  
media samples. This dataset includes positive-class samples  
(drug-related posts), negative-class samples (non-drug  
content), and samples containing emojis, abbreviations, and  
coded language. Human annotators verified all labels to  
ensure accuracy and real-world alignment.  
Fig. 4: Dataset Composition  
B. Data Preprocessing  
Prior to training, all data undergoes the following  
preprocessing steps:  
•​  
Text inputs are processed through the semantic  
normalization layer to handle emojis, slang, and  
obfuscated characters.  
•​  
Normalized text is tokenized using the DistilBERT  
WordPiece tokenizer with a maximum sequence  
length of 512 tokens.  


---

•​  
Duplicate and near-duplicate entries are removed to  
prevent data leakage.  
•​  
Images are resized to 224x224 pixels and  
normalized to the input distribution expected by  
MobileNet.  
C. Data Splitting  
The dataset is partitioned using stratified sampling to  
preserve class distribution across splits: Training Set (70%),  
Validation Set (15%), and Test Set (15%). Stratified  
sampling  
ensures  
that  
each  
partition  
contains  
a  
representative  
proportion  
of  
drug-related  
and  
non-drug-related samples (Fig. 5)  
Fig. 5: Dataset Split Distribution  
D. Training Configuration  
Text Model (DistilBERT): The model is fine-tuned using  
Binary Cross-Entropy loss with the Adam optimizer  
(learning rate: 2e-5, batch size: 16) for 5-10 epochs until  
validation loss convergence.  
Image Model (MobileNet): The MobileNet-based classifier  
is trained using Binary Cross-Entropy loss with the Adam  
optimizer (batch size: 32) for 10-15 epochs. Data  
augmentation  
techniques  
including  
random  
rotation,  
horizontal flipping, and zoom are applied to improve  
generalization to unseen image variations.  
E. Handling Class Imbalance  
To  
address  
the  
inherent  
class  
imbalance  
between  
drug-related and non-drug-related samples, the following  
strategies are applied: class-weighted loss functions to  
penalize  
misclassification  
of  
the  
minority  
class;  
oversampling of minority-class training instances; and  
image-level data augmentation to increase effective sample  
count for underrepresented visual categories.  
F. Evaluation Metrics  
Model performance is assessed using the following standard  
classification  
metrics:  
Accuracy  
(overall  
prediction  
correctness), Precision (fraction of positive predictions that  
are correct), Recall (fraction of actual positives correctly  
identified), and F1-Score (harmonic mean of precision and  
recall). These metrics collectively provide a robust  
assessment of model performance under class imbalance  
conditions.  

**VII. RESULTS AND EVALUATION**

A. Quantitative Results  
Table I presents the performance comparison between  
single-modality  
baseline  
models  
and  
the  
proposed  
multimodal system. All models are evaluated on the  
held-out test set under identical experimental conditions.  
TABLE I  
Performance Comparison of Detection Models  

**Model**


**Accuracy Precision Recall**


**F1-Score**

CNN  
(Image  
Only)  
88%  
0.85  
0.87  
0.86  
BERT  
(Text  
Only)  
90%  
0.88  
0.89  
0.88  
DistilB  
ERT  
(Propos  
ed —  
Text)  
92%  
0.90  
0.91  
0.90  
Multim  
odal  
(Propos  
ed —  
Full)  
94%  
0.92  
0.93  
0.92  
B. Performance Analysis  
The DistilBERT model achieves higher accuracy than the  
CNN-only baseline (92% vs. 88%) due to its capacity to  
capture long-range contextual dependencies in text, which  
are critical for interpreting implicit or indirect drug  
references. However, relying solely on textual features  
introduces vulnerability to posts where illicit intent is  
conveyed primarily through visual content with minimal  
descriptive text. The multimodal system addresses this by  
integrating MobileNet-based image classification, yielding  
an additional 2-percentage-point improvement in accuracy  
(94%) and a corresponding F1-score gain to 0.92. This result  
confirms that cross-modal fusion provides complementary  
discriminative signal beyond what either modality achieves  
independently.  
C. Impact of Semantic Normalization (Ablation Study)  


---

To quantify the contribution of the semantic normalization  
layer, an ablation study was conducted by evaluating the  
DistilBERT  
text  
classifier  
with  
and  
without  
the  
normalization preprocessing stage. Without normalization,  
the model achieves 85% accuracy and an F1-score of 0.83.  
Upon applying the full normalization pipeline, accuracy  
improves to 92% and F1-score to 0.90 — representing a  
7-percentage-point gain in accuracy and a 0.07 improvement  
in  
F1-score.  
These  
results  
confirm  
that  
semantic  
normalization is a functionally critical component that  
enables the model to generalize across previously unseen  
algospeak patterns not encountered during training ( Fig. 6 ).  
Fig. 6: Effect of Semantic Normalization  
D. Real-Time Performance  
The system was evaluated for inference latency under  
simulated real-world load conditions. Average per-request  
processing times are as follows: text normalization and  
DistilBERT inference: ~120 ms; MobileNet image  
inference: ~150 ms; total end-to-end response time  
(including network round-trip): ~250-300 ms. These figures  
demonstrate that the system satisfies real-time  
responsiveness requirements without perceptible latency to  
the end user.  
Fig. 7: End-to-End Inference Latency Breakdown  
E. Case Study  
To illustrate system behavior on an algospeak input,  
consider the following representative example:  
•​  
Input (raw): "[pill emoji] marijuana available  
cheap"  
•​  
After normalization: "pill marijuana available  
cheap"  
•​  
DistilBERT output: P_text = 0.91 (High Risk)  
•​  
MobileNet output: P_image = 0.89 (High Risk)  
•​  
Fused risk score: S = 0.7 x 0.91 + 0.3 x 0.89 =  
0.904  
•​  
Intervention: Content blurred by browser extension.  
This example illustrates the system's ability to decode  
emoji-encoded algospeak and apply immediate, targeted  
intervention at the client side.  

**VIII. PLAGIARISM REPORT**

The project titled 'Algospeak-Resilient Drug Trafficking  
Detection Using Transformer-Based Machine Learning and  
a Browser Extension' was evaluated for originality using an  
online plagiarism detection tool.  
Tool  
Used:  
Online  
Plagiarism  
Checker  
( https://www.plagiarismremover.net/ )  
Result Summary:  
•​  
Plagiarized Content: 0%  
•​  
Unique Content: 100%  
The analysis confirms a high degree of originality and  
adherence to academic integrity standards, with the work  
presented being the authors’ own contribution.  

**IX. CONCLUSION**

This paper presented a real-time, algospeak-resilient drug  
trafficking  
detection  
system  
that  
integrates  
transformer-based NLP, CNN-based image classification,  
and client-side browser intervention within a unified  
operational framework. The proposed system addresses the  
fundamental limitations of existing content moderation  
approaches — namely, their inability to decode evolving  
obfuscation patterns and their lack of real-time, user-level  
intervention capability.  
A semantic normalization layer was introduced to  
systematically decode emojis, slang, and leetspeak prior to  
model inference, yielding a 7-percentage-point accuracy  
improvement  
and  
a 0.07 F1-score gain over the  
unnormalized baseline. A fine-tuned DistilBERT model and  
a MobileNet-based CNN classify text and image inputs  
respectively, with their outputs fused via a weighted scoring  
mechanism. The resulting Chrome extension delivers  
real-time content intervention — blurring or blocking  
high-risk content — at an end-to-end latency of 250-300 ms,  
demonstrating  
feasibility  
for  
real-world  
deployment.Experimental results confirm that the full  


---

multimodal system achieves 94% accuracy and an F1-score  
of 0.92, outperforming all single-modality baselines. Despite  
these contributions, the system faces inherent challenges in  
handling highly ambiguous content and continuously  
evolving slang patterns not captured by the current static  
normalization lexicon. Future work will explore adaptive  
normalization through continual learning, dynamic lexicon  
expansion via community feedback mechanisms, and  
extension to additional modalities such as audio and video to  
further strengthen detection robustness in adversarial  
conditions.  

**REFERENCES**

[1]  K. Alfatmi et al., "LLM-Empowered Detection of Illicit  
Messages on Social Networks," Journal of Cybersecurity,  
2025.  
[2]  K. Alfatmi et al., "Narcotrace: Advanced Detection System for  
Social Media-Based Drug Trafficking," Proc. INCOFT, 2025.  
[3]  M. Song et al., "Covering Cracks in Content Moderation:  
Delexicalized Distant Supervision for Illicit Drug Jargon  
Detection," Proc. ACM Conf. on Content Moderation, 2025.  
[4]  M. Song et al., "Delexicalized Distant Supervision for Illicit  
Drug Jargon Detection (JEDIS)," arXiv:2503.14926, 2025.  
[5]  M. Ahmad et al., "SABIA: An AI-Powered Tool for Detecting  
Opioid-Related Behaviours on Social Media," arXiv, 2025.  
[6]  J. Li et al., "A Machine Learning Approach for the Detection  
of Illicit Drug Dealers on Instagram," Proc. WWW, 2019.  
[7]  C. Hu, B. Liu, X. Li, and Y. Ye, "Knowledge-Prompted  
ChatGPT: Enhancing Drug Trafficking Detection on Social  
Media," Information & Management, vol. 61, no. 1, 2024.  
doi:10.1016/j.im.2024.104010.  
[8]  C. Hu et al., "Knowledge-Prompted ChatGPT: Enhancing Drug  
Trafficking Detection on Social Media," Information &  
Management, vol. 61, no. 1, 2024.  
doi:10.1016/j.im.2024.104010.  
[9] P. Patel et al., "A Cross-Modal Approach for Text, Image, and  
Emoji Interpretation," IJRASET, 2023.  
[10] T. Hayashi and R. Nojima, "Detecting Illicit Drug Trade on  
SNS through Image Classification and Real-Time  
Monitoring," IEEE, 2024.  
[11] DEA, "Drug Emoji Slang: Decoded — The Hidden Language  
of Illicit Drugs," Lake Point Recovery, 2025.  
[12] M. Jahanbakhsh et al., "Real-Time DOM Overlays and User  
Signalling via Browser Extensions," 2024.  
[13] Imagga Team, "Safe Browsing with Content Moderation  
Chrome Extension," Imagga Blog, 2025.  
[14] R. Gautam et al., "Investigating Drug Trafficking Using  
Encrypted Messengers," 2025.  


---
