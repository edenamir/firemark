

import utils
from fire_mark import FireMark
import tkinter as tk
import app_gui


if __name__ == "__main__":

    """
    start_print = FireMark(
        utils.printing_option(), utils.quantity(), utils.opacity(
        ), utils.get_file_path_from_user(), utils.get_dir_path_from_user()
    )
    start_print.watermark_option()
    """

    root = tk.Tk()
    root.geometry("1500x750")
    gui = app_gui.GUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
