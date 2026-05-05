import json
import os

PATH = os.path.expanduser("~/.insighta/credentials.json")

def save_tokens(data):
    os.makedirs(os.path.dirname(PATH), exist_ok=True)

    with open(PATH, "w") as f:
        json.dump(data, f)

def load_tokens():
    if not os.path.exists(PATH):
        return None

    with open(PATH, "r") as f:
        return json.load(f)