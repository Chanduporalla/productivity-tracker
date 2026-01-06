import tkinter as tk
from logic.data import load_data, save_data

def open_finance():
    data = load_data()
    win = tk.Toplevel()
    win.title("Finance")

    inc = tk.Entry(win)
    exp = tk.Entry(win)
    inc.pack()
    exp.pack()

    def add_income():
        data["finance"]["income"].append(float(inc.get()))
        save_data(data)

    def add_expense():
        data["finance"]["expenses"].append(float(exp.get()))
        save_data(data)

    tk.Button(win, text="Add Income", command=add_income).pack()
    tk.Button(win, text="Add Expense", command=add_expense).pack()
