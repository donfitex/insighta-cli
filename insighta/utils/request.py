import requests
from .storage import load_tokens
import os

BACKEND_URL = os.getenv("BACKEND_URL")

def authenticated_get(endpoint, params=None):
    tokens = load_tokens()

    if not tokens:
        print("❌ Not logged in. Run: insighta login")
        return None

    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "X-API-Version": "1"
    }

    response = requests.get(
        f"{BACKEND_URL}{endpoint}",
        headers=headers,
        params=params
    )

    if response.status_code == 401:
        print("⚠️ Session expired. Please login again.")
        return None

    return response.json()