'''

GUI for fire_mark

'''
from tkinter import font
import tkinter as tk
from tkinter import ttk
import utils
from fire_mark import FireMark, Options
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
        self.path = utils.get_save_path_from_user()


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
        '''
        self.random_check = tk.Checkbutton(
            self, text='Random', onvalue=1, offvalue=0)
        '''
        # self.single_mark_check = ttk.Checkbutton(
        #    self, text='Single')
        # self.full_page_mark_check = ttk.Checkbutton(
        #    self, text='Full page')

        self.selected_mark_option = tk.StringVar()
        self.single_mark = ttk.Radiobutton(
            self, text='single', value='single', variable=self.selected_mark_option)
        self.full_page_mark = ttk.Radiobutton(
            self, text='full page', value='full', variable=self.selected_mark_option)

        self.enter_text = tk.Entry(self, font=30)
        self.enter_text.insert(0, "Enter text")

        self.create_drop_down_menu()

        # self.create_print_option()

        self.number_of_copies = tk.Entry(self, font=30)
        self.number_of_copies.insert(0, "Number of copies")

        self.text_opacity = tk.Scale(
            self, from_=1, to=100, orient="horizontal")

    def create_drop_down_menu(self):
        self.combo = ttk.Combobox(self, value=self.font_list)
        self.combo.current(0)
        #self.combo.bind("<<ComboboxSelected>>", selected)

    def load_image(self):
        self.root.chosen_image_path.pick_image()
        self.root.image_frame.display_image(
            self.root.chosen_image_path.path)  # why here????

        # self.chosen_font = tk.StringVar()
        # self.chosen_font.set("choose font")
        # self.select_font = tk.OptionMenu(
        #     self, self.chosen_font, *self.font_list)
        # self.chosen_font = self.chosen_font.get()


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
        self.printing_option = self.root.menu_frame.selected_mark_option.get()
        self.options = Options(
            self.printing_option, int(self.number_of_copies), self.opacity, self.root.chosen_image_path.path, self.root.save_path.path, self.text)

        self.firemark = FireMark(self.options)
        self.firemark.watermark_process()


'''
GUI will pack all widgets to the grid. config the widgets as the user needs
maybe convert to a grid system for easier(?) placing

'''


class GUI(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.dic = {}
        self.chosen_image_path = FilePicker()
        self.save_path = DirPicker()
        self.root = root

        self.image_frame = PreviewFrame(self, bg='#0d0e10')
        self.menu_frame = MenuFrame(self, bg='#232426')
        self.save_frame = SaveFrame(self, bg='#232426')

        self.background_label = tk.Label(
            self, bg='#0d0e10')

        # placing widgets
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.lower()
        '''
        self.image_frame.place(relx=0.05, rely=0.1, relwidth=0.50,
                               relheight=0.85)
                               '''

        self.menu_frame.place(relx=0.05, rely=0.15, relwidth=0.20,
                              relheight=0.6)

        self.save_frame.place(relx=0.05, rely=0.8, relwidth=0.20,
                              relheight=0.1)

        '''
self.menu_frame.print_option.place(
rely=0.25, relwidth=1, relheight=0.15)
'''
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
#        self.menu_frame.random_check.place(rely=0.85, relx=0.1,
#                                          relwidth=0.25)

        self.menu_frame.number_of_copies.place(rely=0.45,
                                               relwidth=1, relheight=0.10)
        self.menu_frame.text_opacity.place(
            rely=0.25, relheight=0.10, relwidth=1)
    """
    font_title = font.Font(size=10)
    title_label = tk.Label(root, text="preview:", font=font_preview)
    title_label.place(relx=0.05, rely=0.06)
    """
