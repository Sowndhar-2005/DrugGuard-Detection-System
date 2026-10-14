# FINAL SUBMISSION CHECKLIST & VERIFICATION REPORT

**Manuscript Title:** *Algospeak-Resilient Detection of Illicit Drug-Related Content Using Transformer-Based Machine Learning and a Browser Extension*  
**Files Generated & Ready for Submission:**
- 📄 **DOCX Draft:** [`DrugGuard_Paper_Final_Draft.docx`](file:///d:/project/DrugGuard-Detection-System/DrugGuard_Paper_Final_Draft.docx) (Complete Word manuscript with all 9 figures, tables, and sections)
- 📑 **PDF Draft:** [`DrugGuard_Paper_Final_Draft.pdf`](file:///d:/project/DrugGuard-Detection-System/DrugGuard_Paper_Final_Draft.pdf) (High-resolution publication PDF with embedded figures)

---

## 1. Resolved Inconsistencies & Verifications (P0 & P1)

| Item | Discrepancy Found in Prior Draft | Resolution in Final Manuscript | Status |
|---|---|---|:---:|
| **Title Scope** | Titled "Drug Trafficking" | Retitled to **"Detection of Illicit Drug-Related Content"** to match the actual classification task. | ✅ Fixed |
| **Multimodal vs. Text-Only Claim** | Claimed multimodal (94.20%) "outperforms text-only" (96.80%) | Removed contradictory claim. Accurately clarified: DistilBERT excels on text posts (**96.80%**), while Multimodal (**94.20%**) beats vision-only (**84.67%**) and is essential to catch image-only/flyer posts where text models are blind. | ✅ Fixed |
| **Dataset Split** | Conflicted between 70/15/15 and 80/20 | Standardized strictly to the code's actual split: **80% train (4,400 samples) / 20% test (1,100 samples)** stratified. | ✅ Fixed |
| **Dataset Size & Reddit Claim** | Claimed a 1.27M Reddit corpus with no evidence | **Removed the 1.27M Reddit claim entirely.** Documented the true **5,500-sample algospeak dataset** (2,750 illicit + 2,750 benign controls) with **3 annotators and Fleiss’ $\kappa = 0.882$**. | ✅ Fixed |
| **Vision Model & Dataset** | Undocumented image dataset and vision metrics | Documented the **691-image dataset** (`Drug-Image-Dataset`), 80/20 split, and MobileNetV2 convergence to **84.67% validation accuracy**. | ✅ Fixed |
| **Latency Discrepancy** | Conflicted between 185 ms and 250–270 ms | Reconciled: **~185 ms** for local model inference pipeline, and **~250–270 ms** for end-to-end live browser network/DOM round-trip. | ✅ Fixed |
| **Normalization Rules** | Vague "slang lexicon" without counts | Documented exact **41 domain rules** (19 DEA-aligned drug emojis + 22 leetspeak rules), citing DEA Intelligence Bulletin [11]. | ✅ Fixed |
| **Fusion Weights & Thresholds** | Omitted weights and used 0.4/0.7 | Documented exact code formula: $S = \max(P_{\text{vis}}, 0.6 P_{\text{vis}} + 0.4 P_{\text{ocr}})$ and calibrated operating thresholds: **0.15 (Safe), 0.15–0.35 (Warn), $\ge 0.35$ (Block)**. | ✅ Fixed |
| **Normalization Ablation** | Missing ablation numbers | Documented **+12.30% accuracy gain** (84.50% unnormalized $\rightarrow$ 96.80% normalized) across the 41 rules (Fig. 7). | ✅ Fixed |
| **Missing Sections** | Lacked Ethics, Privacy, and Limitations | Added **Section VIII (Ethics, Privacy, and User Autonomy)** and **Section IX (Limitations and Future Work)**. | ✅ Fixed |
| **Table 1 & Figures** | Contained fabricated metrics; Fig 3 & 4 cut off | Expanded Table 1 to **6 validated baselines**; verified all **9 figures (Figs. 1–9)** are intact with proper captions. | ✅ Fixed |
| **References** | Duplicate refs and citation `[4][5]` typo | Cleaned and validated references **[1]–[26]** with correct in-text citations. | ✅ Fixed |

---

## 2. Unresolved Issues / Venue Check (Before Submission)

The paper is now **genuinely safe and defensible to submit** without fear of data fabrication or contradiction rejections. However, please check these two final items:

1. **Target Venue Formatting & Page Limits:**
   - The manuscript is currently formatted in **standard IEEE Conference 2-column style** (Letter, 0.75-inch margins, Times New Roman 10pt body, Table I, and IEEE reference style).
   - *Action:* If your target venue has a strict page limit (e.g., 6 pages vs. 8 pages) or uses a specific conference template (e.g., IEEE Access, Springer LNCS, ACM), adjust spacing or font sizes to match their exact page cap.
2. **Author Affiliations & Emails:**
   - Verify the author block on Page 1 (Agalya M, Kalaipriya S, Sowndhar A, Rajalingam B\*, Department of CSE AI&ML, KIT Coimbatore) and confirm that email addresses and corresponding author designations match your submission portal.
