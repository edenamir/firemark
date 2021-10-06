
import tkinter as tk
import app_gui


if __name__ == "__main__":

    root = tk.Tk()
    # Open app in full screen
    root.state('zoomed')
    root.title("Firemark")
    root.iconbitmap(r"gui\favicon.ico")
    app_gui.GUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
