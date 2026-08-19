import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# -----------------------------------------
# Training Email Dataset
# 0 = Safe
# 1 = Phishing
# -----------------------------------------

emails = [

    # Safe emails
    "Hello, the project meeting is scheduled for tomorrow at 10 AM.",
    "Please find the assignment report attached.",
    "Your appointment is confirmed for Monday.",
    "Thank you for submitting your project.",
    "The college examination timetable has been released.",
    "Your order has been delivered successfully.",
    "The team meeting will start at 2 PM.",
    "Please bring your project report tomorrow.",
    "Your application has been received successfully.",
    "The event will be held in the seminar hall.",
    "Your payment receipt is attached.",
    "Thank you for your email. We will respond shortly.",
    "Your library book is due next week.",
    "The class schedule has been updated.",
    "Your registration has been completed.",

    # Phishing emails
    "URGENT! Your bank account has been suspended. Verify your password immediately.",
    "Click here to verify your account or it will be permanently closed.",
    "Congratulations! You are a winner. Click the link to claim your gift.",
    "Your account security has been compromised. Login immediately to verify.",
    "Urgent security alert! Confirm your bank password now.",
    "Your email account will be deleted. Click here to verify your account.",
    "You have won a cash prize. Provide your bank details to receive the money.",
    "Your payment failed. Click here and enter your password to continue.",
    "Verify your banking information immediately to avoid account suspension.",
    "Security warning! Your account requires immediate verification.",
    "Click this link to reset your password and restore your account.",
    "Your account has been locked. Login now to unlock it.",
    "You are selected as a lucky winner. Claim your prize immediately.",
    "Urgent! Confirm your credit card information to avoid cancellation.",
    "Your bank account needs verification. Click here immediately."
]


labels = [
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,

    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1
]


# -----------------------------------------
# Convert text into numerical features
# -----------------------------------------

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

X = vectorizer.fit_transform(emails)


# -----------------------------------------
# Train Machine Learning Model
# -----------------------------------------

model = LogisticRegression()

model.fit(X, labels)


# -----------------------------------------
# Save Model and Vectorizer
# -----------------------------------------

joblib.dump(model, "model/email_phishing_model.pkl")
joblib.dump(vectorizer, "model/email_vectorizer.pkl")


print("Email phishing model trained successfully!")
print("Model saved to model/email_phishing_model.pkl")
print("Vectorizer saved to model/email_vectorizer.pkl")