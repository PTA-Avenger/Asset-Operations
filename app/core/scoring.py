# app/core/scoring.py
def calculate_efficiency(data: dict, anomalies: dict) -> dict:
    score = 100
    for sensor, anoms in anomalies.items():
        if anoms:
            score -= len(anoms) * 5
    score = max(min(score, 100), 0)
    return {"efficiency_score": score}
