'''
Useful utillity functions for firemark

'''


from pathlib import Path
from tkinter.filedialog import askopenfilename
from tkinter import Tk     # from tkinter import Tk for Python 3.x


def percent_to_byte(p: int):
    ''' Convert percentage to bytes between 0-255. '''
    return int(p/100*255)


def get_path_from_user():

    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()
    print("the picked file is:", filename)
    return Path(filename)
