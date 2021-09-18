
import tkinter as tk
from PIL import Image, ImageTk


class PreviewCanvas(tk.Canvas):

    def __init__(self, master, image, text_str, font, font_size, **kwargs):
        super().__init__(master, kwargs)
        self.image = image
        self.text_str = text_str
        self.font = font
        self.font_size = font_size
        self.image_width = self.image.width()
        self.image_height = self.image.height()
        self.text_x = None
        self.text_y = None

        kwargs['width'] = self.image_width
        kwargs['height'] = self.image_height

        self.image = self.create_image(
            kwargs['width']/2,  kwargs['height']/2, image=self.image, anchor='center')

        self.text = self.create_text('50', '15', text=text_str, fill='white', font=(
            self.font, self.font_size))  # you can define all kinds of text options here

        self.bind("<B1-Motion>", self.change_position)

    def change_position(self, event):
        self.text_x = event.x
        self.text_y = event.y

        # 20x20 square around mouse to make sure text only gets targeted if the mouse is near it
        if self.text in self.find_overlapping(str(self.text_x-10), str(self.text_y-10), str(self.text_x+10), str(self.text_y+10)):
            if (self.text_x < self.image_width and self.text_y < self.image_height):
                # move text to mouse position
                self.coords(self.text, self.text_x, self.text_y)
                self.get_position()

    def get_position(self):
        return(self.text_x, self.text_y)

    def update_text(self, options):

        self.itemconfig(self.text, text=options.text,
                        font=(options.font, options.font_size))
