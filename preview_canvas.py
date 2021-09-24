
import tkinter as tk
from PIL import Image, ImageTk


class PreviewCanvas(tk.Canvas):

    def __init__(self, master, image=None, text_str=None, font=None, font_size=None, **kwargs):
        super().__init__(master, kwargs)
        self.image = image
        self.text_str = text_str
        self.font = font
        self.font_size = font_size
        self.text_x = None
        self.text_y = None
        self.text = None

        if image != None:
            self.initialize_display(image, text_str, font, font_size)

    def initialize_display(self, image, text_str, font, font_size):
        self.image = image
        self.text_str = text_str
        self.font = font
        self.font_size = font_size
        self.image_width = self.image.width()
        self.image_height = self.image.height()
        self.text_x = 50
        self.text_y = 15

        self.image = self.create_image(
            self.image_width/2,  self.image_height/2, image=self.image, anchor='center')
        self.text = self.create_text(str(self.text_x), str(self.text_y), text=text_str, fill='white', font=(
            self.font, self.font_size), anchor='nw')
        self.bind("<B1-Motion>", self.change_position)

    def change_position(self, event):
        self.text_x = event.x
        self.text_y = event.y
        print(self.text_x, self.text_y)

        # 20x20 square around mouse to make sure text only gets targeted if the mouse is near it
        if self.text in self.find_overlapping(str(self.text_x-10), str(self.text_y-10), str(self.text_x+10), str(self.text_y+10)):
            if (self.text_x < self.image_width and self.text_y < self.image_height):
                # move text to mouse position
                self.coords(self.text, self.text_x, self.text_y)

    def get_position(self):
        print("get_position")
        print(self.text_x, self.text_y)
        return(self.text_x, self.text_y)

    def update_text(self, options):

        self.itemconfig(self.text, text=options.text,
                        font=(options.font, options.font_size))