import tkinter as tk
from logic.data import load_data, save_data

def open_skills():
    data = load_data()
    win = tk.Toplevel()
    win.title("Skills")

    entry = tk.Entry(win)
    entry.pack()

    def add():
        s = entry.get()
        if s:
            data["skills"][s] = data["skills"].get(s, 0) + 1
            save_data(data)
            entry.delete(0, tk.END)
            render()

    def render():
        text.delete("1.0", tk.END)
        for k,v in data["skills"].items():
            text.insert(tk.END, f"{k}: {v} hrs\n")

    tk.Button(win, text="Log Skill Hour", command=add).pack()
    text = tk.Text(win)
    text.pack()
    render()
