import requests
import webbrowser
from .utils.storage import save_tokens
import os
from dotenv import load_dotenv
from insighta.utils.pkce import generate_pkce
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import secrets
import threading

from .utils.storage import load_tokens, save_tokens, clear_tokens

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
# -------------------------
# Local server handler
# -------------------------
class CallbackHandler(BaseHTTPRequestHandler):
    SESSION = {
        "state": None,
        "verifier": None,
        "code": None
    }

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)

        CallbackHandler.SESSION["code"] = query.get("code", [None])[0]
        CallbackHandler.SESSION["state"] = query.get("state", [None])[0]

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Login successful. You can close this tab.")

    def log_message(self, format, *args):
        return

# -------------------------
# Start local server
# -------------------------
def start_server():
    server = HTTPServer(("127.0.0.1", 8765), CallbackHandler)
    thread = threading.Thread(target=server.handle_request)
    thread.start()
    return server


# -------------------------
# LOGIN
# -------------------------
def login():
    print("🔐 Starting login...")
    state = secrets.token_urlsafe(16)
    # Generate PKCE code verifier and challenge
    verifier, challenge = generate_pkce()

    CallbackHandler.SESSION["state"] = state
    CallbackHandler.SESSION["verifier"] = verifier
    CallbackHandler.SESSION["code"] = None

    # start local server
    start_server()

    # Step 1: Get auth URL
    res = requests.get(
        f"{BACKEND_URL}/auth/github",
        params={
            "cli": "true",
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "code_verifier": verifier,
            "state": state,
        }
    )

    if res.status_code != 200:
        print("Failed to get auth URL:", res.text)
        return

    data = res.json()
    auth_url = data.get("auth_url")
    if not auth_url:
        print("No auth_url in response:", data)
        return

    verifier = data.get("code_verifier", verifier)
    state = data.get("state", state)
    CallbackHandler.SESSION["verifier"] = verifier
    CallbackHandler.SESSION["state"] = state

    print("🌍 Opening browser...")
    webbrowser.open(auth_url)

    # Step 2: Ask user for code manually (simple version)
    print("⏳ Waiting for authentication...")

    # wait until callback fills data
    while CallbackHandler.SESSION["code"] is None:
        pass

    code = CallbackHandler.SESSION["code"]
    state = CallbackHandler.SESSION["state"]
    verifier = CallbackHandler.SESSION["verifier"]


    print("🔄 Exchanging token...")

    # Step 3: Exchange code for tokens
    token_res = requests.post(
        f"{BACKEND_URL}/auth/exchange",
        json={
            "code": code,
            "state": state,
            "code_verifier": verifier,
        }
    )


    try:
        token_data = token_res.json()
    except ValueError:
        token_data = {
            "status": "error",
            "message": token_res.text or f"HTTP {token_res.status_code}"
        }

    if token_res.status_code != 200:
        print("❌ Login failed:", token_data)
        return

    save_tokens(token_data)

    username = token_data["user"]["username"]

    print(f"✅ Logged in as @{username}")


# -------------------------
# REFRESH TOKEN 
# -------------------------
def refresh_access_token():
    tokens = load_tokens()

    if not tokens:
        print("❌ Not logged in")
        return None

    refresh_token = tokens.get("refresh_token")

    response = requests.post(
        f"{BACKEND_URL}/auth/refresh",
        json={"refresh_token": refresh_token}
    )

    if response.status_code != 200:
        print("❌ Session expired. Please login again.")
        return None

    new_tokens = response.json()

    save_tokens(new_tokens)

    return new_tokens

# -------------------------
# LOGOUT 
# -------------------------
def logout():
    tokens = load_tokens()

    if not tokens:
        print("❌ Not logged in")
        return

    refresh_token = tokens.get("refresh_token")

    response = requests.post(
        f"{BACKEND_URL}/auth/logout",
        json={"refresh_token": refresh_token}
    )

    # Always clear locally (important)
    clear_tokens()

    if response.status_code == 200:
        print("✅ Logged out successfully")
    else:
        print("⚠️ Logged out locally (server session may already be invalid)")

# -------------------------
# WHOAMI
# -------------------------
def whoami():
    tokens = load_tokens()

    if not tokens:
        print("❌ Not logged in")
        return

    user = tokens.get("user")

    if not user:
        print("⚠️ No user info found")
        return

    print("\n👤 Current User:")
    print(f"Username: @{user.get('username')}")
    print(f"Role: {user.get('role')}")
    print(f"User ID: {user.get('id')}")