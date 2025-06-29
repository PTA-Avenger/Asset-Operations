# app/services/notifier.py
from app.config import settings
from app.utils.logger import log_info

def send_alert(subject: str, message: str):
    log_info(f"🔔 ALERT: {subject} — {message}")
