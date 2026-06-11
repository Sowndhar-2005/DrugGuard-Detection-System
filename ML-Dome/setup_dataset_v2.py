"""
setup_dataset_v2.py
Improved training dataset for DrugGuard.

Key improvements over v1:
  - Adds HARD NEGATIVES: safe sentences that CONTAIN drug-related words
    (news, journalism, medical, research, law enforcement, UI text)
    so the model learns CONTEXT not just keywords.
  - Adds more realistic trafficking samples with coded slang.
  - Total: 1200 rows (600 drug + 600 safe), up from 600.
  - Negative class now includes sentences with "drug", "delivery",
    "marketplace", "available", "powder", etc. in safe contexts.
"""

import csv
import random

# ─── DRUG TRAFFICKING TEMPLATES (label = 1) ──────────────────────────────────

DRUG_TEMPLATES = [
    # Direct dealing
    "Got {drug} available for pickup tonight, DM for prices",
    "Selling premium {drug}, fast delivery guaranteed to your doorstep",
    "Fresh batch of {drug} just arrived, hit me up",
    "Need {drug} ASAP, anyone near {location} can deliver discreetly",
    "My {drug} guy just re-upped, quality stash available now",
    "Running low on {drug}, need a new connect today",
    "Can ship {drug} overnight, encrypted payments only",
    "Got a package of {drug} ready for the drop, message me",
    "Meeting the plug for {drug} at the usual spot tonight",
    "Reliable {drug} source, never been caught, discreet service",
    "Wholesale {drug} available, bulk discounts for regular buyers",
    "New shipment of {drug} landed, first come first served",
    "Connect me with your {drug} supplier in {location}",
    "Got the purest {drug} in {location}, no middleman needed",
    "Price drop on {drug}, limited stock, DM before it runs out",
    "Discreet {drug} delivery to your doorstep, cash only",
    "Looking to score some {drug} tonight in {location}",
    "Moving {drug} across the border this weekend, bulk orders",
    "{drug} supply chain ready for distribution across {location}",
    "Anyone got a {drug} plug near {location}? Need ASAP",
    "Got product available, hit my line, no pigs",
    "Dropping off the goods tonight, usual spot, bring cash",
    "Plug got stash ready, DM for menu and prices",
    "Selling white powder, premium quality, guaranteed pure",
    "Crystal available for pickup, cash only, fast turnaround",
    "Got pills ready to move, wholesale prices for bulk buyers",
    "Looking for a reliable plug for weekly supply in {location}",
    "Running my connect, got everything you need, DM me",
    "New batch arrived this week, fire quality, cheap prices",
    "Need someone to move product across state lines this weekend",
    "Got green and white available, best prices in {location}",
    "Drop me a message for the menu, got all the good stuff",
    "Moving packs tonight, need a driver for {location} run",
    "Got that fire ready for pickup, 24/7 service available",
]

# Emoji-coded drug trafficking (label = 1)
EMOJI_DRUG_TEMPLATES = [
    "Got that 🍃🍃🍃 ready, DM me for prices",
    "🔌 got the best ❄️ in town, hit me up now",
    "Fresh 💊💊 just landed, first come first served tonight",
    "🔥🔥 quality ❄️ available, fast delivery ⚡",
    "Who got the 🍄🍄? Need a plug ASAP 🔌",
    "💉 supply ready, DM for details, discreet service",
    "Got 🌿🌿 for cheap, bulk orders welcome, message me",
    "🔌 with the 💊 and ❄️ combo, best prices guaranteed",
    "New 📦 arrived, got 🍃 and 💊 ready to move tonight",
    "💰 deals only, 🔌 available 24/7 in {location}",
    "Selling 🍃 and 🍄, quality tested, fast delivery ⚡",
    "❄️ available for pickup, 💰 cash only, message for address",
    "Got the 🔥🔥 stash ready, DM for menu 📋",
    "🌿 and 💊 combo special this week only, DM now",
    "Plug got everything: 🍃 ❄️ 💊 🍄, best in {location}",
]

# ─── SAFE TEMPLATES (label = 0) ──────────────────────────────────────────────

