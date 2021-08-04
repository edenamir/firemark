

# Import required Image library
from PIL import Image, ImageDraw, ImageFont
import string
import random
from pathlib import Path
import os  # not suitable for posix os

'''
is not adapted for a GUI
some of the functions can transfer into utils
'''

# printing_option=("single"): str, quantity=(1): int, opacity=(80): int, image_path=None, save_folder=None


class Options():
    def __init__(self, printing_option, quantity, opacity, image_path, save_folder, text):
        self.printing_option = printing_option
        self.quantity = quantity
        self.opacity = opacity
        self.image_path = image_path
        self.save_folder = save_folder
        self.text = text


class FireMark():

    def __init__(self, options):
        self.options = options
        self.printing_option = self.options.printing_option
        self.quantity = self.options.quantity
        self.opacity = self.options.opacity
        self.image_path = self.options.image_path

        self.save_folder = self.options.save_folder
        self.text = self.options.text

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

        # watermarked_pic.show()

        return watermarked_pic

    def watermark_process(self):

        if self.quantity == 1:
            im = self.add_watermark(self.text)
            im.save(str(self.save_folder))

        else:  # maybe give the option to change num of letter?
            for num in range(self.quantity):
                digits = "".join([random.choice(string.digits)
                                  for i in range(5)])
                im = self.add_watermark(digits)

                file_name = os.path.basename(
                    str(self.save_folder))  # return chosen name of image

               # file_name = self.save_folder.stem
                save_path = self.save_folder.parent
                # print("this is save_path "+str(save_path))
                new_name = str(num)+file_name
                # add numbers to front of name according to num of copies
                im.save(str(save_path.joinpath(str(new_name))))


# TODO: calculate printing pattern
# TODO: change icon and name
# TODO: change menu
