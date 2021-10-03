'''
Useful utillity functions for firemark

'''


from pathlib import Path, PurePosixPath
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import Tk


def get_file_path_from_user():
    """
    return path to chosen file
    """

    Tk().withdraw()  # Keep the root window from appearing
    filename = askopenfilename()
    return Path(filename)


def get_save_path_from_user():
    """
    return path to chosen directory
    """
    Tk().withdraw()  # Keep the root window from appearing
    filename = asksaveasfilename(defaultextension=".png", filetypes=[(
        "png file", ".png"), ("jpg file", ".jpg"), ("jpeg file", ".jpeg")])
    # pure posix for the renaming before save func in fire_mark
    return PurePosixPath(filename)
