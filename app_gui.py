'''

GUI for fire_mark

'''
from tkinter import PhotoImage, font
import tkinter as tk
from tkinter import ttk
from tkinter.constants import COMMAND
import utils
from fire_mark import FireMark, Options
from PIL import Image, ImageTk
import math
from preview_canvas import PreviewCanvas

BG_COLOR = '#3F51B5'


class StyleManager():

    def __init__(self):
        style = ttk.Style()
        style.configure("BW.TRadiobutton", foreground="white",
                        background=BG_COLOR)


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
        self.max_ratio = 1
        self.display_canvas = PreviewCanvas(self, bg='white', bd=0)

    def display_image(self):
        self.chosen_image = Image.open(str(self.root.chosen_image_path.path))

        self.image_resize = self.resize_image(
            self.chosen_image, self.winfo_width(), self.winfo_height())
        font_size_ratio = int(int(
            self.root.menu_frame.combo_size.get())/self.max_ratio)
        self.display_canvas.initialize_display(image=ImageTk.PhotoImage(self.image_resize), text_str=self.root.menu_frame.enter_text.get(),
                                               font=self.root.menu_frame.combo_font.get(), font_size=str(font_size_ratio))
        self.display_canvas.pack(
            side="bottom", fill="both", expand=True)

    def resize_image(self, image, frame_width, frame_height):
        img_width, img_height = image.size
        width_ratio = img_width/frame_width
        height_ratio = img_height/frame_height
        self.max_ratio = max(height_ratio, width_ratio)
        new_width = img_width/self.max_ratio
        new_height = img_height/self.max_ratio
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
        self.font_list = ['arial.ttf', 'jokerman.TTF', 'david.ttf']
        self.font_size = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50,
                          52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100]
        self.select_button_image = ImageTk.PhotoImage(Image.open(
            r"C:\Workspace\fire_mark\gui\button_select-image.png"))

        self.load_image_btn = tk.Button(self, image=self.select_button_image,
                                        font=font.Font(size=11), command=self.load_image, borderwidth=0, bg=BG_COLOR)
        self.selected_mark_option = tk.StringVar()
        self.watermark_type_label = tk.Label(
            self, text='Type Of Watermark:', font=font.Font(size=11), bg=BG_COLOR, fg='white')
        self.single_mark = ttk.Radiobutton(
            self, text='Single', value='single', style="BW.TRadiobutton", variable=self.selected_mark_option)
        self.full_page_mark = ttk.Radiobutton(
            self, text='Full Page', value='full', style="BW.TRadiobutton", variable=self.selected_mark_option)

        self.enter_text = tk.Entry(self, font=11, borderwidth=0)
        self.enter_text.insert(0, "Enter Text")
        self.font_label = tk.Label(
            self, text='Font Style:', font=font.Font(size=11), bg=BG_COLOR, fg='white')
        self.font_style_drop_down()
        self.font_size_label = tk.Label(
            self, text='Font Size:', font=font.Font(size=11), bg=BG_COLOR, fg='white')
        self.font_size_drop_down()

        self.number_of_copies = tk.Entry(self, font=11, borderwidth=0)
        self.number_of_copies.insert(0, "Number Of Copies")

        self.opacity_label = tk.Label(
            self, text='Opacity Of Watermark:', font=font.Font(size=11), bg=BG_COLOR, fg='white')
        self.text_opacity = tk.Scale(
            self, from_=1, to=100, orient="horizontal", bg=BG_COLOR, bd=0, fg='white')

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
        self.save_button_image = ImageTk.PhotoImage(Image.open(
            r"C:\Workspace\fire_mark\gui\button_save-image.png"))
        self.preview_button_image = ImageTk.PhotoImage(Image.open(
            r"C:\Workspace\fire_mark\gui\button_preview-image.png"))
        self.preview_image = tk.Button(self, image=self.preview_button_image,
                                       font=font.Font(size=11), command=self.applay_changes, borderwidth=0, bg=BG_COLOR)
        self.save_image = tk.Button(self, image=self.save_button_image,
                                    font=font.Font(size=11), command=self.export_image, borderwidth=0, bg=BG_COLOR)

    # Allow passing of the inner function because parameter is hard coded

    def applay_changes(self):
        options = self.create_options(0)
        if options.printing_option == 'single':
            self.root.preview_frame.display_canvas.update_image(
                self.root.preview_frame.display_canvas.image)
            self.root.preview_frame.display_canvas.update_text(options)
        else:  # full page
            firemark = FireMark(options)
            image_new = ImageTk.PhotoImage(
                firemark.add_watermark(options.text, self.root.preview_frame.image_resize))
            self.root.preview_frame.display_canvas.update_image(image_new)

    def export_image(self):

        self.firemark = FireMark(self.create_options(1))
        self.firemark.watermark_process()

    def create_options(self, to_save):
        if to_save == 1:
            self.root.save_path.pick_dir()
            font_size_ratio = int(
                self.root.menu_frame.combo_size.get())
            position_ratio = self.calc_position()
        else:
            font_size_ratio = int(int(
                self.root.menu_frame.combo_size.get())/self.root.preview_frame.max_ratio)
            position_ratio = self.root.preview_frame.display_canvas.get_position()
        return Options(
            self.root.menu_frame.selected_mark_option.get(), int(self.root.menu_frame.number_of_copies.get(
            )), self.root.menu_frame.text_opacity.get(), self.root.menu_frame.combo_font.get(),
            font_size_ratio, self.root.chosen_image_path.path,
            self.root.save_path.path, self.root.menu_frame.enter_text.get(), position_ratio)

    def calc_position(self):
        x, y = self.root.preview_frame.display_canvas.get_position()
        return (x*self.root.preview_frame.max_ratio, y*self.root.preview_frame.max_ratio)


