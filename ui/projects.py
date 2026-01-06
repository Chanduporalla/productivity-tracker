import tkinter as tk
from logic.data import load_data, save_data

def open_projects():
    data = load_data()
    win = tk.Toplevel()
    win.title("Projects")

    entry = tk.Entry(win)
    entry.pack()

    def add():
        p = entry.get()
        if p:
            data["projects"].append({"name": p, "status": "Building"})
            save_data(data)
            entry.delete(0, tk.END)
            render()

    def render():
        text.delete("1.0", tk.END)
        for p in data["projects"]:
            text.insert(tk.END, f"{p['name']} - {p['status']}\n")

    tk.Button(win, text="Add Project", command=add).pack()
    text = tk.Text(win)
    text.pack()
    render()
