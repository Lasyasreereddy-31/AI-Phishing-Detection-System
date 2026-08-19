import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from utils.url_features import extract_url_features


# -----------------------------------------
# Load Dataset
# -----------------------------------------

df = pd.read_csv("dataset/PhiUSIIL_Phishing_URL_Dataset.csv")

print("Dataset Loaded!")
print("Rows:", len(df))


# -----------------------------------------
# Extract URL Features
# -----------------------------------------

print("Extracting URL features...")

X = []

for url in df["URL"]:
    X.append(extract_url_features(str(url)))

X = pd.DataFrame(X)


# -----------------------------------------
# Target
# -----------------------------------------

y = df["label"]


# -----------------------------------------
# Train/Test Split
# -----------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# -----------------------------------------
# Train Random Forest
# -----------------------------------------

print("Training AI model...")

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# -----------------------------------------
# Test Model
# -----------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:", round(accuracy, 4))

print("\nClassification Report:")
print(classification_report(y_test, predictions))


# -----------------------------------------
# Save Model
# -----------------------------------------

joblib.dump(model, "model/phishing_model.pkl")

print("\n================================")
print("AI MODEL SAVED SUCCESSFULLY!")
print("================================")
print("Location: model/phishing_model.pkl")