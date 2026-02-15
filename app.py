"""
app.py
Interactive CLI to test the Drug Trafficking Detection model.
Type a sentence → get a Yes/No prediction with confidence score.
"""

import pickle


def load_artifacts():
    """Load the trained model and vectorizer from disk."""
    with open("text_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    return model, vectorizer


def predict(text: str, model, vectorizer):
    """Predict whether the input text is drug-related or safe."""
    text_vec = vectorizer.transform([text.lower()])
    prediction = model.predict(text_vec)[0]
    confidence = max(model.predict_proba(text_vec)[0]) * 100
    return prediction, confidence


def main() -> None:
    print("=" * 60)
    print("   Text-Based Drug Trafficking Detection System")
    print("=" * 60)

    model, vectorizer = load_artifacts()
    print("Model loaded successfully!\n")

    while True:
        print("-" * 60)
        user_input = input("Enter text to analyze (or 'quit' to exit):\n>> ").strip()

        if user_input.lower() in ("quit", "exit", "q"):
            print("\nGoodbye!")
            break

        if not user_input:
            print("Please enter some text.\n")
            continue

        prediction, confidence = predict(user_input, model, vectorizer)

        print(f"\n   Input      : {user_input}")
        print(f"   Confidence : {confidence:.2f}%")

        if prediction == 1:
            print("   Result     : YES — Drug Trafficking Detected")
            print("   Status     : ILLICIT — Flagged as drug-related.\n")
        else:
            print("   Result     : NO — Safe Text")
            print("   Status     : SAFE — This text appears normal.\n")


if __name__ == "__main__":
    main()
