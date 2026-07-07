import os
import matplotlib.pyplot as plt
import numpy as np

# Set design styles
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['figure.autolayout'] = True

# Colors matching a sleek theme (dark slate, modern teal, coral red, golden warning)
colors_dark = ['#1e293b', '#0ea5e9', '#ef4444', '#f59e0b', '#10b981', '#6366f1']

# Output directory
output_dir = r"d:\Project\DrugGuard-Detection-System\media"
os.makedirs(output_dir, exist_ok=True)

def generate_fig4_dataset_composition():
    # Fig. 4: Dataset Composition
    categories = [
        'Direct Drug Ads\n(33.3%)', 
        'Emoji-Coded Ads\n(8.3%)', 
        'Noisy Drug Ads\n(8.3%)',
        'News / busts\n(12.5%)', 
        'Medical Context\n(8.3%)', 
        'Safe E-Commerce\n(12.5%)', 
        'General Chat\n(16.7%)'
    ]
    counts = [400, 100, 100, 150, 100, 150, 200]
    classes = ['Drug (600)', 'Drug (600)', 'Drug (600)', 'Safe (600)', 'Safe (600)', 'Safe (600)', 'Safe (600)']
    
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    bars = ax.bar(categories, counts, color=['#f43f5e', '#ec4899', '#db2777', '#3b82f6', '#10b981', '#84cc16', '#64748b'], edgecolor='black', linewidth=0.5)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
                    
    ax.set_title('Fig. 4: Dataset Composition Categories (N = 1,200)', fontsize=12, fontweight='bold', pad=15)
    ax.set_ylabel('Sample Count', fontsize=10)
    ax.set_ylim(0, 460)
    
    # Add grouping labels at the bottom
    plt.savefig(os.path.join(output_dir, "img_0004.jpeg"), bbox_inches='tight', format='jpeg', dpi=300)
    plt.close()
    print("Generated img_0004.jpeg (Dataset Composition)")

def generate_fig5_dataset_split():
    # Fig. 5: Dataset Split Distribution (80/20 train/test)
    labels = ['Training Set\n(80% - 960 samples)', 'Test Set\n(20% - 240 samples)']
    sizes = [960, 240]
    
    fig, ax = plt.subplots(figsize=(6, 5), dpi=300)
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        autopct='%1.0f%%', 
        startangle=140, 
        colors=['#6366f1', '#06b6d4'],
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
        pctdistance=0.75
    )
    
    plt.setp(texts, fontsize=10, fontweight='bold')
    plt.setp(autotexts, size=10, weight="bold", color="white")
    
    ax.set_title('Fig. 5: Stratified Dataset Split Distribution', fontsize=12, fontweight='bold', pad=15)
    plt.savefig(os.path.join(output_dir, "img_0005.jpeg"), bbox_inches='tight', format='jpeg', dpi=300)
    plt.close()
    print("Generated img_0005.jpeg (Dataset Split Distribution)")

def generate_fig6_ablation_study():
    # Fig. 6: Ablation Study
    methods = ['Keyword Filter', 'Regex Filter', 'Naive Bayes\n(Text Only)', 'Multimodal\n(OCR + NB)']
    accuracies = [71.20, 76.50, 98.75, 98.75]
    
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    bars = ax.bar(methods, accuracies, color=['#cbd5e1', '#94a3b8', '#0ea5e9', '#10b981'], width=0.5, edgecolor='black', linewidth=0.5)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
                    
    ax.set_title('Fig. 6: Classification Accuracy by Method', fontsize=12, fontweight='bold', pad=15)
    ax.set_ylabel('Accuracy (%)', fontsize=10)
    ax.set_ylim(0, 110)
    plt.savefig(os.path.join(output_dir, "img_0006.jpeg"), bbox_inches='tight', format='jpeg', dpi=300)
    plt.close()
    print("Generated img_0006.jpeg (Ablation Study)")

def generate_fig7_latency():
    # Fig. 7: End-to-End Inference Latency Breakdown
    labels = ['Text classification\n(Inference + Vectorization)', 'Image OCR text extraction\n(RapidOCR)', 'Network roundtrip\n(FastAPI local server)']
    times = [4.5, 220, 45]  # in ms
    
    fig, ax = plt.subplots(figsize=(8, 4), dpi=300)
    y_pos = np.arange(len(labels))
    
    bars = ax.barh(y_pos, times, align='center', color=['#38bdf8', '#fb7185', '#fcd34d'], height=0.5, edgecolor='black', linewidth=0.5)
    ax.set_yticks(y_pos, labels=labels, fontsize=9, fontweight='bold')
    ax.invert_yaxis()  # top-down
    ax.set_xlabel('Time (milliseconds)', fontsize=10)
    ax.set_title('Fig. 7: Average Processing Latency Breakdown (ms)', fontsize=12, fontweight='bold', pad=15)
    
    # Add values to the ends of the bars
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width} ms',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0),  # 5 points horizontal offset
                    textcoords="offset points",
                    ha='left', va='center', fontsize=9, fontweight='bold')
                    
    ax.set_xlim(0, 270)
    plt.savefig(os.path.join(output_dir, "img_0007.jpeg"), bbox_inches='tight', format='jpeg', dpi=300)
    plt.close()
    print("Generated img_0007.jpeg (Latency Breakdown)")

if __name__ == "__main__":
    generate_fig4_dataset_composition()
    generate_fig5_dataset_split()
    generate_fig6_ablation_study()
    generate_fig7_latency()
