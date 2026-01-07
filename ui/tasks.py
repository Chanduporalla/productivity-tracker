import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

from logic.data import load_data, save_data, today
from logic.streaks import calculate_streak

class DailyTasksUI:
    def __init__(self, root):
        self.root = root
        self.data = load_data()
        self.today = today()

        self.carry_forward_tasks()
        self.build_ui()
        self.render_tasks()

    # ---------- CORE LOGIC ----------

    def carry_forward_tasks(self):
        yesterday = str(datetime.now().date() - timedelta(days=1))

        if yesterday in self.data["tasks"]:
            unfinished = [
                t for t in self.data["tasks"][yesterday]
                if not t["done"]
            ]
            if unfinished:
                self.data["tasks"].setdefault(self.today, [])
                self.data["tasks"][self.today].extend(unfinished)
                save_data(self.data)

    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            return

        self.data["tasks"].setdefault(self.today, []).append({
            "text": text,
            "done": False
        })
        save_data(self.data)
        self.task_entry.delete(0, tk.END)
        self.render_tasks()

    def toggle_task(self, index):
        task = self.data["tasks"][self.today][index]
        task["done"] = not task["done"]

        tasks_today = self.data["tasks"][self.today]

        if tasks_today and all(t["done"] for t in tasks_today):
            self.data["streak"][self.today] = True
        else:
            self.data["streak"].pop(self.today, None)

        save_data(self.data)
        self.update_streak()
        self.render_tasks()

    # ---------- UI ----------

    def build_ui(self):
        self.root.configure(bg="#0d1117")

        tk.Label(
            self.root,
            text="CHANDU OS — DAILY EXECUTION",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#0d1117"
        ).pack(pady=10)

        self.streak_label = tk.Label(
            self.root,
            text="",
            fg="#58a6ff",
            bg="#0d1117",
            font=("Arial", 13)
        )
        self.streak_label.pack()

        self.update_streak()

        self.task_entry = tk.Entry(self.root, width=40, font=("Arial", 12))
        self.task_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="➕ Add Task",
            command=self.add_task,
            width=20
        ).pack(pady=5)

        self.task_frame = tk.Frame(self.root, bg="#0d1117")
        self.task_frame.pack(pady=10, fill="both", expand=True)

    def render_tasks(self):
        for w in self.task_frame.winfo_children():
            w.destroy()

        for i, task in enumerate(self.data["tasks"].get(self.today, [])):
            var = tk.BooleanVar(value=task["done"])
            cb = tk.Checkbutton(
                self.task_frame,
                text=task["text"],
                variable=var,
                command=lambda i=i: self.toggle_task(i),
                fg="white",
                bg="#0d1117",
                selectcolor="#0d1117",
                font=("Arial", 11)
            )
            cb.pack(anchor="w", pady=2)

    def update_streak(self):
        streak = calculate_streak(self.data["streak"])
        self.streak_label.config(text=f"🔥 Current Streak: {streak} days")
