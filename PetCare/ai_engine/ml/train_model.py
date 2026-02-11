import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# 📥 Load dataset
data = pd.read_csv("dataset.csv")

X = data["text"].astype(str)
y = data["intent"]

# 🧠 Improved TF-IDF (BIG CONFIDENCE BOOST)
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),        # learn phrases like "buy products"
    stop_words="english",     # remove useless words
    max_df=0.9
)

X_vectorized = vectorizer.fit_transform(X)

# 🤖 Improved Naive Bayes
model = MultinomialNB(alpha=0.3)
model.fit(X_vectorized, y)

# 💾 Save model
with open("intent_model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)

print("✅ Intent model trained and saved successfully")
