import tkinter as tk
from logic.data import load_data, save_data

def open_goals():
    data = load_data()
    win = tk.Toplevel()
    win.title("Goals")

    entry = tk.Entry(win, width=40)
    entry.pack()

    def add_goal(gtype):
        g = entry.get()
        if g:
            data["goals"][gtype].append(g)
            save_data(data)
            entry.delete(0, tk.END)
            render()

    def render():
        text.delete("1.0", tk.END)
        for k in ["daily","monthly","yearly"]:
            text.insert(tk.END, f"\n{k.upper()}:\n")
            for g in data["goals"][k]:
                text.insert(tk.END, f"• {g}\n")

    for g in ["daily","monthly","yearly"]:
        tk.Button(win, text=g.capitalize(),
                  command=lambda g=g: add_goal(g)).pack()

    text = tk.Text(win, height=15)
    text.pack()
    render()
