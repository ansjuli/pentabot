# modules/system/train_ml.py
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

FAILED_LOG_FILE = Path("modules/system/failed_commands.json")
MISHEARS_FILE = Path("modules/system/mishears.json")
ML_MODEL_FILE = Path("modules/system/ml_model.pkl")
VECTORIZER_FILE = Path("modules/system/vectorizer.pkl")

def train_ml():
    # Load mishears as high-confidence data
    if MISHEARS_FILE.exists():
        with open(MISHEARS_FILE, "r", encoding="utf-8") as f:
            mishears = json.load(f)
    else:
        mishears = {}

    X = []
    y = []

    for wrong, correct in mishears.items():
        X.append(wrong)
        y.append(correct)

    # Also add failed commands mapped manually (if available)
    if FAILED_LOG_FILE.exists():
        with open(FAILED_LOG_FILE, "r", encoding="utf-8") as f:
            failed = json.load(f)
        # For now, skip unmapped failed commands

    # Train vectorizer
    vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2,4))
    X_vect = vectorizer.fit_transform(X)

    clf = LogisticRegression(max_iter=200)
    clf.fit(X_vect, y)

    # Save model + vectorizer
    pickle.dump(clf, ML_MODEL_FILE.open("wb"))
    pickle.dump(vectorizer, VECTORIZER_FILE.open("wb"))
    print("[Echo ML] Model trained & saved ✅")