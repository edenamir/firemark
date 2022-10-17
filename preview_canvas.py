"""
some text for problem
"""
import tkinter as tk
from PIL import Image, ImageTk


class PreviewCanvas(tk.Canvas):
    """A class used to represent a display frame for images.

    The class can be initialized without parameters other than master
    so it can be modified later in the code.

    Attributes
    ----------
    image : ImageTk.PhotoImage
        The image for the image object
    text_str : str
        The text for the text object (defalut None)
    font : str
        The type of font (defalut None)
    font_size : int
        The size of font (defalut None)
    text_x : int (defalut None)
        The horizontal coordinate of the text object
    text_y : int (defalut None)
        The vertical coordinate of the text object
    text : text
        The text object
    canvas_image_id : image
        The image object
    image_width : int
        The width of an image
    image_height : int
        The height of an image

    Methods
    -------
    initialize_display()
        initialize image and text within the PreviewCanvas
    change_position()
        change position of text object
    get_position()
        return coordinates of text
    update_text()
        update text object parameters
    update_image()
        update image object parameters
    image()
        getter for image
    image.setter()
        set any image as ImageTk.PhotoImage type

    """

    def __init__(self, master, image=None, text_str=None, font=None, font_size=None, **kwargs):
        super().__init__(master, kwargs)
        self._image = None
        self.text_str = text_str
        self.font = font
        self.font_size = font_size
        self.text_x = None
        self.text_y = None
        self.text = None

        if image != None:
            self.initialize_display(image, text_str, font, font_size)

    def initialize_display(self, image, text_str, font, font_size):
        """Initialize image and text within the PreviewCanvas.
        Create an image object with given image as its image.
        Create a text object with given string as text.
        Bind mouse click to drag and drop of text

        Parameters
        ----------
        image : ImageTk.PhotoImage
            The image for the image object
        text_str : str
            The text for the text object
        font : str
            The type of font
        font_size : int
            The size of font

        """
        self.image = image
        self.text_str = text_str
        self.font = font
        self.font_size = font_size
        self.image_width = self.image.width()
        self.image_height = self.image.height()
        self.text_x = 50
        self.text_y = 15
        # Display the image on the canvas
        self.canvas_image_id = self.create_image(
            0,  0, image=self.image, anchor='nw')
        # Display the text om the canvas
        self.text = self.create_text(str(self.text_x), str(self.text_y), text=text_str,
                                     fill='white', font=(self.font, self.font_size), anchor='nw')
        # Bind draging text object to changes in text posiotion on canvas
        self.bind("<B1-Motion>", self.change_position)

    def change_position(self, event):
        """Change position of text object triggered by an event.

        Parameters
        ----------
        event
            event triggers mooving of object

        Issues
        ------
        Text object is moovable beyond the image width and height

        """
        self.text_x = event.x
        self.text_y = event.y

        #  Make sure text only gets targeted if the mouse is near it
        if self.text in self.find_overlapping(str(self.text_x-15), str(self.text_y-15), str(self.text_x+15), str(self.text_y+15)):
            if (self.text_x < self.image_width and self.text_y < self.image_height) and (self.text_x > 0 or self.text_y > 0):
                # Move text to mouse position
                self.coords(self.text, self.text_x, self.text_y)

    def get_position(self):
        """Return coordinates of text.
        """
        return(self.text_x, self.text_y)

    def update_text(self, new_text, new_font, new_size):
        """Update text object parameters.

        Parameters
        ----------
        new_text : str
            The new text to display
        new_font : str
            The new font of the text
        new_size : int
            The new size of the text

        """
        self.itemconfig(self.text, text=new_text,
                        font=(new_font, new_size))

    def update_image(self, new_image):
        """Update image object parameters.

        Parameters
        ----------
        new_image : str
            The new image to display

        """
        self.image = new_image
        self.itemconfig(self.canvas_image_id, image=self.image)

    # Using property decorator

    @property
    def image(self):
        """A getter for image
        """

        return self._image

    @image.setter
    def image(self, new_image):
        """Set any image as ImageTk.PhotoImage type.

        Parameters
        ----------
        new_image : Image
            The image to set as new image for display

        Raises
        ------
        ValueError
            if type of image isn't Image or ImageTk.PhotoImage
        """
        if issubclass(type(new_image), Image.Image):
            new_image = ImageTk.PhotoImage(new_image)
        elif(type(new_image) != ImageTk):
            raise ValueError("Not a recognized image type")
        self._image = new_image
