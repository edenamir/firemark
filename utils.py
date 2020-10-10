'''
Useful utillity functions for firemark

'''


from pathlib import Path
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter import Tk     # from tkinter import Tk for Python 3.x


def percent_to_byte(p: int):
    ''' Convert percentage to bytes between 0-255. '''
    return int(p/100*255)


def get_file_path_from_user():

    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()
    print("\n please pick a file")
    print("the picked file is:", filename)
    return Path(filename)


def get_dir_path_from_user():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    direname = askdirectory()
    print("\n please pick a folder")
    print("the picked file is:", direname)
    return Path(direname)


def printing_option():
    while True:
        try:
            printing_option = input(
                "Whould you like a single or multipule watermarks? ")
            if printing_option == "single" or printing_option == "multipule":
                break
        except:
            print("Please answer single or multipule only")
            continue
    return printing_option


def quantity():
    quantity = int(input("How many copies would you like to create? "))
    return quantity


def opacity():
    opacity = percent_to_byte(
        int(input("Enter opacity percentage: ")))
    return opacity
