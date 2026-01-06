import tkinter as tk
import time, threading

def open_focus():
    win = tk.Toplevel()
    win.title("Focus Mode")

    lbl = tk.Label(win, text="25:00", font=("Arial", 30))
    lbl.pack()

    def start():
        for i in range(25*60, -1, -1):
            m,s = divmod(i,60)
            lbl.config(text=f"{m:02}:{s:02}")
            time.sleep(1)

    threading.Thread(target=start, daemon=True).start()
