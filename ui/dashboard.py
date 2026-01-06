import tkinter as tk
from logic.data import load_data, save_data
from logic.streaks import get_streak_count
from ui.tasks import open_tasks
from ui.goals import open_goals
from ui.skills import open_skills
from ui.projects import open_projects
from ui.finance import open_finance
from ui.focus import open_focus

def launch_dashboard():
    data = load_data()

    root = tk.Tk()
    root.title("Chandu OS")
    root.geometry("900x600")
    root.configure(bg="#0d1117")

    tk.Label(root, text="CHANDU OS",
             font=("Arial", 22, "bold"),
             fg="white", bg="#0d1117").pack(pady=10)

    tk.Label(root,
             text=f"🔥 Streak: {get_streak_count(data)} days",
             fg="#58a6ff", bg="#0d1117",
             font=("Arial", 14)).pack(pady=5)

    btns = [
        ("Daily Tasks", open_tasks),
        ("Goals", open_goals),
        ("Skills", open_skills),
        ("Projects", open_projects),
        ("Finance", open_finance),
        ("Focus Mode", open_focus)
    ]

    for text, cmd in btns:
        tk.Button(root, text=text, width=25,
                  command=lambda c=cmd: c()).pack(pady=4)

    root.mainloop()
