import json
import os
from datetime import datetime

DATA_PATH = "data/data.json"

DEFAULT_DATA = {
    "tasks": {},      # date -> list of tasks
    "streak": {}      # date -> true (completed)
}

def ensure_data_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_PATH):
        save_data(DEFAULT_DATA)

def load_data():
    ensure_data_file()
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

def today():
    return str(datetime.now().date())
