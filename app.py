import tkinter as tk
import json, os
from datetime import datetime, date

FILE = "data.json"
BG = "#121212"
FG = "#ffffff"
BTN = "#2c2c2c"
GREEN = "#4CAF50"
RED = "#FF5252"
BLUE = "#2196F3"

# ---------------- DATA ----------------
def load_data():
    if not os.path.exists(FILE):
        return {"tasks": [], "goals": []}
    with open(FILE, "r") as f:
        data = json.load(f)

    for t in data.get("tasks", []):
        t.setdefault("created", str(date.today()))
    return data

def save_data():
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# ---------------- TASKS ----------------
def add_task():
    name = task_entry.get().strip()
    deadline = deadline_entry.get().strip()

    if not name or not deadline:
        return

    data["tasks"].append({
        "name": name,
        "deadline": deadline,
        "done": False,
        "created": str(date.today())
    })
    save_data()
    task_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    refresh_all()

def toggle_task(i):
    data["tasks"][i]["done"] = not data["tasks"][i]["done"]
    save_data()
    refresh_all()

def delete_task(i):
    del data["tasks"][i]
    save_data()
    refresh_all()

# ---------------- SEARCH & FILTER ----------------
filter_var = "All"

def apply_filter(task):
    today = date.today()
    try:
        d = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
    except:
        d = today

    if filter_var == "Completed":
        return task["done"]
    if filter_var == "Pending":
        return not task["done"]
    if filter_var == "Overdue":
        return d < today and not task["done"]
    return True

def load_tasks():
    for w in task_list.winfo_children():
        w.destroy()

    search = search_entry.get().lower()
    today = date.today()

    for i, t in enumerate(data["tasks"]):
        if search and search not in t["name"].lower():
            continue
        if not apply_filter(t):
            continue

        try:
            d = datetime.strptime(t["deadline"], "%Y-%m-%d").date()
            overdue = d < today and not t["done"]
        except:
            overdue = False

        color = GREEN if t["done"] else (RED if overdue else FG)

        row = tk.Frame(task_list, bg=BG)
        row.pack(fill="x", pady=2)

        tk.Label(row, text=f"{t['name']}  ⏰ {t['deadline']}",
                 fg=color, bg=BG).pack(side="left", padx=5)

        tk.Button(row, text="✔", bg=BTN, fg=FG,
                  command=lambda i=i: toggle_task(i)).pack(side="right", padx=2)

        tk.Button(row, text="🗑", bg=BTN, fg=FG,
                  command=lambda i=i: delete_task(i)).pack(side="right", padx=2)

# ---------------- CALENDAR PICKER ----------------
def open_calendar():
    cal = tk.Toplevel(root)
    cal.title("Pick Date")
    cal.configure(bg=BG)

    year_var = tk.IntVar(value=date.today().year)
    month_var = tk.IntVar(value=date.today().month)
    day_var = tk.IntVar(value=date.today().day)

    def set_date():
        deadline_entry.delete(0, tk.END)
        deadline_entry.insert(0, f"{year_var.get()}-{month_var.get():02}-{day_var.get():02}")
        cal.destroy()

    for txt, var, start, end in [
        ("Year", year_var, 2024, 2035),
        ("Month", month_var, 1, 12),
        ("Day", day_var, 1, 31)
    ]:
        frame = tk.Frame(cal, bg=BG)
        frame.pack(pady=5)
        tk.Label(frame, text=txt, bg=BG, fg=FG).pack(side="left")
        tk.Spinbox(frame, from_=start, to=end, textvariable=var,
                   bg=BTN, fg=FG, width=8).pack(side="left")

    tk.Button(cal, text="Set Date", bg=GREEN,
              command=set_date).pack(pady=10)

# ---------------- STATS ----------------
def load_stats():
    total = len(data["tasks"])
    today = str(date.today())
    completed_today = sum(1 for t in data["tasks"]
                          if t["done"] and t["created"] == today)
    pending = sum(1 for t in data["tasks"] if not t["done"])
    percent = int((completed_today / total) * 100) if total else 0

    stats_label.config(
        text=f"📊 Today: {completed_today}/{total} completed | Pending: {pending} | {percent}%"
    )

# ---------------- UI ----------------
def refresh_all():
    load_tasks()
    load_stats()

root = tk.Tk()
root.title("Task & Goal Manager")
root.geometry("1000x650")
root.configure(bg=BG)

# ---- Top Controls ----
top = tk.Frame(root, bg=BG)
top.pack(pady=10)

task_entry = tk.Entry(top, width=30, bg=BTN, fg=FG, insertbackground=FG)
task_entry.grid(row=0, column=0, padx=5)

deadline_entry = tk.Entry(top, width=15, bg=BTN, fg=FG, insertbackground=FG)
deadline_entry.grid(row=0, column=1, padx=5)

tk.Button(top, text="📅 Pick Date", bg=BLUE,
          command=open_calendar).grid(row=0, column=2, padx=5)

tk.Button(top, text="Add Task", bg=GREEN,
          command=add_task).grid(row=0, column=3, padx=5)

# ---- Search & Filter ----
search_frame = tk.Frame(root, bg=BG)
search_frame.pack()

search_entry = tk.Entry(search_frame, width=30,
                        bg=BTN, fg=FG, insertbackground=FG)
search_entry.pack(side="left", padx=5)
search_entry.bind("<KeyRelease>", lambda e: load_tasks())

for f in ["All", "Completed", "Pending", "Overdue"]:
    tk.Button(search_frame, text=f, bg=BTN, fg=FG,
              command=lambda x=f: set_filter(x)).pack(side="left", padx=3)

def set_filter(f):
    global filter_var
    filter_var = f
    load_tasks()

# ---- Task List ----
task_list = tk.Frame(root, bg=BG)
task_list.pack(pady=10)

# ---- Stats ----
stats_label = tk.Label(root, bg=BG, fg=FG, font=("Arial", 12))
stats_label.pack(pady=10)

# ---- START ----
refresh_all()
root.mainloop()
