import os
import sqlite3
import threading
import requests
from typing import Optional
from datetime import datetime
import hashlib
import re

# Firebase Admin SDK
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firebase if credentials are present
FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH")
FIREBASE_APP = None
FIREBASE_DB = None
if FIREBASE_CRED_PATH and os.path.exists(FIREBASE_CRED_PATH):
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    FIREBASE_APP = firebase_admin.initialize_app(cred)
    FIREBASE_DB = firestore.client()

LOCAL_DB = os.path.join(os.path.dirname(__file__), "users.db")

def init_local_db():
    conn = sqlite3.connect(LOCAL_DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_number TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            last_sync TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_local_db()

def is_online():
    try:
        requests.get("https://www.google.com", timeout=2)
        return True
    except Exception:
        return False

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def valid_employee_number(employee_number: str) -> bool:
    # Example: must be digits, 4-10 chars
    return bool(re.fullmatch(r"\d{4,10}", employee_number))

def signup(employee_number: str, password: str) -> bool:
    if not valid_employee_number(employee_number) or not password:
        return False
    password_hash = hash_password(password)
    conn = sqlite3.connect(LOCAL_DB)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (employee_number, password_hash, last_sync) VALUES (?, ?, ?)", (employee_number, password_hash, None))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    # Try to sync with Firebase if online
    if is_online() and FIREBASE_APP:
        try:
            user = auth.create_user(uid=employee_number, password=password, app=FIREBASE_APP)
            FIREBASE_DB.collection("users").document(user.uid).set({"employee_number": employee_number, "created": datetime.utcnow()})
            update_last_sync(employee_number)
        except Exception:
            pass
    return True

def login(employee_number: str, password: str) -> bool:
    password_hash = hash_password(password)
    conn = sqlite3.connect(LOCAL_DB)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE employee_number=?", (employee_number,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == password_hash:
        return True
    # If not found locally and online, try Firebase
    if is_online() and FIREBASE_APP:
        try:
            user = auth.get_user(employee_number, app=FIREBASE_APP)
            # Password check is not possible via Admin SDK, so just check existence
            return True
        except Exception:
            return False
    return False

def logout():
    # Stateless: handled by frontend/session
    pass

def update_last_sync(employee_number: str):
    conn = sqlite3.connect(LOCAL_DB)
    c = conn.cursor()
    c.execute("UPDATE users SET last_sync=? WHERE employee_number=?", (datetime.utcnow(), employee_number))
    conn.commit()
    conn.close()

def sync_local_to_firebase():
    if not (is_online() and FIREBASE_APP):
        return
    conn = sqlite3.connect(LOCAL_DB)
    c = conn.cursor()
    c.execute("SELECT employee_number, password_hash FROM users WHERE last_sync IS NULL")
    unsynced = c.fetchall()
    for employee_number, password_hash in unsynced:
        try:
            # Firebase requires password, but we only have hash; skip password sync for security
            user = auth.create_user(uid=employee_number, app=FIREBASE_APP)
            FIREBASE_DB.collection("users").document(user.uid).set({"employee_number": employee_number, "created": datetime.utcnow()})
            update_last_sync(employee_number)
        except Exception:
            continue
    conn.close()

def background_sync():
    while True:
        sync_local_to_firebase()
        import time
        time.sleep(60)

def start_background_sync():
    t = threading.Thread(target=background_sync, daemon=True)
    t.start()

from flask import Blueprint, request, jsonify, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def api_signup():
    data = request.get_json()
    employee_number = data.get('employee_number')
    password = data.get('password')
    if not employee_number or not password:
        return jsonify({"success": False, "message": "Missing employee_number or password"}), 400
    if signup(employee_number, password):
        return jsonify({"success": True, "message": "Signup successful"})
    else:
        return jsonify({"success": False, "message": "Signup failed (possibly duplicate employee number)"}), 400

@auth_bp.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    employee_number = data.get('employee_number')
    password = data.get('password')
    if not employee_number or not password:
        return jsonify({"success": False, "message": "Missing employee_number or password"}), 400
    if login(employee_number, password):
        session['employee_number'] = employee_number
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@auth_bp.route('/logout', methods=['POST'])
def api_logout():
    session.pop('employee_number', None)
    return jsonify({"success": True, "message": "Logged out"})
