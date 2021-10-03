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
    """
    A class used to change style of ttk widgets
    Create a stlyle object
    """

    def __init__(self):

        style = ttk.Style()
        # Change background and text color of radio buttons
        style.configure("BW.TRadiobutton", foreground="white",
                        background=BG_COLOR)


class FilePicker():
    """
    A class used to save path of an image

    Methods
    ----------
    pick_image()
        save selected image path to self.path

    """

    def __init__(self):
        self.path = None

    def pick_image(self):
        self.path = utils.get_file_path_from_user()


class DirPicker():
    """
    A class used to save path of an image

    Methods
    ----------
    pick_dir()
        save selected directory path to self.path

    """

    def __init__(self):
        self.path = None

    def pick_dir(self):
        self.path = utils.get_save_path_from_user()


class PreviewFrame(tk.Frame):
    """
    A class used to represent the preview portion of the gui

    Attributes
    ---------
    root : tk.TK
        The main screen of the app
    max_ratio : int
        The max ratio of image hight or width to frame hight or width
        (default is 1)
    display_canvas : PreviewCanvas
        The widget where the image is displayed
    chosen_image : Image
        The image user chose to mark
    image_resize : Image
        The resized chosen image according to max ratio

    Methods
    ----------
    display_image():
        Create a PreviewCanvas class and display resized image
    pick_image()
        save selected image path to self.path

    """

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.max_ratio = 1
        # Created here to be able to change later
        self.display_canvas = PreviewCanvas(self, bg='white', bd=0)

    def display_image(self):
        self.chosen_image = Image.open(str(self.root.chosen_image_path.path))
        # Save Image type of resized image
        self.image_resize = self.resize_image(
            self.chosen_image, self.winfo_width(), self.winfo_height())
        font_size_ratio = int(int(
            self.root.menu_frame.combo_size.get())/self.max_ratio)
        # Initialize the image to be displayed
        self.display_canvas.initialize_display(image=self.image_resize, text_str=self.root.menu_frame.enter_text.get(),
                                               font=self.root.menu_frame.combo_font.get(), font_size=str(font_size_ratio))
        self.display_canvas.pack(
            side="bottom", fill="both", expand=True)

    def resize_image(self, image, frame_width, frame_height):
        """Create a resized version of original image 
           according to max retio

        Calculate hight and width ratios between image and frame.
        Cave max ratio so image will be a big as possible 
        Resize image.

        Parameters
        ----------
        image : Image
            The image to resize
        frame_width : int
            The width of the frame the image will be displayed in
        frame_height : int
            The heigt of the frame the image will be displayed in
        Returns
        -------
        Image
        resized image
        """
        img_width, img_height = image.size
        width_ratio = img_width/frame_width
        height_ratio = img_height/frame_height
        self.max_ratio = max(height_ratio, width_ratio)
        new_width = img_width/self.max_ratio
        new_height = img_height/self.max_ratio
        return image.resize((int(new_width), int(new_height)), Image.ANTIALIAS)


class MenuFrame(tk.Frame):

    """
    A class to define all widgets responsible for the options of the menu
    image loading, single water mark or full page,number of copies,
    opacity of font,font type and size.

    Attributes
    ----------
    root : tk.TK
        The main screen of the app
    font_list : str list
        The list of all avaliable font types
    font size : int list
        The list of all avaliable font sizes
    select_button_image : ImageTk.PhotoImage
        The image of load image button
    load_image_btn : tk.Button
        The button for loading an image
    watermark_type_label : tk.Label
        Text- 'Type Of Watermark:'
    single_mark : ttk.Radiobutton
        The radiobutton to watermark in a unique space 
    full_page_mark : ttk.Radiobutton
        The radiobutton to watermark multipule watermarks on the image
    enter_text : tk.Entry
        The entry for the text of the watermark.
        not avaliable with multiple copies
    font_label : tk.Label
        Text- 'Font Style:'
    font_size_label : tk.Label
        Text- 'Font Size'
    number_of_copies : tk.Entry
        The entry for number of copies
    opacity_label : tk.Label
        Text- 'Opacity Of Watermark'
    text_opacity : tk.Scale
        The scale to represent precentage of opacity 1-100.

    Methods
    -------
    font_style_drop_down()
        Create drop down menu of font types
    font_size_drop_down()   
        Create drop down menu of font sizes
    load_image()
        User picks image and path is sent to display_image func

    Issues
    ------
    Opacity of text is not reflected on display of single watermark.
    Can't create watermark without number of copies.
    """

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        # Avaliable font types
        self.font_list = ['arial.ttf', 'jokerman.TTF',
                          'david.ttf']
        # Avaliable font sizes
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
        """Create a drop down menu for font types.

            Defluat font style is ariel.ttf 
        """
        self.combo_font = ttk.Combobox(self, value=self.font_list)
        self.combo_font.current(0)

    def font_size_drop_down(self):
        """Create a drop down menu for font sizes.

           Ranges from 8-100 defluat font size is 8
        """
        self.combo_size = ttk.Combobox(self, value=self.font_size)
        self.combo_size.current(0)

    def load_image(self):
        """User picks image and path is sent to display_image func.

           Call pick_image to save a path of the image.
           Calls display_image to display image on preview_frame.
        """
        self.root.chosen_image_path.pick_image()
        self.root.preview_frame.display_image()


