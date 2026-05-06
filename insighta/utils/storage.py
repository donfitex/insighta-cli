import json
import os
import time

PATH = os.path.expanduser("~/.insighta/credentials.json")

def save_tokens(data):
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    data["_saved_at"] = int(time.time())

    with open(PATH, "w") as f:
        json.dump(data, f)

def load_tokens():
    if not os.path.exists(PATH):
        return None

    with open(PATH, "r") as f:
        return json.load(f)
    
def clear_tokens():
    if os.path.exists(PATH):
        os.remove(PATH)