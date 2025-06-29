# app/routers/ai.py
from fastapi import APIRouter
from app.data.mqtt_client import get_latest_sensor_data
from app.agents.anomaly_agent import detect_anomalies
from app.core.scoring import calculate_efficiency
from app.core.predictive_maintenance import estimate_rul
from app.core.recommender import recommend
from app.services.notifier import send_alert

router = APIRouter()

@router.get("/analyze/{asset_id}")
def analyze(asset_id: str):
    data = get_latest_sensor_data(asset_id)
    if not data:
        return {"error": "No data for asset"}

    anomalies = detect_anomalies(data)
    efficiency = calculate_efficiency(data, anomalies)
    rul = estimate_rul(data)
    recs = recommend(data, anomalies, efficiency)

    if anomalies and any(anomalies.values()):
        send_alert("Anomaly detected", str(anomalies))

    return {
        "data": data,
        "anomalies": anomalies,
        "efficiency": efficiency,
        "maintenance_eta": rul,
        "recommendations": recs,
    }
