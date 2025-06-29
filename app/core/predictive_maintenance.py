# app/core/predictive_maintenance.py
import statistics, math

def estimate_rul(data: dict) -> dict:
    rul = {}
    for sensor, values in data.items():
        if sensor in ("asset_id", "timestamp"): continue
        avg = statistics.mean(values)
        std = statistics.pstdev(values)
        rul[sensor] = max(1, math.floor(100 / (std + 1)))
    return {"rul": rul}
