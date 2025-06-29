# app/routes/sensors.py

from fastapi import APIRouter
from app.data.mqtt_client import get_latest_sensor_data
from fastapi.responses import JSONResponse
import json

router = APIRouter()

@router.get("/api/sensors/latest")
def get_latest_data():
    payload = get_latest_sensor_data()
    try:
        data = json.loads(payload)
        return JSONResponse(content=data)
    except Exception:
        return JSONResponse(content={"error": "No valid data yet."}, status_code=404)
