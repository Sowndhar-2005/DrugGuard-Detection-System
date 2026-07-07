"""
train_model.py
Loads dataset.csv, trains a Multinomial Naive Bayes classifier,
evaluates on an 80/20 split, and saves model + vectorizer as .pkl files.
"""

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report


def normalize_text(text: str) -> str:
    """
    Standardizes input text by mapping emojis to semantic text equivalents,
    and correcting simple leetspeak obfuscations (e.g. d*ugs -> drugs).
    """
    emoji_map = {
        "🍃": " marijuana ",
        "🌿": " marijuana ",
        "❄️": " cocaine ",
        "💊": " pills ",
        "🔌": " plug ",
        "🍄": " mushrooms ",
        "💉": " heroin ",
        "📦": " package ",
        "💰": " cash ",
    }
    for emoji, replacement in emoji_map.items():
        text = text.replace(emoji, replacement)
        
    leetspeak_map = {
        "dr*gs": "drugs",
        "dr*g": "drug",
        "d r u g s": "drugs",
        "d r u g": "drug",
        "x*nax": "xanax",
        "x@nax": "xanax",
        "c*caine": "cocaine",
        "h*roin": "heroin",
        "f*ntanyl": "fentanyl",
    }
    for pattern, replacement in leetspeak_map.items():
        text = text.replace(pattern, replacement)
        
    return text


def main() -> None:
    # Load dataset
    df = pd.read_csv("dataset.csv")
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns\n")

    # Preprocessing
    df["text"] = df["text"].astype(str).apply(normalize_text).str.lower()
    X = df["text"]
    y = df["label"]

    # Train-Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Split -> Train: {len(X_train)}  |  Test: {len(X_test)}\n")

    # Vectorization (Bag of Words) with emoji and stopword support
    vectorizer = CountVectorizer(token_pattern=r'(?u)\b\w+\b|[^\x00-\x7F]', stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train model
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    # Evaluate
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)

    print("=" * 50)
    print(f"  Accuracy: {accuracy * 100:.2f}%")
    print("=" * 50)
    print("\nClassification Report:\n")
    print(
        classification_report(
            y_test, y_pred, target_names=["Safe (0)", "Drug Trafficking (1)"]
        )
    )

    # Save model & vectorizer
    with open("text_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    print("Model saved      -> text_model.pkl")
    print("Vectorizer saved  -> vectorizer.pkl")


if __name__ == "__main__":
    main()
