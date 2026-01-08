import tkinter as tk
import json, os
import calendar as calmod
from datetime import datetime, date, timedelta

# ---------------- CONFIG ----------------
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
        return {"tasks": []}
    with open(FILE, "r") as f:
        data = json.load(f)

    for t in data["tasks"]:
        t.setdefault("created", str(date.today()))
        t.setdefault("completed_on", None)
    return data

def save_data():
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# ---------------- TASK LOGIC ----------------
def add_task():
    name = task_entry.get().strip()
    deadline = deadline_entry.get().strip()
    if not name or not deadline:
        return

    data["tasks"].append({
        "name": name,
        "deadline": deadline,
        "done": False,
        "created": str(date.today()),
        "completed_on": None
    })
    save_data()
    task_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    refresh_all()

def toggle_task(i):
    t = data["tasks"][i]
    t["done"] = not t["done"]
    t["completed_on"] = str(date.today()) if t["done"] else None
    save_data()
    refresh_all()

def delete_task(i):
    del data["tasks"][i]
    save_data()
    refresh_all()

# ---------------- FILTER ----------------
def apply_filter(task):
    today = date.today()
    try:
        d = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
    except:
        d = today
    return True

# ---------------- TASK UI ----------------
def load_tasks():
    for w in task_list.winfo_children():
        w.destroy()

    search = search_entry.get().lower()
    today = date.today()

    for i, t in enumerate(data["tasks"]):
        if search and search not in t["name"].lower():
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
                  command=lambda i=i: toggle_task(i)).pack(side="right")

        tk.Button(row, text="🗑", bg=BTN, fg=FG,
                  command=lambda i=i: delete_task(i)).pack(side="right")

# ---------------- CALENDAR ----------------
def open_calendar():
    win = tk.Toplevel(root)
    win.title("Pick Date")
    win.configure(bg=BG)

    year = tk.IntVar(value=date.today().year)
    month = tk.IntVar(value=date.today().month)
    day = tk.IntVar(value=date.today().day)

    def update_days():
        max_day = calmod.monthrange(year.get(), month.get())[1]
        day_spin.config(to=max_day)
        if day.get() > max_day:
            day.set(max_day)

    def set_date():
        deadline_entry.delete(0, tk.END)
        deadline_entry.insert(0, f"{year.get()}-{month.get():02}-{day.get():02}")
        win.destroy()

    for label, var, start, end in [
        ("Year", year, 2024, 2035),
        ("Month", month, 1, 12),
        ("Day", day, 1, 31)
    ]:
        f = tk.Frame(win, bg=BG)
        f.pack(pady=4)
        tk.Label(f, text=label, fg=FG, bg=BG).pack(side="left")
        spin = tk.Spinbox(f, from_=start, to=end,
                          textvariable=var, width=8,
                          command=update_days,
                          bg=BTN, fg=FG)
        spin.pack(side="left")
        if label == "Day":
            day_spin = spin

    update_days()
    tk.Button(win, text="Set Date", bg=GREEN, command=set_date).pack(pady=10)

# ---------------- WEEKLY CHART ----------------
def draw_weekly_chart():
    chart.delete("all")
    today = date.today()

    counts = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        counts.append(
            sum(1 for t in data["tasks"] if t["completed_on"] == str(d))
        )

    max_val = max(counts + [1])
    x = 30

    for i, val in enumerate(counts):
        height = int((val / max_val) * 150)
        chart.create_rectangle(x, 200-height, x+40, 200, fill=BLUE)
        chart.create_text(x+20, 215, text=(today - timedelta(days=6-i)).strftime("%a"), fill=FG)
        chart.create_text(x+20, 190-height, text=str(val), fill=FG)
        x += 60

# ---------------- STATS ----------------
def load_stats():
    total = len(data["tasks"])
    done = sum(1 for t in data["tasks"] if t["done"])
    stats_label.config(text=f"📊 Total: {total} | Done: {done} | Pending: {total-done}")

# ---------------- UI ----------------
def refresh_all():
    load_tasks()
    load_stats()
    root.after(100, draw_weekly_chart)  # prevents UI freeze

root = tk.Tk()
root.title("Task & Goal Manager PRO")
root.geometry("1100x700")
root.configure(bg=BG)

top = tk.Frame(root, bg=BG)
top.pack(pady=10)

task_entry = tk.Entry(top, width=30, bg=BTN, fg=FG)
task_entry.grid(row=0, column=0, padx=5)

deadline_entry = tk.Entry(top, width=15, bg=BTN, fg=FG)
deadline_entry.grid(row=0, column=1, padx=5)

tk.Button(top, text="📅 Pick Date", bg=BLUE, command=open_calendar).grid(row=0, column=2)
tk.Button(top, text="Add Task", bg=GREEN, command=add_task).grid(row=0, column=3)

search_entry = tk.Entry(root, width=30, bg=BTN, fg=FG)
search_entry.pack()
search_entry.bind("<KeyRelease>", lambda e: load_tasks())

task_list = tk.Frame(root, bg=BG)
task_list.pack(pady=10)

stats_label = tk.Label(root, bg=BG, fg=FG)
stats_label.pack()

chart = tk.Canvas(root, width=420, height=230, bg=BG, highlightthickness=0)
chart.pack(pady=10)

refresh_all()
root.mainloop()
