# app/core/recommender.py
def recommend(data: dict, anomalies: dict, efficiency: dict) -> dict:
    recs = []
    if any(anomalies.values()):
        recs.append("🔧 Schedule maintenance ASAP due to anomalies.")
    if efficiency["efficiency_score"] < 80:
        recs.append("💡 Investigate efficiency drop.")
    return {"recommendations": recs or ["All systems optimal."]}
