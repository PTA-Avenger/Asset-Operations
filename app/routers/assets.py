# app/routers/assets.py
from fastapi import APIRouter

router = APIRouter()
@router.get("/")
def list_assets():
    return {"assets": ["TURBINE-001"]}
