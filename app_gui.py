'''

GUI for fire_mark

'''
from tkinter import font
import tkinter as tk
from tkinter import ttk
import utils
from fire_mark import FireMark
from PIL import Image, ImageTk


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
    # here the picture will be shown
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

    '''
    display_image:
    param1: file_path(path) 
    pack the picked image for water marking on screen 
    '''

    def display_image(self, file_path):

        self.img = ImageTk.PhotoImage(
            Image.open(str(file_path)))
        self.display_label = tk.Label(
            self, image=self.img)
        self.display_label.pack()
        print("hello")


'''
MenuFrame will define all widgets responsible for the options of the menu

number of copies 
text or random 
opacity
font options
single water mark or full page

'''


class MenuFrame(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.font_list = ['arial.ttf', 'lucida bright.ttf', 'david.ttf']
        self.load_image_btn = tk.Button(self, text="Selcet image",
                                        font=font.Font(size=11), command=self.load_image)
        self.random_check = tk.Checkbutton(
            self, text='Random', onvalue=1, offvalue=0)

        self.enter_text = tk.Entry(self, font=30)
        self.enter_text.insert(0, "Enter text")

        self.create_drop_down_menu()

        # self.create_print_option()

        self.number_of_copies = tk.Entry(self, font=30)
        self.number_of_copies.insert(0, "Number of copies")
        # not suppose to be here move to outside func
        self.chosen_num = self.number_of_copies.get()

        self.text_opacity = tk.Scale(
            self, from_=1, to=100, orient="horizontal")
        # not suppose to be here move to outside func
        self.chosen_opacity = self.text_opacity.get()

    def create_drop_down_menu(self):
        self.combo = ttk.Combobox(self, value=self.font_list)
        self.combo.current(0)
        #self.combo.bind("<<ComboboxSelected>>", selected)

    def load_image(self):
        self.root.fn.pick_image()
        self.root.image_frame.display_image(self.root.fn.path)

        # self.chosen_font = tk.StringVar()
        # self.chosen_font.set("choose font")
        # self.select_font = tk.OptionMenu(
        #     self, self.chosen_font, *self.font_list)
        # self.chosen_font = self.chosen_font.get()


'''
    def create_print_option(self):
        self.print_option = tk.Listbox(self, selectmode="single",
                                       height=2, font=font.Font(size=11), bd=5)
        self.print_option.insert(0, "single water mark")
        self.print_option.insert(1, "water mark full page")
        self.chosen_option = self.print_option.get(
            self.print_option.curselection())
'''

'''
SaveFrame will define all widgets responsible for the save options

show preview
run and save copies

'''


class SaveFrame(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        self.show_image = tk.Button(self, text="Show preview",
                                    font=font.Font(size=11))
        self.save_image = tk.Button(self, text="Save",
                                    font=font.Font(size=11), command=self.export_image)

        self.show_image.place(rely=0.1, relheight=0.35, relwidth=1)
        self.save_image.place(rely=0.5, relheight=0.35, relwidth=1)
        self.firemark = FireMark()

    def export_image(self):
        self.root.dp.pick_dir()
        self.firemark.save_folder = self.root.dp.path
        self.firemark.image_path = self.root.fn.path
        self.firemark.watermark_process(self.root.menu_frame.enter_text.get())


'''
GUI will pack all widgets to the grid. config the widgets as the user needs
maybe convert to a grid system for easier(?) placing

'''


class GUI(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.dic = {}
        self.fn = FilePicker()
        self.dp = DirPicker()
        self.root = root

        self.image_frame = PreviewFrame(self, bg='#0d0e10')
        self.menu_frame = MenuFrame(self, bg='#232426')
        self.save_frame = SaveFrame(self, bg='#232426')

        self.background_label = tk.Label(
            self, bg='#0d0e10')

        # label buttons entrys etc...
        self.preview_label = tk.Label(
            self, text="preview:", font=font.Font(size=15))

        self.single_mode = tk.Button(self, text="Single",
                                     font=font.Font(size=11))
        self.batch_mode = tk.Button(self, text="Batch",
                                    font=font.Font(size=11))

        # placing widgets
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.lower()
        '''
        self.image_frame.place(relx=0.05, rely=0.1, relwidth=0.50,
                               relheight=0.85)
                               '''
        self.preview_label.place(relx=0.05, rely=0.06)
        self.menu_frame.place(relx=0.05, rely=0.15, relwidth=0.20,
                              relheight=0.4)

        self.save_frame.place(relx=0.05, rely=0.8, relwidth=0.20,
                              relheight=0.1)

        self.single_mode.place(relx=0.05, rely=0.1)
        self.batch_mode.place(relx=0.1, rely=0.1)
        '''
self.menu_frame.print_option.place(
rely=0.25, relwidth=1, relheight=0.15)
'''
        self.menu_frame.combo.place(
            rely=0.65, relwidth=1, relheight=0.15)
        self.menu_frame.enter_text.place(rely=0.85, relx=0.4,
                                         relwidth=0.6, relheight=0.15)
        self.menu_frame.random_check.place(rely=0.85, relx=0,
                                           relwidth=0.2)
        self.menu_frame.load_image_btn.place(
            rely=0.05, relheight=0.15, relwidth=1)
        self.menu_frame.number_of_copies.place(rely=0.45,
                                               relwidth=1, relheight=0.15)
        self.menu_frame.text_opacity.place(
            rely=0.25, relheight=0.15, relwidth=1)
    """
    font_title = font.Font(size=10)
    title_label = tk.Label(root, text="preview:", font=font_preview)
    title_label.place(relx=0.05, rely=0.06)
    """
