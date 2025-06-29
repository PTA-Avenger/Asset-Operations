# app/agents/reasoning_agent.py

from app.utils.logger import log_info
from app.ai.watsonx_client import call_watsonx

def generate_reasoning(analysis: dict) -> str:
    """
    Converts the analysis into a prompt and sends it to IBM Watsonx
    for reasoning generation using mistral-medium-2505.
    """
    log_info("🧠 Generating reasoning using Watsonx...")

    if not analysis or "summary" not in analysis:
        log_info("⚠️ No valid analysis to reason about.")
        return "No analysis data available for reasoning."

    prompt = (
        f"You are an industrial AI expert. Based on the following analysis of "
        f"sensor data, provide a professional reasoning and recommendation:\n\n"
        f"{analysis['summary']}\n\n"
        f"Respond concisely in plain English."
    )

    reasoning = call_watsonx(prompt)
    log_info("💡 Reasoning completed.")
    return reasoning
