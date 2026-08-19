# 🛡️ AI Phishing Detection System

An AI-based web application designed to detect and analyze **phishing URLs and suspicious emails**. The system uses machine learning and rule-based analysis to identify potential phishing threats and provides users with a security risk assessment and downloadable PDF report.

## 📌 Project Overview

Phishing is one of the most common cybersecurity threats used to steal sensitive information such as usernames, passwords, banking details, OTPs, and other personal information.

The **AI Phishing Detection System** provides a simple web interface where users can:

* Analyze suspicious URLs
* Analyze suspicious emails
* Detect potential phishing activity
* View confidence/risk levels
* View previous scan history
* Monitor results through a dashboard
* Generate a detailed PDF security report

## 🎯 Objectives

* Detect potentially malicious phishing URLs using machine learning.
* Identify suspicious emails using phishing-related indicators.
* Provide a confidence score for detection results.
* Maintain scan history using SQLite.
* Generate security reports in PDF format.
* Provide security recommendations to help users avoid phishing attacks.

## ✨ Key Features

### 🔗 URL Phishing Detection

Users can enter a URL into the URL Analyzer.

The system:

1. Extracts URL-related features.
2. Passes the features to the trained machine learning model.
3. Predicts whether the URL is potentially phishing or legitimate.
4. Calculates the prediction confidence.
5. Stores the scan result in the database.

### 📧 Email Phishing Detection

Users can enter an email subject and email body.

The system checks for suspicious indicators such as:

* Urgent requests
* Account verification requests
* Password-related requests
* Login requests
* OTP requests
* Banking/payment-related content
* Suspicious links or instructions
* Requests for credentials

Based on the detected indicators, the system provides a risk classification and confidence score.

### 📊 Dashboard

The dashboard provides an overview of:

* Total scans
* Phishing/suspicious scans
* Legitimate scans
* URL scans
* Email scans
* Phishing percentage
* Legitimate percentage

### 📋 Scan History

The application stores previous scans in an SQLite database so users can review earlier analysis results.

### 📄 PDF Security Report

After an analysis, the user can generate a downloadable PDF report containing information such as:

* Analyzed URL/email
* Detection result
* Confidence level
* Security risk information
* Possible phishing attack indicators
* Recommended safety actions
* Actions users should avoid

## 🧠 Technologies Used

* **Python**
* **Flask**
* **Scikit-learn**
* **Pandas**
* **Joblib**
* **SQLite**
* **HTML**
* **CSS**
* **Jinja2**
* **ReportLab**
* **Machine Learning**

## 🏗️ Project Structure

```text
AI-Phishing-Detection-System/
│
├── app.py
├── database.py
├── report_generator.py
├── requirements.txt
├── README.md
│
├── model/
│   └── phishing_model.pkl
│
├── utils/
│   └── url_features.py
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── url_analyzer.html
│   ├── email_analyzer.html
│   ├── result.html
│   └── history.html
│
├── static/
│   └── ...
│
├── dataset/
│   └── PhiUSIIL_Phishing_URL_Dataset.csv
│
└── database/
    └── phishing.db
```

> **Note:** The large phishing dataset is excluded from Git tracking because of GitHub's file-size recommendations. The application requires the dataset only for model-training workflows, not necessarily for running the already-trained application.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Lasyasreereddy-31/AI-Phishing-Detection-System.git
cd AI-Phishing-Detection-System
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

For macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python3 app.py
```

The application will run locally on:

```text
http://127.0.0.1:5000
```

Open that address in your browser.

## 🔄 System Workflow

```text
User
  ↓
Enter URL / Email
  ↓
AI Phishing Detection System
  ↓
Feature Extraction / Suspicious Indicator Analysis
  ↓
Detection
  ↓
Confidence / Risk Assessment
  ↓
Result Display
  ↓
Save Scan History
  ↓
Generate Security Report
```

## 🔐 Security Recommendations

Users should:

* Verify the sender before responding to suspicious emails.
* Check URLs carefully before opening them.
* Avoid sharing passwords or OTPs.
* Avoid clicking suspicious links.
* Use multi-factor authentication.
* Verify urgent financial requests through official channels.
* Keep operating systems and security software updated.

Users should **not**:

* Share passwords through email.
* Share OTPs with unknown persons.
* Enter banking information on suspicious websites.
* Trust messages only because they appear urgent.
* Download unknown attachments.
* Ignore browser security warnings.

## 🚀 Future Enhancements

Possible future improvements include:

* Real-time URL reputation checking
* Integration with threat intelligence APIs
* Advanced NLP-based email analysis
* Deep learning-based phishing detection
* Browser extension integration
* Automatic malicious URL reputation lookup
* Improved explainable AI results
* Cloud deployment
* User authentication
* Advanced analytics and visualization

## 👩‍💻 Project Author

**Bontha Lasya Sree Reddy**

B.Sc. Digital Forensic Science
Mallareddy University

## ⚠️ Disclaimer

This project is developed for **educational and cybersecurity research purposes**. Detection results should be treated as an aid for security analysis and should not be considered a guarantee that a website or email is completely safe or malicious.
