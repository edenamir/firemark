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
from preview_canvas import PreviewCanvas


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
        self.display_canvas = PreviewCanvas(
            self, image=self.image_resize, text_str=self.root.menu_frame.enter_text.get(),
            font=self.root.menu_frame.combo_font.get(), font_size=self.root.menu_frame.combo_size.get(), height=self.frame_height, width=self.frame_width)
        self.display_canvas.pack(
            side="bottom", fill="both", expand=True)

    def resize_image(self, image, frame_width, frame_height):
        img_width, img_height = image.size
        width_ratio = img_width/frame_width
        height_ratio = img_height/frame_height
        new_width = img_width/max(height_ratio, width_ratio)
        new_height = img_height/max(height_ratio, width_ratio)
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
        self.font_size = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50,
                          52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100]
        self.load_image_btn = tk.Button(self, text="Selcet image",
                                        font=font.Font(size=11), command=self.load_image)
        self.selected_mark_option = tk.StringVar()
        self.single_mark = ttk.Radiobutton(
            self, text='single', value='single', variable=self.selected_mark_option)
        self.full_page_mark = ttk.Radiobutton(
            self, text='full page', value='full', variable=self.selected_mark_option)

        self.enter_text = tk.Entry(self, font=20)
        self.enter_text.insert(0, "Enter text")

        self.font_style_drop_down()
        self.font_size_drop_down()

        self.number_of_copies = tk.Entry(self, font=20)
        self.number_of_copies.insert(0, "Number of copies")

        self.text_opacity = tk.Scale(
            self, from_=1, to=100, orient="horizontal")

    def font_style_drop_down(self):
        self.combo_font = ttk.Combobox(self, value=self.font_list)
        self.combo_font.current(0)

    def font_size_drop_down(self):
        self.combo_size = ttk.Combobox(self, value=self.font_size)
        self.combo_size.current(0)

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

        self.preview_image = tk.Button(self, text="Show preview",
                                       font=font.Font(size=11), command=self.root.preview_frame.display_canvas.update_text(self.create_options()))
        self.save_image = tk.Button(self, text="Save",
                                    font=font.Font(size=11), command=self.export_image)

        self.preview_image.place(rely=0.1, relheight=0.35, relwidth=1)
        self.save_image.place(rely=0.5, relheight=0.35, relwidth=1)

    def export_image(self):

        self.firemark = FireMark(self.create_options())
        self.firemark.watermark_process()

    def create_options(self):
        self.root.save_path.pick_dir()
        return Options(
            self.root.menu_frame.selected_mark_option.get(), int(self.root.menu_frame.number_of_copies.get(
            )), self.root.menu_frame.text_opacity.get(), self.root.menu_frame.combo_font.get(),
            int(self.root.menu_frame.combo_size.get()
                ), self.root.chosen_image_path.path,
            self.root.save_path.path, self.root.menu_frame.enter_text.get(), self.root.preview_frame.display_canvas.get_position())


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
        self.menu_frame.combo_font.place(
            rely=0.65, relwidth=0.45, relheight=0.1)
        self.menu_frame.combo_size.place(
            rely=0.65, relx=0.55, relwidth=0.45, relheight=0.1)
        self.menu_frame.enter_text.place(rely=0.85,
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
