import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime, timedelta
import threading
import time
import random

DATA_FILE = "data.json"

# ---------------- DATA HANDLING ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- STREAK LOGIC ----------------
