import requests
import os
from dotenv import load_dotenv
from .storage import load_tokens
from insighta.auth import refresh_access_token


load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

def authenticated_get(endpoint, params=None):
    tokens = load_tokens()

    # Check if logged in
    if not tokens:
        print("❌ Not logged in. Run: insighta login")
        return None

    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "X-API-Version": "1"
    }

    # Make request
    response = requests.get(
        f"{BACKEND_URL}{endpoint}",
        headers=headers,
        params=params
    )

    # If access token expired, try refreshing
    if response.status_code == 401:
        print("🔄 Refreshing session...")

        new_tokens = refresh_access_token()

        if not new_tokens:
            return None

        headers["Authorization"] = f"Bearer {new_tokens['access_token']}"

        # retry request
        response = requests.get(
            f"{BACKEND_URL}{endpoint}",
            headers=headers,
            params=params
        )

    return response.json()