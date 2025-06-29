# app/ai/watsonx_client.py

import requests
import json
import os
from app.utils.logger import log_info

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")  # Must be set in environment
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")    # Also required
MODEL_ID = "mistral-medium-2505"
BASE_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {WATSONX_API_KEY}"
}

def call_watsonx(prompt: str, temperature=0.2, max_tokens=512) -> str:
    payload = {
        "model_id": MODEL_ID,
        "project_id": PROJECT_ID,
        "inputs": [prompt],
        "parameters": {
            "decoding_method": "greedy",
            "temperature": temperature,
            "max_new_tokens": max_tokens,
            "stop_sequences": ["\n\n"]
        }
    }

    try:
        log_info("🔗 Sending request to Watsonx...")
        response = requests.post(BASE_URL, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        generated = result["results"][0]["generated_text"]
        log_info("✅ Received response from Watsonx.")
        return generated.strip()
    except Exception as e:
        log_info(f"❌ Watsonx API error: {e}")
        return "Watsonx reasoning unavailable at this time."
