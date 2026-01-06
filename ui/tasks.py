import tkinter as tk
from datetime import datetime
from logic.data import load_data, save_data
from logic.streaks import update_streak

def open_tasks():
    data = load_data()
    today = str(datetime.now().date())

    win = tk.Toplevel()
    win.title("Daily Tasks")
    win.geometry("400x500")

    entry = tk.Entry(win, width=30)
    entry.pack(pady=5)

    def add_task():
        t = entry.get()
        if not t: return
        data["tasks"].setdefault(today, []).append({"text": t, "done": False})
        save_data(data)
        entry.delete(0, tk.END)
        render()

    def toggle(i):
        data["tasks"][today][i]["done"] ^= True
        completed = all(t["done"] for t in data["tasks"][today])
        update_streak(data, completed)
        save_data(data)
        render()

    def render():
        for w in frame.winfo_children():
            w.destroy()
        for i, t in enumerate(data["tasks"].get(today, [])):
            cb = tk.Checkbutton(frame, text=t["text"],
                                command=lambda i=i: toggle(i))
            if t["done"]: cb.select()
            cb.pack(anchor="w")

    tk.Button(win, text="Add Task", command=add_task).pack()
    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True)
    render()
