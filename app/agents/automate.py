# app/agents/automate.py

from app.utils.logger import log_info

def trigger_automation(reasoning: dict) -> str:
    """
    Simulate automated actions based on reasoning.
    """
    log_info("Triggering automation based on reasoning...")

    # Get the reasoning summary or actions as a string
    reasoning_text = reasoning.get("summary", "")  # or reasoning.get("actions", "")

    if "maintenance" in reasoning_text.lower():
        return "✅ Maintenance ticket generated and assigned to Technician #17."
    elif "normal operations" in reasoning_text.lower():
        return "✅ System continues real-time monitoring."
    else:
        return "⚠️ Action logged. Awaiting manual review."
