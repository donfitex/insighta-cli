import requests
import os
import time
from datetime import timedelta
from dotenv import load_dotenv
from .storage import load_tokens
from insighta.auth import refresh_access_token


load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

# Assume 5-minute expiry, refresh after 3 minutes (proactive)
TOKEN_REFRESH_INTERVAL = 180  # 3 minutes in seconds

def should_refresh_token(tokens):
    """Check if tokens should be proactively refreshed based on age"""
    try:
        if not tokens:
            return True
        
        saved_at = tokens.get("_saved_at")
        if not saved_at:
            return True
        
        age = time.time() - saved_at
        print(f"🔎 Token age: {int(age)}s (refresh threshold: {TOKEN_REFRESH_INTERVAL}s)")
        return age > TOKEN_REFRESH_INTERVAL
    except Exception as exc:
        print(f"⚠️ Token refresh check failed: {exc}")
        return True

def authenticated_get(endpoint, params=None):
    tokens = load_tokens()

    # Check if logged in
    if not tokens:
        print("❌ Not logged in. Run: insighta login")
        return None

    # Proactively refresh if token is old (older than 2.5 minutes)
    if should_refresh_token(tokens):
        print("🔄 Refreshing session...")
        new_tokens = refresh_access_token()
        if not new_tokens:
            return None
        tokens = new_tokens

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

    # Fallback: If access token expired anyway, try refreshing
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