
from PIL import Image, ImageDraw, ImageFont
import string
import random
from pathlib import Path
import os  # not suitable for posix os


class Options():
    """
    A class used to link between FireMark and Gui of application

    Attributes
    ----------
    printing_option: str
        The type of watermark 
    quantity : int
        The amount of copies for saving
    opacity : int
        The opacity percentage of the watermark
    font : str
        The type of font
    font_size : int
        The size of font
    image_path : path
        The path of the chosen image
    save_folder : path
        The path of the chosen directory
    text : str
        The text of the watermark
    position : tuple
        The coordinates of the text

    """

    def __init__(self, printing_option, quantity, opacity, font, font_size, image_path, save_folder, text, position):
        self.printing_option = printing_option
        self.quantity = quantity
        self.opacity = opacity
        self.font = font
        self.font_size = font_size
        self.image_path = image_path
        self.save_folder = save_folder
        self.text = text
        self.position = position


class FireMark():
    """
    A class used to print a watermark on an image and save image

    Attributes
    ----------
    options : Options
        A class with data from Gui
    printing_option: str
        The type of watermark 
    quantity : int
        The amount of copies for saving
    opacity : int
        The opacity percentage of the watermark
    font : str
        The type of font
    font_size : int
        The size of font
    image_path : path
        The path of the chosen image
    save_folder : path
        The path of the chosen directory
    text : str
        The text of the watermark
    position : tuple
        The coordinates of the text

    Methodes
    --------
    add_watermark()
        print the text on an image
    watermark_process()
        save watermarked image/images

    """

    def __init__(self, options):
        self.options = options
        self.printing_option = self.options.printing_option
        self.quantity = self.options.quantity
        self.opacity = self.options.opacity
        self.font_size = self.options.font_size
        self.font = self.options.font
        self.image_path = self.options.image_path
        self.save_folder = self.options.save_folder
        self.text = self.options.text
        self.position = self.options.position

    def add_watermark(self, text, image):
        """Print the text on an image.
        If printing option is singel prints a singel watermark.
        Else print multipule watermark all over the image 

        Parameters
        ----------
        text : str
            The text to print
        image : Image
            The image to print on


        Returns
        -------
        Image
            the proccesed image with a watermark/watermarks.

        Issues
        ------
        The position of the printed text is slightly different then the given position

        """

        # Create an Image Object from an Image
        base_layer = image.convert("RGBA")

        width, height = base_layer.size

        # Make a blank image for the text, initialized to transparent text color
        blank_text_image = Image.new(
            "RGBA", base_layer.size, (255, 255, 255, 0))
        blank_text_layer = ImageDraw.Draw(blank_text_image)
        # Create the text font
        font = ImageFont.truetype(self.font, self.font_size)
        textwidth, textheight = blank_text_layer.textsize(text, font)

        if self.printing_option == "single":
            # Draw watermark according to the current position of text
            blank_text_layer.text(self.position, text, font=font,
                                  fill=(255, 255, 255, self.opacity))

        else:
            # Draw watermarks all over the image
            for i in range(10, width-10, 2*textwidth):
                for j in range(10, height-10, 3*textheight):
                    blank_text_layer.text((i, j), text, font=font,
                                          fill=(255, 255, 255, self.opacity))
        # Combine the layers to one image
        watermarked_pic = Image.alpha_composite(
            base_layer, blank_text_image)

        return watermarked_pic

    def watermark_process(self):
        """Save watermarked image/images.

        If quantity is 1 print text on image.
        Save image by given name in saving procces.
        Else print a 5 digits number that is randomly gerenated. 
        save images by givan name adding a number to the start of each
        image name stating with 0.

        """

        image = Image.open(str(self.image_path))

        if self.quantity == 1:
            im = self.add_watermark(self.text, image)
            im.save(str(self.save_folder))

        else:
            # Create multipule images with random digits in each copy
            for num in range(self.quantity):
                digits = "".join([random.choice(string.digits)
                                  for i in range(5)])
                im = self.add_watermark(digits, image)
                # Save chosen name of image
                file_name = os.path.basename(
                    str(self.save_folder))

                save_path = self.save_folder.parent
                new_name = str(num)+file_name
                # Add numbers to front of name according to num of copies
                im.save(str(save_path.joinpath(str(new_name))))
