import tkinter as tk
from ui.tasks import DailyTasksUI

def main():
    root = tk.Tk()
    root.title("Chandu OS")
    root.geometry("500x550")
    DailyTasksUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
