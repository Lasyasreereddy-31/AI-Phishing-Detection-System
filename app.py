from flask import Flask, render_template, request, send_file, redirect
import sqlite3
import os
import joblib

from utils.url_features import extract_url_features
from report_generator import generate_security_report


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# PATHS
# ============================================================

DATABASE_NAME = "database/phishing.db"
MODEL_PATH = "model/phishing_model.pkl"


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            result TEXT,
            confidence REAL,
            scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# SAVE SCAN
# ============================================================

def save_scan(url, result, confidence):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scan_history
        (url, result, confidence)
        VALUES (?, ?, ?)
    """, (url, result, confidence))

    conn.commit()
    conn.close()


# ============================================================
# GET HISTORY
# ============================================================

def get_history():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, url, result, confidence, scan_time
        FROM scan_history
        ORDER BY scan_time DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ============================================================
# LOAD ML MODEL
# ============================================================

model = None

try:

    if os.path.exists(MODEL_PATH):

        model = joblib.load(MODEL_PATH)

        print("Phishing model loaded successfully.")

    else:

        print("WARNING: phishing model not found.")

except Exception as e:

    print("WARNING: Could not load phishing model.")
    print(e)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")


# ============================================================
# URL ANALYZER PAGE
# ============================================================

@app.route("/analyze_url", methods=["GET"])
def analyze_url_page():

    return render_template("url_analyzer.html")


# ============================================================
# URL ANALYSIS
# ============================================================

@app.route("/analyze_url", methods=["POST"])
def analyze_url():

    url = request.form.get("url", "").strip()

    if not url:

        return render_template(
            "result.html",
            input_data="No URL entered",
            result="Invalid Input",
            confidence=0
        )

    try:

        # Extract URL features
        features = extract_url_features(url)

        # Convert features to model input
        if hasattr(features, "values"):

            model_input = [features.values]

        else:

            model_input = [features]

        # ----------------------------------------------------
        # ML Prediction
        # ----------------------------------------------------

        if model is not None:

            prediction = model.predict(model_input)[0]

            if hasattr(model, "predict_proba"):

                probabilities = model.predict_proba(model_input)[0]

                confidence = max(probabilities) * 100

            else:

                confidence = 99.0

            prediction_string = str(prediction).lower()

            if (
                prediction == 1
                or prediction_string in [
                    "1",
                    "phishing",
                    "malicious",
                    "suspicious"
                ]
            ):

                result = "Phishing Website Detected"

            else:

                result = "Legitimate Website"

        else:

            result = "Model Not Available"
            confidence = 0

        confidence = round(confidence, 2)

        # Save scan
        save_scan(
            url,
            result,
            confidence
        )

        # Display result
        return render_template(
            "result.html",
            input_data=url,
            result=result,
            confidence=confidence
        )

    except Exception as e:

        print("URL ANALYSIS ERROR:")
        print(e)

        return render_template(
            "result.html",
            input_data=url,
            result="Analysis Error",
            confidence=0,
            error=str(e)
        )


# ============================================================
# EMAIL ANALYZER PAGE
# ============================================================

@app.route("/email_analyzer", methods=["GET"])
def email_analyzer():

    return render_template("email_analyzer.html")


# ============================================================
# EMAIL ANALYSIS
# ============================================================

@app.route("/analyze_email", methods=["POST"])
def analyze_email():

    subject = request.form.get(
        "subject",
        ""
    ).strip()

    email_body = request.form.get(
        "email",
        ""
    ).strip()

    email_text = (
        "Subject: "
        + subject
        + "\n"
        + email_body
    )

    if not subject and not email_body:

        return render_template(
            "result.html",
            input_data="No email entered",
            result="Invalid Input",
            confidence=0
        )

    # --------------------------------------------------------
    # Suspicious keywords
    # --------------------------------------------------------

    suspicious_words = [

        "urgent",
        "verify your account",
        "verify account",
        "password",
        "login",
        "click here",
        "suspended",
        "suspend",
        "immediately",
        "security team",
        "confirm your identity",
        "otp",
        "bank",
        "payment",
        "credit card",
        "debit card",
        "limited time",
        "account verification",
        "credentials"

    ]

    text_lower = email_text.lower()

    matched_words = []

    for word in suspicious_words:

        if word in text_lower:

            matched_words.append(word)

    # --------------------------------------------------------
    # Calculate email risk
    # --------------------------------------------------------

    score = len(matched_words)

    if score >= 5:

        result = "Suspicious Email Detected"

        confidence = min(
            95.0,
            60.0 + score * 5
        )

    elif score >= 3:

        result = "Suspicious Email Detected"

        confidence = min(
            85.0,
            55.0 + score * 5
        )

    elif score >= 1:

        result = "Potentially Suspicious Email"

        confidence = 60.0

    else:

        result = "Legitimate Email"

        confidence = 85.0

    confidence = round(
        confidence,
        2
    )

    # Save email scan
    save_scan(
        email_text,
        result,
        confidence
    )

    return render_template(
        "result.html",
        input_data=email_text,
        result=result,
        confidence=confidence
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard", methods=["GET"])
def dashboard():

    scans = get_history()

    total_scans = len(scans)

    phishing_count = 0
    legitimate_count = 0

    url_scans = 0
    email_scans = 0

    # --------------------------------------------------------
    # Calculate statistics
    # --------------------------------------------------------

    for scan in scans:

        scan_input = str(scan[1])
        scan_result = str(scan[2]).lower()

        # Phishing
        if (
            "phishing" in scan_result
            or "suspicious" in scan_result
            or "malicious" in scan_result
        ):

            phishing_count += 1

        else:

            legitimate_count += 1

        # URL
        if (
            scan_input.startswith("http://")
            or scan_input.startswith("https://")
        ):

            url_scans += 1

        # Email
        elif (
            "Subject:" in scan_input
            or "@" in scan_input
        ):

            email_scans += 1

    # --------------------------------------------------------
    # Percentages
    # --------------------------------------------------------

    if total_scans > 0:

        phishing_percentage = round(
            phishing_count
            / total_scans
            * 100,
            2
        )

        legitimate_percentage = round(
            legitimate_count
            / total_scans
            * 100,
            2
        )

    else:

        phishing_percentage = 0
        legitimate_percentage = 0

    return render_template(
        "dashboard.html",

        total_scans=total_scans,

        phishing_count=phishing_count,

        legitimate_count=legitimate_count,

        phishing_percentage=phishing_percentage,

        legitimate_percentage=legitimate_percentage,

        url_scans=url_scans,

        email_scans=email_scans
    )


# ============================================================
# HISTORY
# ============================================================

@app.route("/history", methods=["GET"])
def history():

    scans = get_history()

    return render_template(
        "history.html",
        scans=scans
    )


# ============================================================
# GENERATE PDF SECURITY REPORT
# ============================================================

@app.route("/generate_report", methods=["POST"])
def generate_report():

    input_data = request.form.get(
        "input_data",
        ""
    )

    result = request.form.get(
        "result",
        ""
    )

    confidence = request.form.get(
        "confidence",
        "0"
    )

    # Convert confidence
    try:

        confidence = float(confidence)

    except (ValueError, TypeError):

        confidence = 0.0

    # --------------------------------------------------------
    # Generate PDF
    # --------------------------------------------------------

    try:

        report_path = generate_security_report(

            input_data=input_data,

            result=result,

            confidence=confidence

        )

        return send_file(

            report_path,

            as_attachment=True,

            download_name="AI_Phishing_Security_Report.pdf",

            mimetype="application/pdf"

        )

    except Exception as e:

        print("PDF GENERATION ERROR:")
        print(e)

        return f"""
        <html>
        <head>
            <title>PDF Generation Error</title>
        </head>

        <body>

            <h2>PDF Generation Error</h2>

            <p>{e}</p>

            <br>

            <a href="/">← Back to Home</a>

        </body>
        </html>
        """, 500


# ============================================================
# CREATE DATABASE
# ============================================================

create_database()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )