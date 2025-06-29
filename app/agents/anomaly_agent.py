# app/core/anomaly_agent.py
from app.config import settings

def detect_anomalies(data: dict) -> dict:
    anomalies = {}
    for sensor, values in data.items():
        if sensor in ("asset_id", "timestamp"): continue
        thresh = settings.anomaly_thresholds.get(sensor, float("inf"))
        anomalies[sensor] = [v for v in values if v > thresh]
    return anomalies
