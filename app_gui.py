'''

GUI for fire_mark

'''
from tkinter import font
import tkinter as tk
from tkinter import ttk
from tkinter.constants import COMMAND
import utils
from fire_mark import FireMark, Options
from PIL import Image, ImageTk
import math


class FilePicker():

    def __init__(self):
        self.path = None

    def pick_image(self):
        self.path = utils.get_file_path_from_user()


class DirPicker():
    def __init__(self):
        self.path = None

    def pick_dir(self):
        self.path = utils.get_save_path_from_user()


class PreviewFrame(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

    def display_image(self):
        self.chosen_image = Image.open(str(self.root.chosen_image_path.path))
        self.frame_width = self.winfo_width()
        self.frame_height = self.winfo_height()
        self.image_resize = ImageTk.PhotoImage(self.resize_image(
            self.chosen_image, self.frame_width, self.frame_height))
        self.display_label = tk.Label(
            self, image=self.image_resize)
        self.display_label.pack(side="top", fill="both", expand=True)

    def resize_image(self, image, frame_width, frame_height):
        import pdb
        pdb.set_trace()
        img_width, img_height = image.size
        width_ratio = img_width/frame_width
        height_ratio = img_height/frame_height
        new_width = img_width/max(height_ratio, width_ratio)
        new_height = img_height/max(height_ratio, width_ratio)
        print(new_width, new_height)
        return image.resize((int(new_width), int(new_height)), Image.ANTIALIAS)


class MenuFrame(tk.Frame):

    '''
    MenuFrame will define all widgets responsible for the options of the menu

    number of copies 
    text or random 
    opacity
    font options
    single water mark or full page

    '''

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.font_list = ['arial.ttf', 'JOKERMAN.TTF', 'david.ttf']
        self.load_image_btn = tk.Button(self, text="Selcet image",
                                        font=font.Font(size=11), command=self.load_image)
        self.selected_mark_option = tk.StringVar()
        self.single_mark = ttk.Radiobutton(
            self, text='single', value='single', variable=self.selected_mark_option)
        self.full_page_mark = ttk.Radiobutton(
            self, text='full page', value='full', variable=self.selected_mark_option)

        self.enter_text = tk.Entry(self, font=30)
        self.enter_text.insert(0, "Enter text")

        self.create_drop_down_menu()

        self.number_of_copies = tk.Entry(self, font=30)
        self.number_of_copies.insert(0, "Number of copies")

        self.text_opacity = tk.Scale(
            self, from_=1, to=100, orient="horizontal")

    def create_drop_down_menu(self):
        self.combo = ttk.Combobox(self, value=self.font_list)
        self.combo.current(0)

    def load_image(self):
        self.root.chosen_image_path.pick_image()
        self.root.preview_frame.display_image()


class SaveFrame(tk.Frame):
    '''
    SaveFrame will define all widgets responsible for the save options

    show preview
    run and save copies

    '''

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        self.show_image = tk.Button(self, text="Show preview",
                                    font=font.Font(size=11))
        self.save_image = tk.Button(self, text="Save",
                                    font=font.Font(size=11), command=self.export_image)

        self.show_image.place(rely=0.1, relheight=0.35, relwidth=1)
        self.save_image.place(rely=0.5, relheight=0.35, relwidth=1)

    def check_value(self):
        if(self.root.menu_frame.single_mark_check.state()):
            return "single"
        else:
            return "full page"

    def export_image(self):
        self.root.save_path.pick_dir()
        self.text = self.root.menu_frame.enter_text.get()
        self.opacity = self.root.menu_frame.text_opacity.get()
        self.number_of_copies = self.root.menu_frame.number_of_copies.get()
        self.font = self.root.menu_frame.combo.get()
        self.printing_option = self.root.menu_frame.selected_mark_option.get()
        self.options = Options(
            self.printing_option, int(self.number_of_copies), self.opacity, self.font, self.root.chosen_image_path.path, self.root.save_path.path, self.text)

        self.firemark = FireMark(self.options)
        self.firemark.watermark_process()


class GUI(tk.Frame):

    '''
    GUI will pack all widgets to the grid. config the widgets as the user needs
    maybe convert to a grid system for easier(?) placing

    '''

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.dic = {}
        self.chosen_image_path = FilePicker()
        self.save_path = DirPicker()
        self.root = root
        self.preview_frame = PreviewFrame(self, bg='#232426')
        self.menu_frame = MenuFrame(self, bg='#232426')
        self.save_frame = SaveFrame(self, bg='#232426')

        # self.background_label = tk.Label(
        #    self, bg='#0d0e10')
        # self.image_label=
        # placing widgets
        #self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # self.background_label.lower()

        # self.image_label.place(relx=0.3, rely=0.15, relwidth=0.5,
        #                       relheight=0.75)

        self.preview_frame.place(relx=0.3, rely=0.1, relwidth=0.6,
                                 relheight=0.8)
        self.menu_frame.place(relx=0.05, rely=0.15, relwidth=0.20,
                              relheight=0.6)

        self.save_frame.place(relx=0.05, rely=0.8, relwidth=0.20,
                              relheight=0.1)

        self.menu_frame.load_image_btn.place(
            relheight=0.10, relwidth=1)
        self.menu_frame.single_mark.place(rely=0.15, relx=0.2,
                                          relwidth=0.2)
        self.menu_frame.full_page_mark.place(rely=0.15, relx=0.6,
                                             relwidth=0.25)
        self.menu_frame.combo.place(
            rely=0.65, relwidth=1, relheight=0.10)
        self.menu_frame.enter_text.place(rely=0.85, relx=0.4,
                                         relwidth=0.6, relheight=0.10)

        self.menu_frame.number_of_copies.place(rely=0.45,
                                               relwidth=1, relheight=0.10)
        self.menu_frame.text_opacity.place(
            rely=0.25, relheight=0.10, relwidth=1)
    """
    font_title = font.Font(size=10)
    title_label = tk.Label(root, text="preview:", font=font_preview)
    title_label.place(relx=0.05, rely=0.06)
    """
