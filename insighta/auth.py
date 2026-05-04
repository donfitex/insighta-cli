import requests
import webbrowser
from .utils.storage import save_tokens
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")


def login():
    print("🔐 Starting login...")

    # Step 1: Get auth URL
    res = requests.get(f"{BACKEND_URL}/auth/github?cli=true")
    data = res.json()

    auth_url = data["auth_url"]
    state = data["state"]

    print("🌍 Opening browser...")
    webbrowser.open(auth_url)

    # Step 2: Ask user for code manually (simple version)
    code = input("Paste the 'code' from callback URL here: ")

    # Step 3: Exchange code for tokens
    token_res = requests.post(
        f"{BACKEND_URL}/auth/github/callback",
        json={
            "code": code,
            "state": state
        }
    )

    token_data = token_res.json()

    if token_res.status_code != 200:
        print("❌ Login failed:", token_data)
        return

    save_tokens(token_data)

    username = token_data["user"]["username"]

    print(f"✅ Logged in as @{username}")