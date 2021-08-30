

from fire_mark import FireMark
import tkinter as tk
import app_gui


if __name__ == "__main__":

    root = tk.Tk()
    root.geometry("1500x750")
    root.config(background='#232426')
    app_gui.GUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
