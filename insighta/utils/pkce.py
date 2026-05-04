import secrets
import hashlib
import base64

def generate_pkce():
    # code_verifier (secret)
    code_verifier = secrets.token_urlsafe(96)

    # code_challenge (hashed)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b'=').decode('utf-8')

    return code_verifier, code_challenge