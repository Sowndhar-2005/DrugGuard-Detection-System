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


def explain_prediction(text: str, model, vectorizer):
    """
    Identify which words contributed most to the Drug Trafficking prediction.
    Returns a list of (word, score) tuples. Positive score = Drug, Negative = Safe.
    """
    # Tokenize input exactly like the vectorizer does
    analyzer = vectorizer.build_analyzer()
    tokens = analyzer(text)
    
    # Filter words that are actually in our vocabulary
    valid_tokens = [t for t in tokens if t in vectorizer.vocabulary_]
    
    if not valid_tokens:
        return []

    # Get log probabilities from the model
    # index 0 is Safe, index 1 is Drug
    log_prob_safe = model.feature_log_prob_[0]
    log_prob_drug = model.feature_log_prob_[1]
    
    word_contributions = []
    
    for token in valid_tokens:
        idx = vectorizer.vocabulary_[token]
        # Score > 0 means adds to Drug probability
        # Score < 0 means adds to Safe probability
        score = log_prob_drug[idx] - log_prob_safe[idx]
        word_contributions.append((token, score))
    
    # Sort by highest "Drug" influence
    word_contributions.sort(key=lambda x: x[1], reverse=True)
    return word_contributions


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
        triggers = explain_prediction(user_input, model, vectorizer)

        print(f"\n   Input      : {user_input}")
        print(f"   Confidence : {confidence:.2f}%")

        if prediction == 1:
            print("   Result     : YES — Drug Trafficking Detected")
            print("   Status     : ILLICIT — Flagged as drug-related.\n")
            
            # Show ONLY words that actually pushed toward "Drug" class (score > 0)
            drug_triggers = [t for t in triggers if t[1] > 0]
            if drug_triggers:
                print("   🔍 Why? These words triggered the alarm:")
                for word, score in drug_triggers[:3]:  # Show top 3
                    # Visual bar for impact
                    bar = "█" * int(score * 2) 
                    print(f"      - {word:<12} {bar} (Risk Score: {score:.2f})")
                print()
                
        else:
            print("   Result     : NO — Safe Text")
            print("   Status     : SAFE — This text appears normal.\n")
            
            # Optional: Show what made it safe
            safe_signals = [t for t in triggers if t[1] < 0]
            if safe_signals:
                print("   🛡️  Safe signals found:")
                for word, score in safe_signals[-3:]: # Sort is descending, so safe are at end
                    print(f"      - {word}")
                print()


if __name__ == "__main__":
    main()
