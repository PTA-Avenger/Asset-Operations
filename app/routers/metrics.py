# app/routers/metrics.py
from fastapi import APIRouter
from prometheus_client import Gauge, generate_latest
from app.core.scoring import calculate_efficiency
from app.data.mqtt_client import get_latest_sensor_data

router = APIRouter()
eff_gauge = Gauge("asset_efficiency", "Efficiency score of assets", ["asset_id"])

@router.get("/prometheus")
def metrics():
    for asset_id in ["TURBINE-001"]:
        data = get_latest_sensor_data(asset_id)
        if data:
            eff = calculate_efficiency(data, {})["efficiency_score"]
            eff_gauge.labels(asset_id=asset_id).set(eff)
    return generate_latest()
