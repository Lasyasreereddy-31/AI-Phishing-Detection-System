import sqlite3
import os

DATABASE_NAME = "database/phishing.db"


# -----------------------------------------
# Create Database
# -----------------------------------------

def create_database():

    # Make sure database folder exists
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


# -----------------------------------------
# Save Scan
# -----------------------------------------

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


# -----------------------------------------
# Get Scan History
# -----------------------------------------

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


# -----------------------------------------
# Save Email Scan
# -----------------------------------------

def save_email_scan(email, result, confidence):

    # Reuse the same scan_history table
    save_scan(email, result, confidence)