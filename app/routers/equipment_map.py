# app/routes/equipment_map.py
from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter()

class EquipmentLocation(BaseModel):
    id: str
    name: str
    lat: float
    lon: float
    status: str  # e.g., "online", "offline", "maintenance"

# Temporary mock data (to be connected to real DB or MQTT later)
@router.get("/api/assets/locations", response_model=List[EquipmentLocation])
def get_asset_locations():
    return [
        {"id": "EQ001", "name": "Pump Station A", "lat": -26.2, "lon": 28.0, "status": "online"},
        {"id": "EQ002", "name": "Valve B", "lat": -26.3, "lon": 27.9, "status": "maintenance"},
        {"id": "EQ003", "name": "Turbine C", "lat": -26.25, "lon": 28.1, "status": "offline"}
    ]
