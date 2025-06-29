# app/routes/charts.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import random
from app.core.model_interface import call_model

router = APIRouter()

@router.get("/api/efficiency")
def get_efficiency():
    now = datetime.utcnow()
    data = [
        {"timestamp": (now - timedelta(minutes=i)).isoformat(), "efficiency": round(80 + random.uniform(-5, 5), 2)}
        for i in range(10)
    ]
    return JSONResponse(content=data)

@router.get("/api/anomalies/trend")
def get_anomaly_trend():
    now = datetime.utcnow()
    data = [
        {"timestamp": (now - timedelta(hours=i)).isoformat(), "anomalies": random.randint(0, 3)}
        for i in range(12)
    ]
    return JSONResponse(content=data)

@router.get("/api/maintenance/eta")
def get_maintenance_eta():
    # Sample ETA logic (could be AI-predicted)
    eta = datetime.utcnow() + timedelta(days=random.randint(3, 10))
    return JSONResponse(content={"next_maintenance_eta": eta.isoformat()})

@router.get("/api/energy/optimization")
def get_energy_optimization():
    suggestions = [
        "Reduce motor load between 2PM–4PM",
        "Switch to off-peak schedule for heavy processes",
        "Upgrade cooling system for zone 3"
    ]
    return JSONResponse(content={"suggestions": random.sample(suggestions, k=2)})

@router.get("/api/anomaly_report")
def anomaly_report():
    # Compose a prompt for Watsonx summarizing recent anomalies
    from app.data.mqtt_client import latest_payloads
    reports = []
    for asset_id, payload in latest_payloads.items():
        anomalies = {}
        for sensor, values in payload.items():
            if sensor in ("asset_id", "timestamp"): continue
            if sensor == "temperature":
                threshold = 130
            elif sensor == "vibration":
                threshold = 1.5
            elif sensor == "pressure":
                threshold = 350
            else:
                threshold = float("inf")
            anomalies[sensor] = [v for v in values if v > threshold]
        reports.append({
            "asset_id": asset_id,
            "anomalies": anomalies,
            "timestamp": payload.get("timestamp")
        })
    prompt = (
        "You are an industrial asset monitoring assistant. "
        "Given the following recent anomaly data per asset, generate a concise, human-readable summary highlighting which assets and sensors have anomalies, and any trends or urgent issues:\n\n"
        f"{reports}\n\nSummary:"
    )
    summary = call_model(prompt)
    return JSONResponse(content={"watsonx_report": summary})

@router.get("/api/efficiency_report")
def efficiency_report():
    from app.data.mqtt_client import latest_payloads
    from app.core.scoring import calculate_efficiency
    reports = []
    for asset_id, payload in latest_payloads.items():
        anomalies = {}
        for sensor, values in payload.items():
            if sensor in ("asset_id", "timestamp"): continue
            anomalies[sensor] = []
        eff = calculate_efficiency(payload, anomalies)
        reports.append({
            "asset_id": asset_id,
            "efficiency_score": eff["efficiency_score"],
            "timestamp": payload.get("timestamp")
        })
    prompt = (
        "You are an industrial asset monitoring assistant. "
        "Given the following efficiency scores per asset, generate a concise, human-readable summary highlighting top performers, underperformers, and any actionable insights:\n\n"
        f"{reports}\n\nSummary:"
    )
    summary = call_model(prompt)
    return JSONResponse(content={"watsonx_report": summary})

@router.get("/api/downtime_report")
def downtime_report():
    from app.data.mqtt_client import latest_payloads
    import random
    reports = []
    for asset_id in latest_payloads.keys():
        reports.append({
            "asset_id": asset_id,
            "downtime_minutes": random.randint(0, 120),
            "last_downtime": "2024-06-01T12:00:00Z"
        })
    prompt = (
        "You are an industrial asset monitoring assistant. "
        "Given the following downtime data per asset, generate a concise, human-readable summary highlighting which assets have the most downtime, possible causes, and recommendations to reduce downtime:\n\n"
        f"{reports}\n\nSummary:"
    )
    summary = call_model(prompt)
    return JSONResponse(content={"watsonx_report": summary})
