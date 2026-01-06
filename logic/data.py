import json, os

FILE = "data/data.json"

def load():
    if not os.path.exists(FILE):
        return {
            "tasks": {},
            "streak": {},
            "skills": {},
            "projects": [],
            "finance": {"income": [], "expenses": []}
        }
    return json.load(open(FILE))

def save(data):
    os.makedirs("data", exist_ok=True)
    json.dump(data, open(FILE, "w"), indent=4)
