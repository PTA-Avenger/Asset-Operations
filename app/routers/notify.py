# app/routers/notify.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/notify/test")
async def test_notification():
    return {"message": "Notification system online."}
