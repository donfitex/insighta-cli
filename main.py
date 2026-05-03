import threading
import click
import webbrowser
import secrets
import requests
import os
from dotenv import load_dotenv
from utils.pkce import generate_pkce
from flask import Flask, request
from utils.storage import save_tokens

load_dotenv()

YOUR_CLIENT_ID = os.getenv("CLIENT_ID")
BACKEND_URL = os.getenv("BACKEND_URL")

@click.group()
def cli():
    pass
# Command to initiate the login process
@cli.command()
def login():
    print("Starting login...")
    state = secrets.token_urlsafe(16)
    code_verifier, code_challenge = generate_pkce()

    auth_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={YOUR_CLIENT_ID}"
        f"&redirect_uri={BACKEND_URL}/callback"
        f"&state={state}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )

    webbrowser.open(auth_url)

    print("Opened browser for authentication")
if __name__ == "__main__":
    cli()

app = Flask(__name__)
# This route will handle the callback from GitHub after authentication
@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")
    code_verifier = request.args.get("code_verifier")

    response = requests.post(
        f"{BACKEND_URL}/auth/github/callback",
        json={
            "code": code,
            "code_verifier": code_verifier,
            "state": state
        }
    )

    data = response.json()

    save_tokens(data)

    print("Received callback")
    print("Code:", code)

    print("Logged in as:", data.get("username"))
    
    return "Login successful. You can close this window."

# Start the Flask server in a separate thread to handle the callback
def run_server():
    app.run(port=8000)

threading.Thread(target=run_server).start()