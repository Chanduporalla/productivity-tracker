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
def mark_today_done():
    data = load_data()
    today = str(datetime.now().date())
    data[today] = data.get(today, 0) + 1
    save_data(data)
    messagebox.showinfo("Success", "🔥 Today's productivity logged!")

def calculate_streak():
    data = load_data()
    streak = 0
    today = datetime.now().date()

    for i in range(0, 365):
        day = str(today - timedelta(days=i))
        if day in data:
            streak += 1
        else:
            break
    return streak


# ---------------- HEATMAP ----------------
def draw_heatmap(frame):
    data = load_data()
    today = datetime.now().date()

    for i in range(28):  # 4 weeks
        for j in range(7):
            day = today - timedelta(days=(i * 7 + j))
            day_str = str(day)

            value = data.get(day_str, 0)
            color = "#ebedf0"
            if value == 1:
                color = "#9be9a8"
            elif value == 2:
                color = "#40c463"
            elif value >= 3:
                color = "#216e39"

            cell = tk.Label(frame, bg=color, width=4, height=2)
            cell.grid(row=j, column=27 - i, padx=1, pady=1)
