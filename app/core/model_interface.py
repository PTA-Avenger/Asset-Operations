import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
BASE_URL = os.getenv("WATSONX_BASE_URL")
MODEL_ID = os.getenv("GRANITE_MODEL_ID")  # e.g., mistral-medium-2505

def get_access_token() -> str:
    token_url = "https://iam.cloud.ibm.com/identity/token"
    response = httpx.post(
        token_url,
        data={"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()
    return response.json()["access_token"]

def call_model(prompt: str) -> str:
    """
    Calls the Watsonx model with the given prompt and returns the generated text.
    """
    url = f"{BASE_URL}/ml/v1/text/generation?version=2024-05-01"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    payload = {
        "model_id": MODEL_ID,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 300
        },
        "project_id": PROJECT_ID
    }
    response = httpx.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["results"][0]["generated_text"]
