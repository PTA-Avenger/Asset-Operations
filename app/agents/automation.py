# app/agents/automation.py

from app.utils.logger import log_info

def trigger_automation(reasoning: str) -> str:
    """
    Simulate or trigger automation actions based on AI reasoning summary.
    """
    log_info("🔁 Processing reasoning for automation decision...")

    reasoning_lower = reasoning.lower()

    if "maintenance" in reasoning_lower or "technician" in reasoning_lower:
        return "🛠️ Maintenance task created and assigned to appropriate team."
    elif "alert" in reasoning_lower or "warning" in reasoning_lower:
        return "📣 Alert triggered in operations center."
    elif "normal operations" in reasoning_lower:
        return "✅ System continues real-time monitoring with no intervention."
    elif "optimize" in reasoning_lower or "efficiency" in reasoning_lower:
        return "⚙️ Optimization routine activated for performance tuning."
    else:
        return "📋 Action logged for manual review."
