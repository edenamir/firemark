'''

GUI for fire_mark

'''
from tkinter import font
import tkinter as tk
import utils
from fire_mark import FireMark
from PIL import Image, ImageTk

HEIGHT = 750
WIDTH = 1000


class FilePicker():

    def __init__(self):
        self.path = None

    def pick_image(self):
        self.path = utils.get_file_path_from_user()


class DirPicker():
    def __init__(self):
        self.path = None

    def pick_dir(self):
        self.path = utils.get_dir_path_from_user()


class PreviewFrame(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)


class MenuFrame(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.font_list = ['arial.ttf', 'lucida bright.ttf', 'david.ttf']

        self.load_image = tk.Button(self, text="selcet image",
                                    font=font.Font(size=11), command=self.root.fn.pick_image)

        self.enter_text = tk.Entry(self, font=40)
        self.text = self.enter_text.get()

        self.create_drop_down_menu()

        # self.create_print_option()

        self.number_of_copies = tk.Entry(self, font=40)
        self.chosen_num = self.number_of_copies.get()

        self.text_opacity = tk.Entry(self, font=40)
        self.text_opacity = self.text_opacity.get()

    def create_drop_down_menu(self):
        self.chosen_font = tk.StringVar()
        self.chosen_font.set("choose font")
        self.select_font = tk.OptionMenu(
            self, self.chosen_font, *self.font_list)
        self.chosen_font = self.chosen_font.get()


'''
    def create_print_option(self):
        self.print_option = tk.Listbox(self, selectmode="single",
                                       height=2, font=font.Font(size=11), bd=5)
        self.print_option.insert(0, "single water mark")
        self.print_option.insert(1, "water mark full page")
        self.chosen_option = self.print_option.get(
            self.print_option.curselection())
'''


class SaveFrame(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        self.show_image = tk.Button(self, text="show preview",
                                    font=font.Font(size=11))
        self.save_image = tk.Button(self, text="save",
                                    font=font.Font(size=11), command=self.root.dp.pick_dir)

        self.show_image.place(rely=0.1, relheight=0.35, relwidth=1)
        self.save_image.place(rely=0.5, relheight=0.35, relwidth=1)


class GUI(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.dic = {}
        self.fn = FilePicker()
        self.dp = DirPicker()
        self.root = root
        '''
        self.background_image = ImageTk.PhotoImage(
            Image.open(str(r"C:\Workspace\fire_mark\bg1.jpg")))
        '''
        self.image_frame = PreviewFrame(self, bg='#6930c3')
        self.menu_frame = MenuFrame(self, bg='#64dfdf')
        self.save_frame = SaveFrame(self, bg='#47ffcb')

        self.background_label = tk.Label(
            self, bg='#252525')

        # label buttons entrys etc...
        self.preview_label = tk.Label(
            self, text="preview:", font=font.Font(size=15))

        # playcing widgets
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.lower()
        self.image_frame.place(relx=0.05, rely=0.1, relwidth=0.50,
                               relheight=0.85)
        self.preview_label.place(relx=0.05, rely=0.06)
        self.menu_frame.place(relx=0.65, rely=0.1, relwidth=0.30,
                              relheight=0.6)

        self.save_frame.place(relx=0.65, rely=0.8, relwidth=0.30,
                              relheight=0.15)

        self.menu_frame.load_image.place(rely=0.05, relheight=0.15, relwidth=1)
        self.menu_frame.number_of_copies.place(rely=0.45,
                                               relwidth=1, relheight=0.15)
        '''
self.menu_frame.print_option.place(
rely=0.25, relwidth=1, relheight=0.15)
'''
        self.menu_frame.select_font.place(
            rely=0.65, relwidth=1, relheight=0.15)
        self.menu_frame.enter_text.place(rely=0.85,
                                         relwidth=1, relheight=0.15)

    """
    font_title = font.Font(size=10)
    title_label = tk.Label(root, text="preview:", font=font_preview)
    title_label.place(relx=0.05, rely=0.06)
    """