class GUI(tk.Frame):

    '''
    GUI will pack all widgets to the grid. config the widgets as the user needs
    maybe convert to a grid system for easier(?) placing

    '''

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.style = StyleManager()
        self.chosen_image_path = FilePicker()
        self.save_path = DirPicker()
        self.root = root
        self.back_image = ImageTk.PhotoImage(Image.open(
            r"C:\Workspace\fire_mark\gui\back.png"))
        self.background_label = tk.Label(self, image=self.back_image)
        self.preview_frame = PreviewFrame(self, bg='white')
        self.menu_frame = MenuFrame(self, bg=BG_COLOR)
        self.save_frame = SaveFrame(self, bg=BG_COLOR)
        self.background_label.place(relwidth=1, relheight=1)
        self.background_label.lower()
        self.preview_frame.place(relx=0.3, rely=0.1, relwidth=0.6,
                                 relheight=0.8)
        self.menu_frame.place(relx=0.05, rely=0.15, relwidth=0.15,
                              relheight=0.6)

        self.save_frame.place(relx=0.05, rely=0.7, relwidth=0.15,
                              relheight=0.17)
        # Placing menu widgets
        self.menu_frame.load_image_btn.place(
            relheight=0.12, relwidth=1)

        self.menu_frame.watermark_type_label.place(rely=0.12)
        self.menu_frame.single_mark.place(rely=0.18, relx=0.15,
                                          relwidth=0.25)
        self.menu_frame.full_page_mark.place(rely=0.18, relx=0.55,
                                             relwidth=0.35)
        self.menu_frame.font_label.place(rely=0.6)
        self.menu_frame.combo_font.place(
            rely=0.65, relwidth=0.45, relheight=0.1)
        self.menu_frame.font_size_label.place(rely=0.6, relx=0.55)
        self.menu_frame.combo_size.place(
            rely=0.65, relx=0.55, relwidth=0.45, relheight=0.1)
        self.menu_frame.number_of_copies.place(rely=0.45,
                                               relwidth=1, relheight=0.10)
        self.menu_frame.opacity_label.place(rely=0.25)
        self.menu_frame.text_opacity.place(
            rely=0.3, relheight=0.10, relwidth=1)
        self.menu_frame.enter_text.place(rely=0.8,
                                         relwidth=0.6, relheight=0.10)

        # Placing save and preview widgets
        self.save_frame.preview_image.place(
            rely=0.1, relheight=0.4, relwidth=1)
        self.save_frame.save_image.place(rely=0.55, relheight=0.4, relwidth=1)
