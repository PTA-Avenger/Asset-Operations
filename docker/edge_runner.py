# edge_runner.py

from data import mqtt_client
from agents.anomaly_agent import analyze_data
from utils.logger import log_info
import time

if __name__ == "__main__":
    log_info("🔌 Edge AI module starting...")
    mqtt_client.start_mqtt()

    while True:
        payload = mqtt_client.get_latest_sensor_data()
        if payload:
            log_info("🧠 Running edge anomaly detection...")
            result = analyze_data(payload)
            log_info(f"📍 Edge result: {result}")
        time.sleep(10)
