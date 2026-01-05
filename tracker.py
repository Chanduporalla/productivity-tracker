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
# ---------------- ANALYTICS ----------------
def weekly_analytics():
    data = load_data()
    total = 0
    for i in range(7):
        day = str(datetime.now().date() - timedelta(days=i))
        total += data.get(day, 0)

    messagebox.showinfo(
        "Weekly Analytics",
        f"📊 Last 7 days productivity score: {total}\n🔥 Average/day: {round(total/7,2)}"
    )

# ---------------- AI REWARDS ----------------
def ai_reward():
    streak = calculate_streak()
    rewards = [
        "🎧 Listen to your favorite music",
        "☕ Take a coffee break",
        "📺 Watch one episode guilt-free",
        "📖 Read something non-academic",
        "🚶 Take a short walk",
        "🔥 Post your streak on LinkedIn 😄"
    ]

    if streak >= 7:
        reward = random.choice(rewards)
        messagebox.showinfo("AI Reward 🎁", f"Streak: {streak} days\nReward: {reward}")
    else:
        messagebox.showinfo("Keep Going 💪", f"Current streak: {streak}\nReach 7 days for rewards!")


# ---------------- REMINDER ----------------
def reminder_loop():
    while True:
        time.sleep(3600)  # every 1 hour
        messagebox.showinfo("Reminder ⏰", "Have you logged your productivity today?")

# ---------------- UI ----------------
root = tk.Tk()
root.title("🔥 Productivity Streak Tracker")
root.geometry("900x500")
root.configure(bg="#0d1117")

title = tk.Label(root, text="GitHub-Style Productivity Tracker", fg="white", bg="#0d1117",
                 font=("Arial", 18, "bold"))
title.pack(pady=10)

streak_label = tk.Label(root, text=f"🔥 Current Streak: {calculate_streak()} days",
                        fg="#58a6ff", bg="#0d1117", font=("Arial", 14))
streak_label.pack(pady=5)

btn_frame = tk.Frame(root, bg="#0d1117")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="✅ Mark Today Done", command=mark_today_done, width=20).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="📊 Weekly Analytics", command=weekly_analytics, width=20).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="🎁 Get AI Reward", command=ai_reward, width=20).grid(row=0, column=2, padx=5)

heatmap_frame = tk.Frame(root, bg="#0d1117")
heatmap_frame.pack(pady=20)

draw_heatmap(heatmap_frame)

# Start reminder thread
threading.Thread(target=reminder_loop, daemon=True).start()

root.mainloop()