# --- HARD NEGATIVES: news/journalism about drugs (safe!) ---
NEWS_TEMPLATES = [
    "Police seized a large shipment of illegal substances at the border checkpoint",
    "Authorities arrested three suspects in connection with drug trafficking operations",
    "The DEA announced a major crackdown on drug distribution networks this week",
    "Law enforcement agencies are investigating a suspected drug trafficking ring",
    "Officials confiscated thousands of pills during the drug bust operation yesterday",
    "The government is increasing penalties for drug trafficking offenses this year",
    "Investigators found evidence of drug distribution at the storage facility",
    "Border patrol agents intercepted a vehicle carrying controlled substances",
    "The district attorney charged five individuals with drug trafficking conspiracy",
    "A recent report highlights the rise of algospeak used to conceal drug deals online",
    "Researchers are studying social media patterns to detect drug-related activity",
    "The study analyzed machine learning approaches to drug trafficking detection",
    "Academic paper on using NLP to identify drug dealer language on social platforms",
    "DrugGuard is an AI-powered browser extension for detecting drug-related content",
    "The extension scans web pages for drug trafficking language in real time",
    "This drug detection system uses natural language processing to flag suspicious posts",
    "Scientists developed a model to classify drug-related posts on social media",
    "The algorithm achieved high accuracy in detecting drug trafficking language",
    "Researchers trained a classifier on drug trafficking data from Reddit forums",
    "The paper describes a multimodal system for drug content detection online",
    "Our system flags drug-related content using a transformer-based NLP model",
    "The DrugGuard extension monitors web pages for illicit drug trafficking content",
    "Testing the drug detection extension on sample web pages for accuracy",
    "This page demonstrates how the DrugGuard extension handles drug content detection",
    "Drug trafficking detection requires advanced models to handle algospeak patterns",
    "The DEA seized ten kilograms of cocaine during a raid in Florida",
    "Police arrested a suspect for illegally distributing prescription pills like xanax",
    "A major shipment of heroin was intercepted at the port yesterday",
    "Medical research shows the dangers of fentanyl abuse in suburban areas",
    "A study was published on the history of LSD and psychedelic mushrooms in therapy",
]

# --- HARD NEGATIVES: medical/pharmacy context (safe!) ---
MEDICAL_TEMPLATES = [
    "The doctor prescribed a new drug to treat the patient's chronic condition",
    "This medication is a controlled substance available by prescription only",
    "Pharmaceutical companies are developing new drugs to treat autoimmune disorders",
    "The FDA approved a new drug for treating depression after clinical trials",
    "Patients receiving drug therapy showed significant improvement after six weeks",
    "The pharmacist explained the drug interactions to avoid with this medication",
    "Antibiotic drugs are used to treat bacterial infections in clinical settings",
    "Drug rehabilitation centers provide support for individuals recovering from addiction",
    "The hospital administers pain medication through carefully monitored drug protocols",
    "Clinical trials for the new anti-cancer drug show promising results in early stages",
    "Over-the-counter drugs for cold and flu symptoms are available at pharmacies",
    "Drug abuse prevention programs are offered at local community health centers",
    "The patient was prescribed alprazolam to manage severe anxiety attacks",
    "Xanax should only be taken under direct medical supervision",
    "Fentanyl is a powerful synthetic opioid used for severe pain management in hospitals",
    "The doctor changed the prescription from valium to diazepam for better tolerance",
    "Adderall is commonly prescribed to treat attention deficit hyperactivity disorder",
    "The patient was treated with choline salicylate gel for mouth ulcers",
    "Apply alcofresh gum paint to the affected area twice daily",
    "Alcolabs manufactures pharmaceutical products under strict guidelines",
    "Choline salicylate is commonly used to treat pain and inflammation",
]

