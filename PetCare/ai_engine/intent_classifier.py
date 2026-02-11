import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "intent_model.pkl")

vectorizer = None
model = None

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        vectorizer, model = pickle.load(f)
else:
    print("⚠️ intent_model.pkl not found")

def detect_intent(text):
    if not model or not vectorizer:
        return {"intent": "unknown", "confidence": 0.0}

    X = vectorizer.transform([text])
    intent = model.predict(X)[0]
    confidence = max(model.predict_proba(X)[0])

    return {
        "intent": intent,
        "confidence": round(confidence, 2)
    }
