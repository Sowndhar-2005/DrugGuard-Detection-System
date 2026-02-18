"""
setup_dataset.py
Generates a synthetic dataset (dataset.csv) with 500 rows for
Text-Based Drug Trafficking Detection.

Labels:
    1 = Drug Trafficking (Illicit)
    0 = Safe / Normal (Non-Illicit)
"""

import csv
import random

# Drug trafficking text templates
DRUG_TEMPLATES = [
    "Looking for a plug to get some {drug} delivered tonight",
    "Got {drug} available for pickup, DM for prices",
    "Need {drug} ASAP, anyone near {location} can deliver?",
    "Selling premium {drug}, fast delivery guaranteed",
    "Fresh batch of {drug} just arrived, hit me up",
    "{drug} supply chain ready for distribution",
    "Moving {drug} across the border this weekend",
    "Wholesale {drug} available, bulk discounts",
    "New shipment of {drug} landed, first come first served",
    "Connect me with your {drug} supplier in {location}",
    "Got the purest {drug} in {location}, no middleman",
    "Price drop on {drug}, limited stock available",
    "Discreet {drug} delivery to your doorstep",
    "Looking to score some {drug} tonight in {location}",
    "My {drug} guy just re-upped, quality stuff",
    "Running low on {drug}, need a new connect",
    "Can ship {drug} overnight, encrypted payments only",
    "Got a package of {drug} ready for the drop",
    "Meeting the plug for {drug} at the usual spot",
    "Reliable {drug} source, never been caught",
]

# Safe / normal text templates
SAFE_TEMPLATES = [
    "Just finished reading a great {item} about {topic}",
    "Anyone recommend a good {item} for {topic}?",
    "Selling my old {item} on marketplace, barely used",
    "Had an amazing {meal} at the new {place} downtown",
    "Looking for study partners for {topic} exam next week",
    "My {item} arrived today and it works perfectly",
    "Going to the {place} this weekend with family",
    "Started learning {topic} online, really enjoying it",
    "Need advice on buying a new {item} for college",
    "The weather in {location} has been beautiful lately",
    "Cooking {meal} for dinner tonight, easy recipe",
    "Anyone want to join a {topic} study group?",
    "Found a great deal on a used {item} locally",
    "Planning a road trip to {location} next month",
    "Best {meal} I have ever had, totally worth it",
    "Working on a {topic} project for my class",
    "Just moved to {location}, looking for friends",
    "My new {item} is so much better than the old one",
    "Volunteering at the local {place} this Saturday",
    "Attended a {topic} workshop and learned so much",
]

# Fill-in words
DRUGS = ["powder", "crystal", "pills", "white", "green", "stuff", "product", "pack", "goods", "stash"]
ITEMS = ["laptop", "phone", "bicycle", "textbook", "camera", "headphones", "watch", "backpack", "tablet", "guitar"]
TOPICS = ["machine learning", "history", "photography", "cooking", "music", "fitness", "coding", "art", "math", "science"]
MEALS = ["pasta", "sushi", "tacos", "pizza", "salad", "burger", "curry", "soup", "steak", "sandwich"]
PLACES = ["park", "library", "gym", "cafe", "museum", "beach", "mall", "theater", "church", "school"]
LOCATIONS = ["downtown", "the east side", "midtown", "the suburbs", "uptown", "the west end", "the bay area", "the north side"]


def generate_text(template: str, is_drug: bool) -> str:
    """Fill in a template with random words."""
    text = template
    text = text.replace("{drug}", random.choice(DRUGS))
    text = text.replace("{item}", random.choice(ITEMS))
    text = text.replace("{topic}", random.choice(TOPICS))
    text = text.replace("{meal}", random.choice(MEALS))
    text = text.replace("{place}", random.choice(PLACES))
    text = text.replace("{location}", random.choice(LOCATIONS))
    return text


def main() -> None:
    random.seed(42)
    rows = []

    # Generate 250 drug trafficking texts (label = 1)
    for _ in range(250):
        template = random.choice(DRUG_TEMPLATES)
        text = generate_text(template, is_drug=True)
        rows.append([text, 1])

    # Generate 250 safe texts (label = 0)
    for _ in range(250):
        template = random.choice(SAFE_TEMPLATES)
        text = generate_text(template, is_drug=False)
        rows.append([text, 0])

    # Shuffle
    random.shuffle(rows)

    # Write CSV
    with open("dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(rows)

    print(f"Dataset created: dataset.csv  ({len(rows)} rows)")


if __name__ == "__main__":
    main()
