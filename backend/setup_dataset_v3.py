"""
setup_dataset_v3.py
DrugGuard — Robust Dataset Generator (5,000+ Rows)

Generates balanced safe (class 0) and drug-related (class 1) text data
including emoji mappings, leetspeak, spacing obfuscation, and clean content.
"""

import os
import random
import pandas as pd

# Safe templates (Class 0)
SAFE_TEMPLATES = [
    "The doctor recommended a new {med} prescription for {illness}.",
    "FDA approved a novel {med} formulation to treat chronic {illness}.",
    "Ensure you take your {med} dose after meals.",
    "Can you pick up my {med} refill from the CVS pharmacy tomorrow?",
    "We need to study the chemical synthesis of {med} in our organic lab.",
    "I need a workout partner for the gym session tonight.",
    "Please send the shipping details for the standard package.",
    "The shipping company delivered the items to the local post office.",
    "Our research team published a paper on deep learning for healthcare classification.",
    "How does the drug rehabilitation center support patients in recovery?",
    "A study was published detailing side effects of {med} on children.",
    "I am looking for a cheap laptop to buy for university work.",
    "Let's meet at the coffee shop at 5pm to discuss the project slides.",
    "The government is implementing strict border controls to stop trafficking.",
    "The police seized smuggled items at the seaport today.",
    "Are you interested in reading this textbook about natural language processing?",
    "The weather is absolutely beautiful outside, let's go for a walk.",
    "Do you want to grab some pizza and watch a movie tonight?",
    "I forgot my homework at home, can I copy your notes?",
    "The company announced a significant increase in their quarterly revenue."
]

MEDICATIONS = [
    "ibuprofen", "aspirin", "insulin", "metformin", "lisinopril", 
    "amoxicillin", "atorvastatin", "albuterol", "omeprazole", "gabapentin"
]

ILLNESSES = [
    "hypertension", "diabetes", "bacterial infection", "asthma", "acid reflux",
    "chronic pain", "headache", "inflammation", "fever", "arthritis"
]

# Drug templates (Class 1)
DRUG_TEMPLATES = [
    "{plug} got that {drug} on deck, hit me up on Signal.",
    "Fast shipping on premium {drug}, DM for prices.",
    "Got a fresh batch of {drug} ready for delivery tonight.",
    "Selling high-quality {drug}, discreet packaging, cash or BTC accepted.",
    "{plug} has the best {drug} in town, fast delivery.",
    "Looking for a {plug} for {drug} in the local area, HMU.",
    "Premium quality {drug} available, PGP verified listings.",
    "Cheap {drug} pills for sale, bulk discounts available, PM me.",
    "Safe and discreet delivery of {drug} straight to your mailbox.",
    "Who is active tonight? Need a delivery of {drug} ASAP."
]

PLUGS = [
    "The plug", "My local plug", "Vendor", "🔌", "Connection", "Seller", "Plug"
]

DRUGS_WORDS = [
    "weed", "marijuana", "cocaine", "heroin", "fentanyl", "xanax", "percocet", "meth", "ketamine", "oxy"
]

# Obfuscations mappings
OBFUSCATIONS = {
    "weed": ["w33d", "🍃", "🌿", "w e e d", "weed 🍃"],
    "marijuana": ["mar1juana", "c@nnab!s", "ganja", "🌿", "marijuana 🌿"],
    "cocaine": ["c0ca1ne", "c*caine", "❄️", "c o c a i n e", "cocaine ❄️"],
    "heroin": ["h*roin", "h.e.r.o.i.n", "💉", "heroin 💉"],
    "fentanyl": ["f*ntanyl", "f3nt@nyl", "fentanyl 💀"],
    "xanax": ["x*nax", "x@nax", "x@n@x", "💊", "xanax 💊"],
    "percocet": ["p3rc0c3t", "percs", "💊"],
    "meth": ["m3th", "ice", "🧊", "meth 🧊"],
    "ketamine": ["k3tam1ne", "special k", "🐴"],
    "oxy": ["0xy", "oxycodone", "💊"]
}

def generate_dataset(num_rows=5500):
    rows = []
    
    # Half safe, half drug
    half = num_rows // 2
    
    # Safe rows
    for _ in range(half):
        template = random.choice(SAFE_TEMPLATES)
        med = random.choice(MEDICATIONS)
        ill = random.choice(ILLNESSES)
        text = template.format(med=med, illness=ill)
        
        # Randomly insert occasional safe emoji
        if random.random() < 0.15:
            text += " " + random.choice(["😊", "👍", "☕", "📖", "💻", "🏃"])
            
        rows.append({"text": text, "label": 0})
        
    # Drug rows
    for _ in range(half):
        template = random.choice(DRUG_TEMPLATES)
        plug = random.choice(PLUGS)
        drug = random.choice(DRUGS_WORDS)
        
        # Apply algospeak / obfuscation with 70% probability
        if random.random() < 0.70:
            drug_val = random.choice(OBFUSCATIONS[drug])
        else:
            drug_val = drug
            
        text = template.format(plug=plug, drug=drug_val)
        
        # Add drug emojis randomly
        if random.random() < 0.30:
            text += " " + random.choice(["💊", "🔌", "🍃", "❄️", "🍄", "💉", "📦", "💰"])
            
        rows.append({"text": text, "label": 1})
        
    # Shuffle and create DataFrame
    random.shuffle(rows)
    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    print("Generating DrugGuard dataset v3...")
    df = generate_dataset()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, "dataset.csv")
    
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} rows. Saved to: {output_path}")
    print(df["label"].value_counts())
