import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_FILE = "data.json"

# ------------------ DATA HANDLING ------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"tasks": [], "goals": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# ------------------ UI FUNCTIONS ------------------
def add_task():
    task = task_entry.get()
    if task == "":
        messagebox.showwarning("Warning", "Task cannot be empty")
        return
    data["tasks"].append({"name": task, "done": False})
    save_data()
    task_entry.delete(0, tk.END)
    refresh_tasks()

def add_goal():
    goal = goal_entry.get()
    if goal == "":
        messagebox.showwarning("Warning", "Goal cannot be empty")
        return
    data["goals"].append(goal)
    save_data()
    goal_entry.delete(0, tk.END)
    refresh_goals()

def toggle_task(index):
    data["tasks"][index]["done"] = not data["tasks"][index]["done"]
    save_data()
    refresh_tasks()

def delete_task(index):
    del data["tasks"][index]
    save_data()
    refresh_tasks()

def refresh_tasks():
    for widget in task_frame.winfo_children():
        widget.destroy()

    for i, task in enumerate(data["tasks"]):
        color = "green" if task["done"] else "black"

        task_label = tk.Label(task_frame, text=task["name"], fg=color, font=("Arial", 11))
        task_label.grid(row=i, column=0, sticky="w")

        done_btn = tk.Button(task_frame, text="✔", command=lambda i=i: toggle_task(i))
        done_btn.grid(row=i, column=1)

        del_btn = tk.Button(task_frame, text="🗑", command=lambda i=i: delete_task(i))
        del_btn.grid(row=i, column=2)

def refresh_goals():
    goal_list.delete(0, tk.END)
    for goal in data["goals"]:
        goal_list.insert(tk.END, goal)

# ------------------ MAIN WINDOW ------------------
root = tk.Tk()
root.title("Task & Goal Manager")
root.geometry("600x500")
root.config(bg="#f5f5f5")

# ------------------ TASK SECTION ------------------
tk.Label(root, text="📝 Tasks", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=5)

task_entry = tk.Entry(root, width=40, font=("Arial", 12))
task_entry.pack()

tk.Button(root, text="Add Task", command=add_task, bg="#4CAF50", fg="white").pack(pady=5)

task_frame = tk.Frame(root, bg="#f5f5f5")
task_frame.pack(pady=10)

# ------------------ GOAL SECTION ------------------
tk.Label(root, text="🎯 Goals", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=5)

goal_entry = tk.Entry(root, width=40, font=("Arial", 12))
goal_entry.pack()

tk.Button(root, text="Add Goal", command=add_goal, bg="#2196F3", fg="white").pack(pady=5)

goal_list = tk.Listbox(root, width=50, height=6)
goal_list.pack(pady=10)

# ------------------ INIT ------------------
refresh_tasks()
refresh_goals()

root.mainloop()