# --- HARD NEGATIVES: marketplace/delivery/selling safe items ---
ECOMMERCE_TEMPLATES = [
    "Selling my old {item} on the marketplace, barely used, great condition",
    "Fast delivery guaranteed to your doorstep within 3 business days",
    "New shipment of {item} arrived in our warehouse, available for order",
    "My {item} just arrived today and it works perfectly, great purchase",
    "Connect me with your {item} supplier in {location} for wholesale pricing",
    "Fresh batch of {item} just restocked, prices are very competitive",
    "Discreet packaging available for all orders, ships within 24 hours",
    "Got {item} available for pickup from our store in {location}",
    "Wholesale {item} available for bulk buyers, contact us for pricing",
    "Price drop on {item} this weekend only, limited stock remaining",
    "Amazon delivery driver dropped off the package at the wrong address",
    "Free overnight shipping on all orders over fifty dollars storewide",
    "The product arrived discreetly packaged as described by the seller",
    "Selling surplus inventory at reduced prices, all items brand new",
    "Looking for a reliable supplier of {item} for our small business",
    "The marketplace has great deals on used electronics this season",
    "I found a great deal on a used {item} locally, barely used",
    "Anyone selling a {item} near {location}? Looking for a good deal",
]

# --- Regular safe everyday conversation ---
SAFE_TEMPLATES = [
    "Just finished reading a great {item} about {topic}, highly recommend it",
    "Anyone recommend a good {item} for learning {topic} from scratch?",
    "Had an amazing {meal} at the new {place} downtown, absolutely delicious",
    "Looking for study partners for the {topic} exam coming up next week",
    "Going to the {place} this weekend with my family, really excited",
    "Started learning {topic} online through a free course, really enjoying it",
    "Need advice on buying a new {item} for college, any recommendations?",
    "The weather in {location} has been beautiful lately, perfect for a walk",
    "Cooking {meal} for dinner tonight, trying a new recipe I found",
    "Anyone want to join a {topic} study group that meets on weekends?",
    "Working on a {topic} project for my class, learning a lot from it",
    "Just moved to {location}, looking to make new friends in the area",
    "My new {item} is so much better than the old one, great upgrade",
    "Volunteering at the local {place} this Saturday, come join us",
    "Attended a {topic} workshop and learned so much about the field",
    "The {place} near my house has a great community events this month",
    "Planning a road trip to {location} next month, any recommendations?",
    "Best {meal} I have ever had at that restaurant, totally worth it",
    "My professor recommended a great textbook for the {topic} course",
    "Just finished my {topic} assignment, feeling really proud of the work",
    "Looking for a gym buddy to work out together three times a week",
    "Had a wonderful birthday party at the {place} last night with friends",
    "Tried a new {meal} recipe this weekend, turned out absolutely amazing",
    "The library has a new collection of books about {topic} this month",
    "Excited to start my new job at the tech company next Monday morning",
    # Balanced templates for drug-adjacent terms in safe contexts
    "Fresh organic {meal} ingredients available for delivery",
    "Drinking a warm cup of green tea in the morning is healthy",
    "Order organic matcha green tea powder online",
    "Need a new spark plug or electrical plug for the outlet",
    "Baking powder is a key ingredient for making pancakes",
    "The crystal clear water at the beach was beautiful",
    "Choose between white bread or whole wheat bread for the sandwich",
    "Take your daily vitamin pills with a glass of water",
    "A fresh batch of cookies is baking in the oven",
    "Keep your stash of yarn and hobby supplies organized",
    "The power supply for the computer failed and needs replacement",
    "Testing and scanning this web application to find security issues",
]

# ─── Fill-in words ────────────────────────────────────────────────────────────

