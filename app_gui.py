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
        super().__init__(self, root, *args, **kwargs)


class MenuFrame(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        super().__init__(self, root, *args, **kwargs)
        self.root = root
        self.font_list = ['arial.ttf', 'lucida bright.ttf', 'david.ttf']

        self.load_image = tk.Button(self, text="selcet image",
                                    font=font.Font(size=11), command=self.fn.pick_image)

        self.enter_text = tk.Entry(self, font=40)
        self.create_print_option()

    def create_drop_down_menu(self):
        self.chosen_font = tk.StringVar()
        self.chosen_font.set([0])
        self.select_font = tk.OptionMenu(
            self.root, self.chosen_font, *self.font_list)

    def create_print_option(self):
        self.print_option = tk.Listbox(self, selectmode="single",
                                       height=2, font=font.Font(size=11), bd=5)
        self.print_option.insert(0, "single water mark")
        self.print_option.insert(1, "water mark full page")


class SaveFrame(tk.Frame):


class GUI(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        super.__init__(self, root, *args, **kwargs)
        self.fn = FilePicker()
        self.dp = DirPicker()
        self.root = root
        self.background_image = ImageTk.PhotoImage(
            Image.open(str(r"C:\Workspace\fire_mark\bgimg.jpg")))
        self.image_frame = tk.Frame(self, bg='#5db3fb', bd=5)
        self.menu_frame = MenuFrame(self, bg='#5db3fb')
        self.save_frame = tk.Frame(self, bg='#5db3fb', bd=5)

        self.font_preview = font.Font(size=15)

        self.font_print_option = font.Font(size=11)
        self.font_show_image = font.Font(size=11)
        self.font_save_image = font.Font(size=11)

        self.show_image = tk.Button(self.save_frame, text="show preview",
                                    font=self.font_show_image)
        self.save_image = tk.Button(self.save_frame, text="selcet image",
                                    font=self.font_save_image, command=self.dp.pick_dir)
        self.background_label = tk.Label(
            self.root, image=self.background_image)

        # label buttons entrys etc...
        self.preview_label = tk.Label(
            self.root, text="preview:", font=self.font_preview)

        self.number_of_copies = tk.Entry(self.menu_frame, font=40)
        self.number_of_copies.place(rely=0.45,
                                    relwidth=1, relheight=0.15)

        # styling widgets

        # playcing widgets
        #self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.image_frame.place(relx=0.05, rely=0.1, relwidth=0.50,
                               relheight=0.85)
        self.preview_label.place(relx=0.05, rely=0.06)
        self.menu_frame.place(relx=0.65, rely=0.1, relwidth=0.30,
                              relheight=0.6)
        self.load_image.place(rely=0.05, relheight=0.15, relwidth=1)

        self.print_option.place(rely=0.25, relwidth=1, relheight=0.15)
        self.select_font.place(rely=0.65, relwidth=1, relheight=0.15)
        self.enter_text.place(rely=0.85,
                              relwidth=1, relheight=0.15)
        self.save_frame.place(relx=0.65, rely=0.8, relwidth=0.30,
                              relheight=0.15)
        self.show_image.place(rely=0.1, relheight=0.35, relwidth=1)
        self.save_image.place(rely=0.5, relheight=0.35, relwidth=1)

    """
    font_title = font.Font(size=10)
    title_label = tk.Label(root, text="preview:", font=font_preview)
    title_label.place(relx=0.05, rely=0.06)
    """
