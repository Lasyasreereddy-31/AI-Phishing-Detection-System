import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib

# Read Dataset
data = pd.read_csv("dataset/phishing_urls.csv")

# Features and Labels
X = data["url"]
y = data["label"]

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Build Model
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB())
])

# Train
model.fit(X_train, y_train)

# Test
predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))

# Save Model
joblib.dump(model, "model/phishing_model.pkl")

print("Model Saved Successfully!")