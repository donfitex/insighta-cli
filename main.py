import click
import webbrowser
import secrets
import os
from dotenv import load_dotenv
from utils.pkce import generate_pkce

load_dotenv()

YOUR_CLIENT_ID = os.getenv("CLIENT_ID")
BACKEND_URL = os.getenv("BACKEND_URL")

@click.group()
def cli():
    pass

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