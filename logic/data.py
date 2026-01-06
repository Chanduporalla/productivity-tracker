import json, os

DATA_FILE = "data/data.json"

DEFAULT_DATA = {
    "tasks": {},
    "goals": {"daily": [], "monthly": [], "yearly": []},
    "skills": {},
    "projects": [],
    "finance": {"income": [], "expenses": []},
    "streak": {}
}

def load_data():
    if not os.path.exists(DATA_FILE):
        os.makedirs("data", exist_ok=True)
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA
    return json.load(open(DATA_FILE))

def save_data(data):
    json.dump(data, open(DATA_FILE, "w"), indent=4)