class SaveFrame(tk.Frame):
    '''
    A class to define all widgets responsible saveing and previewing images

    Attributes
    ---------
    root : tk.TK
        The main screen of the app
    save_button_image : ImageTk.PhotoImage
        The image of save_image button
    preview_button_image : ImageTk.PhotoImage
        The image of preview_image button
    preview_image : tk.Button
        The button for displaying an image
    save_image : tk.Button
        The button for saving an image

    Methods
    -------
    applay_changes()
        collect changes of preferences and display the updated image
    export_image()
        execute saving of watermarked image
    create_options()
        create an Option class based on the parameters 
        gathered from user
    calc_position()
        return the coordinates of text relative to the original image
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
        """collect changes of preferences and display the updated image.

            Create an option class. 
            If printing options is single, send resized image to display
            by calling update_image.
            Update position,font and size of text by calling update_text
            else printing option is full page, create a firemark class
            and display the watermarkd image and not a preview. 
            Update text to an empty str by calling update_text
            (defalut is full page)

        """
        options = self.create_options(False)
        if options.printing_option == 'single':
            self.root.preview_frame.display_canvas.update_image(
                self.root.preview_frame.image_resize)
            self.root.preview_frame.display_canvas.update_text(
                options.text, options.font, options.font_size)
        else:  # full page
            firemark = FireMark(options)
            image_new = firemark.add_watermark(
                options.text, self.root.preview_frame.image_resize)
            self.root.preview_frame.display_canvas.update_image(
                image_new)
            self.root.preview_frame.display_canvas.update_text(
                "", options.font, 0)

    def export_image(self):
        """execute saving of watermarked image.

        Create a firemark class by calling create_options 
        and execute the watermarking and saving procces

        """
        self.firemark = FireMark(self.create_options(True))
        self.firemark.watermark_process()

    def create_options(self, to_save=False):
        """Create an Option class based on the parameters 
           collected from menu_frame widgets .
        If the argument to_save isn't passed in, defalut is False

        Parameters
        ----------
        to_save : Bool
            True if image is saved False if image is displayed
            (default is False)
        Returns
        -------
        Options
            an option class used for displaying image or saving
        """
        if to_save:
            self.root.save_path.pick_dir()
            font_size_ratio = int(
                self.root.menu_frame.combo_size.get())
            # Add the relative position of text to options
            position_ratio = self.calc_position()
        else:
            # Add the real size of the text to options
            font_size_ratio = int(int(
                self.root.menu_frame.combo_size.get())/self.root.preview_frame.max_ratio)
            # Add the real position of text to options
            position_ratio = self.root.preview_frame.display_canvas.get_position()
        return Options(
            self.root.menu_frame.selected_mark_option.get(), int(self.root.menu_frame.number_of_copies.get(
            )), self.root.menu_frame.text_opacity.get(), self.root.menu_frame.combo_font.get(),
            font_size_ratio, self.root.chosen_image_path.path,
            self.root.save_path.path, self.root.menu_frame.enter_text.get(), position_ratio)

    def calc_position(self):
        """Calculate the real position of text for the original image.

        get position of text on resized image and multiply it by max_ratio.

        Returns
        -------
        tuple
            a tuple containing x,y coordinates of text.
        """
        x, y = self.root.preview_frame.display_canvas.get_position()
        return (x*self.root.preview_frame.max_ratio, y*self.root.preview_frame.max_ratio)


class GUI(tk.Frame):

    """
    A class to initialise frames and place all frame's widgets on the root.

    Attributes
    ---------
    style : StyleManager
        A class to configure ttk widgets design
    chosen_image_path : FilePicker
        A class to save image path
    save_path : DirPicker
        A class to save directory path
    root : tk.TK
        The main screen of the app
    back_image : ImageTk.PhotoImage
        The image of background label
    background_label : tk.Label
        The label for the background of the app
    preview_frame : PreviewFrame
        A class for displaying an image
    menu_frame : MenuFrame
        A class for the option menu
    save_frame : SaveFrame
        A class for saving an image and updating display

    """

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
        # Position the background lower than frames
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
                                               relwidth=1, relheight=0.08)
        self.menu_frame.opacity_label.place(rely=0.25)
        self.menu_frame.text_opacity.place(
            rely=0.3, relheight=0.10, relwidth=1)
        self.menu_frame.enter_text.place(rely=0.8,
                                         relwidth=0.6, relheight=0.08)

        # Placing save and preview widgets
        self.save_frame.preview_image.place(
            rely=0.1, relheight=0.4, relwidth=1)
        self.save_frame.save_image.place(rely=0.55, relheight=0.4, relwidth=1)
