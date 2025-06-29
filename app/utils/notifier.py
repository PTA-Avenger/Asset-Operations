# app/utils/notifier.py

from app.utils.logger import log_info

def notify_team(message: str):
    log_info(f"NOTIFICATION SENT: {message}")
