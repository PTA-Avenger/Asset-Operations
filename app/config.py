# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mqtt_broker: str = "broker.hivemq.com"
    mqtt_port: int = 1883
    mqtt_topic: str = "assetops/sensor"
    anomaly_thresholds: dict = {"temperature": 130, "vibration": 1.5, "pressure": 350}
    efficiency_min_score: int = 70
    alert_recipients: list = ["ops@example.com"]

settings = Settings()
