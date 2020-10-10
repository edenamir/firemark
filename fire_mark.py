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
#from tkinter.filedialog import askopenfilename
#from tkinter import Tk


def add_watermark(img_path: Path, text: str, opacity: int, printing_option: str):

    # Create an Image Object from an Image
    base_layer = Image.open(str(img_path)).convert("RGBA")
    # pdb.set_trace()

    width, height = base_layer.size

    # make a blank image for the text, initialized to transparent text color
    blank_text_image = Image.new("RGBA", base_layer.size, (255, 255, 255, 0))
    blank_text_layer = ImageDraw.Draw(blank_text_image)

    font = ImageFont.truetype('arial.ttf', 36)
    # TODO: choose font and size
    textwidth, textheight = blank_text_layer.textsize(text, font)

    if printing_option == "single":
        # calculate the x,y coordinates of the text
        margin = 10
        x = width - textwidth - margin
        y = height - textheight - margin
        # TODO: get x,y from user

        # draw watermark in the bottom right corner

        blank_text_layer.text((x, y), text, font=font,
                              fill=(255, 255, 255, opacity))

        watermarked_pic = Image.alpha_composite(base_layer, blank_text_image)

        watermarked_pic.show()

    else:
        aspect_ratio = textwidth / textheight
        new_text_width = width * 0.125
        blank_text_layer.thumbnail(
            (new_text_width, new_text_width / aspect_ratio), Image.ANTIALIAS)

        tmp_img = Image.new('RGB', base_layer.size)

        for i in range(0, tmp_img.size[0], blank_text_layer.size[0]):
            for j in range(0, tmp_img.size[1], blank_text_layer.size[1]):
                base_layer.paste(blank_text_layer, (i, j), blank_text_layer)

        watermarked_pic = base_layer
        watermarked_pic.show()

    return watermarked_pic

# Save watermarked image
# im.save('images/watermark.jpg')


def printing_option_and_quantity():

    while True:
        try:
            printing_option = input(
                "Whould you like a single or multipule watermarks? ")
            if printing_option == "single" or printing_option == "multipule":
                break
        except:
            print("Please answer single or multipule only")
            continue

    quantity = int(input("How many copies would you like to create? "))
    opacity = utils.percent_to_byte(
        int(input("Enter opacity percentage: ")))

    path = utils.get_path_from_user()

    print("Enter folder to save files")
    save_path = utils.get_path_from_user()

    if printing_option == "single":

        if quantity == 1:
            im = add_watermark(path,
                               input("Enter watermark: "),
                               opacity, "single")

            # might need a format
            im.save(str(save_path/"watermarked_image.jpg"))

        else:
            for num in range(quantity):
                digits = "".join([random.choice(string.digits)
                                  for i in range(8)])
                im = add_watermark(path, digits, opacity, "single")
                # might need a format
                im.save(str(save_path/"watermarked"+str(num)+".jpg"))

    else:
        if quantity == 1:
            im = add_watermark(path,
                               input("Enter watermark: "),
                               opacity, "multipule")

            # might need a format
            im.save(str(save_path/"watermarked_image.jpg"))

        else:
            for num in range(quantity):
                digits = "".join([random.choice(string.digits)
                                  for i in range(8)])
                im = add_watermark(path, digits, opacity, "multipule")
                # might need a format
                im.save(str(save_path/"watermarked"+str(num)+".jpg"))
