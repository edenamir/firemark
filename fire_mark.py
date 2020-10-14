'''
new awesome project by Mattan and Eden

'''

# Import required Image library
import string
import random
from pathlib import Path
import pdb
import utils
from PIL import Image, ImageDraw, ImageFont


class FireMark():

    def __init__(self, printing_option: str, quantity: int, opacity: int, image_path, save_folder):
        self.printing_option = printing_option
        self.quantity = quantity
        self.opacity = opacity
        self.image_path = image_path
        self.save_folder = save_folder

    def add_watermark(self, text):

        # Create an Image Object from an Image
        base_layer = Image.open(str(self.image_path)).convert("RGBA")
        # pdb.set_trace()

        width, height = base_layer.size

        # make a blank image for the text, initialized to transparent text color
        blank_text_image = Image.new(
            "RGBA", base_layer.size, (255, 255, 255, 0))
        blank_text_layer = ImageDraw.Draw(blank_text_image)

        font = ImageFont.truetype('arial.ttf', 72)
        # TODO: choose font and size
        textwidth, textheight = blank_text_layer.textsize(text, font)

        if self.printing_option == "single":
            # calculate the x,y coordinates of the text
            margin = 10
            x = width - textwidth - margin
            y = height - textheight - margin
            # TODO: get x,y from user

            # draw watermark in the bottom right corner
            blank_text_layer.text((x, y), text, font=font,
                                  fill=(255, 255, 255, self.opacity))

        else:

            for i in range(10, width-10, 2*textwidth):
                for j in range(10, height-10, 3*textheight):
                    blank_text_layer.text((i, j), text, font=font,
                                          fill=(255, 255, 255, self.opacity))

        watermarked_pic = Image.alpha_composite(
            base_layer, blank_text_image)

        watermarked_pic.show()

        return watermarked_pic

    def watermark_option(self):

        if self.quantity == 1:
            text = input("Enter watermark: ")
            im = self.add_watermark(text)

            # might need a format
            im.save(str(self.save_folder/"watermarked_image.png"))

        else:  # maybe give the option to change num of letter?
            for num in range(self.quantity):
                digits = "".join([random.choice(string.digits)
                                  for i in range(5)])
                im = self.add_watermark(digits)
                # might need a format
                im.save(str(self.save_folder/(f"watermarked{num}.png")))


# TODO: input to name of saved file and a deafault saving name
# TODO: calculate printing pattern