DRUGS = [
    # General slang/coded terms
    "powder", "crystal", "pills", "white", "green", "stuff", "product",
    "pack", "goods", "stash", "supply", "batch", "packs", "bricks", "plug",
    # Darknet / Illegal drugs (Agora 2014-2015 categories)
    "cocaine", "heroin", "mdma", "ecstasy", "lsd", "acid", "meth", "methamphetamine",
    "speed", "ketamine", "weed", "cannabis", "marijuana", "hash", "hashish",
    "shrooms", "mushrooms", "dmt", "peyo", "mescaline", "psilocybin", "crank",
    # Pharmaceutical / Prescription drugs (Drug Listing Dataset)
    "xanax", "alprazolam", "valium", "diazepam", "ativan", "lorazepam",
    "klonopin", "clonazepam", "percocet", "oxycodone", "oxycontin", "vicodin",
    "hydrocodone", "adderall", "ritalin", "concerta", "fentanyl", "tramadol",
    "codeine", "morphine", "suboxone", "buprenorphine", "gabapentin", "pregabalin",
    "ambien", "zolpidem", "soma", "carisoprodol", "viagra", "sildenafil", "cialis",
    # Adversarial Typo / Slang / Typo Variations (advpromptset style)
    "xannys", "extasy", "fenty", "coka", "smack", "percs", "bars", "percocet"
]
ITEMS = [
    "laptop", "phone", "bicycle", "textbook", "camera", "headphones",
    "watch", "backpack", "tablet", "guitar", "keyboard", "monitor",
    "gaming chair", "desk lamp", "coffee maker"
]
TOPICS = [
    "machine learning", "history", "photography", "cooking", "music",
    "fitness", "coding", "art", "mathematics", "data science",
    "web development", "psychology", "economics", "biology", "chemistry"
]
MEALS = [
    "pasta", "sushi", "tacos", "pizza", "salad", "burger", "curry",
    "soup", "steak", "sandwich", "noodles", "rice bowl", "pancakes"
]
PLACES = [
    "park", "library", "gym", "cafe", "museum", "beach", "mall",
    "theater", "community center", "school", "garden", "sports club"
]
LOCATIONS = [
    "downtown", "the east side", "midtown", "the suburbs", "uptown",
    "the west end", "the bay area", "the north side", "the city center",
    "our neighborhood", "the local area"
]


def fill(template: str) -> str:
    t = template
    t = t.replace("{drug}", random.choice(DRUGS))
    t = t.replace("{item}", random.choice(ITEMS))
    t = t.replace("{topic}", random.choice(TOPICS))
    t = t.replace("{meal}", random.choice(MEALS))
    t = t.replace("{place}", random.choice(PLACES))
    t = t.replace("{location}", random.choice(LOCATIONS))
    return t


def main() -> None:
    random.seed(42)
    rows = []

    # ── Positive (Drug Trafficking) ──────────────────────────────────────────
    # 400 text-based drug trafficking
    for _ in range(400):
        t = random.choice(DRUG_TEMPLATES)
        rows.append([fill(t), 1])

    # 100 emoji-coded drug trafficking
    for _ in range(100):
        t = random.choice(EMOJI_DRUG_TEMPLATES)
        rows.append([fill(t), 1])

    # 100 duplicates with variations (simulate real social media noise)
    for _ in range(100):
        t = random.choice(DRUG_TEMPLATES)
        text = fill(t)
        # Add noise: extra filler words to vary the text
        noise = random.choice(["bro", "hit me", "fr fr", "100%", "no cap", "on god", "real talk"])
        rows.append([text + ", " + noise, 1])

    # ── Negative (Safe Content) ──────────────────────────────────────────────
    # 150 news/journalism about drugs (HARD NEGATIVES)
    for _ in range(150):
        rows.append([random.choice(NEWS_TEMPLATES), 0])

    # 100 medical/pharmacy context (HARD NEGATIVES)
    for _ in range(100):
        rows.append([random.choice(MEDICAL_TEMPLATES), 0])

    # 150 e-commerce/delivery/marketplace safe text (HARD NEGATIVES)
    for _ in range(150):
        t = random.choice(ECOMMERCE_TEMPLATES)
        rows.append([fill(t), 0])

    # 200 general safe everyday conversation
    for _ in range(200):
        t = random.choice(SAFE_TEMPLATES)
        rows.append([fill(t), 0])

    random.shuffle(rows)

    with open("dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(rows)

    total = len(rows)
    drug_count = sum(1 for r in rows if r[1] == 1)
    safe_count = total - drug_count
    print(f"Dataset created: dataset.csv")
    print(f"  Total rows : {total}")
    print(f"  Drug (1)   : {drug_count}")
    print(f"  Safe (0)   : {safe_count}")
    print(f"  Hard negatives included: news, medical, e-commerce contexts")


if __name__ == "__main__":
    main()
