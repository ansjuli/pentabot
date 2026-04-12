# modules/system/train_echo.py
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# File paths
FAILED_LOG_FILE = Path("modules/system/failed_commands.json")
MISHEARS_FILE = Path("modules/system/mishears.json")
ML_MODEL_FILE = Path("modules/system/ml_model.pkl")
VECTORIZER_FILE = Path("modules/system/vectorizer.pkl")


# ----------------------------
# Step 1: Interactive mishears trainer
# ----------------------------
def train_mishears():
    """Load failed commands and let user map misheard phrases to correct commands/apps."""
    # Load existing mishears
    if MISHEARS_FILE.exists():
        with open(MISHEARS_FILE, "r", encoding="utf-8") as f:
            mishears = json.load(f)
    else:
        mishears = {}

    # Load failed log
    if FAILED_LOG_FILE.exists():
        with open(FAILED_LOG_FILE, "r", encoding="utf-8") as f:
            failed_log = json.load(f)
    else:
        print("[Echo Training] No failed commands logged ✅")
        return mishears

    # Interactive correction
    for phrase in failed_log:
        if phrase in mishears:
            continue  # skip already mapped
        print(f"\n[Echo Training] Misheard phrase: '{phrase}'")
        correct = input("Correct mapping (leave empty to ignore): ").strip()
        if correct:
            mishears[phrase] = correct

    # Save updated mishears
    with open(MISHEARS_FILE, "w", encoding="utf-8") as f:
        json.dump(mishears, f, indent=2)
    print("[Echo Training] Mishears updated ✅")
    return mishears


# ----------------------------
# Step 2: Train small ML classifier
# ----------------------------
def train_ml(mishears):
    """Train a small offline ML model from mishears and save it locally."""
    if not mishears:
        print("[Echo ML] No mishears to train on ❌")
        return

    X = list(mishears.keys())
    y = list(mishears.values())

    # Character n-grams for robust text representation
    vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4))
    X_vect = vectorizer.fit_transform(X)

    clf = LogisticRegression(max_iter=200)
    clf.fit(X_vect, y)

    # Save model + vectorizer
    pickle.dump(clf, ML_MODEL_FILE.open("wb"))
    pickle.dump(vectorizer, VECTORIZER_FILE.open("wb"))
    print("[Echo ML] Model trained & saved ✅")


# ----------------------------
# Step 3: Optional evaluation
# ----------------------------
def predict(text, threshold=0.7):
    """Predict command using trained ML model, return None if confidence is low."""
    if not ML_MODEL_FILE.exists() or not VECTORIZER_FILE.exists():
        return None

    clf = pickle.load(ML_MODEL_FILE.open("rb"))
    vectorizer = pickle.load(VECTORIZER_FILE.open("rb"))
    X_vect = vectorizer.transform([text])
    prob = clf.predict_proba(X_vect)[0]
    idx = prob.argmax()
    if prob[idx] >= threshold:
        return clf.classes_[idx]
    return None


# ----------------------------
# Step 4: Main trainer flow
# ----------------------------
def main():
    print("=== Echo Local Trainer ===")
    mishears = train_mishears()
    train_ml(mishears)
    print("Training complete ✅")

    # Optional: test a phrase
    while True:
        test = input("\nType a phrase to test ML (or 'exit'): ").strip()
        if test.lower() in ["exit", "quit"]:
            break
        pred = predict(test)
        if pred:
            print(f"[ML Prediction] '{test}' -> '{pred}'")
        else:
            print(f"[ML Prediction] No confident match for '{test}'")


if __name__ == "__main__":
    main()