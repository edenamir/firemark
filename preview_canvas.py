
import tkinter as tk
from PIL import Image, ImageTk


class PreviewCanvas(tk.Canvas):

    def __init__(self, master, image, text_str, font, font_size, **kwargs):
        super().__init__(master, kwargs)
        self.image = image
        self.text_str = text_str
        self.font = font
        self.font_size = font_size

        kwargs['width'] = self.image.width()
        kwargs['height'] = self.image.height()

        self.image = self.create_image(
            kwargs['width']/2,  kwargs['height']/2, image=self.image, anchor='center')

        self.text = self.create_text('50', '15', text=text_str, fill='white', font=(
            self.font, self.font_size))  # you can define all kinds of text options here

        self.bind("<B1-Motion>", self.change_position)

    def change_position(self, event):
        x = event.x
        y = event.y

        # 20x20 square around mouse to make sure text only gets targeted if the mouse is near it
        if self.text in self.find_overlapping(str(x-10), str(y-10), str(x+10), str(y+10)):
            self.coords(self.text, x, y)  # move text to mouse position
