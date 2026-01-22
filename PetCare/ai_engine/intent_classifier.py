import pickle
import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "ml",
    "intent_model.pkl"
)

with open(MODEL_PATH, "rb") as f:
    vectorizer, model = pickle.load(f)

def detect_intent(user_text):
    text_vector = vectorizer.transform([user_text])
    intent = model.predict(text_vector)[0]
    return intent
