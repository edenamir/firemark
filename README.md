# Firemark

## Table of contents
* [General info](#general-info)
* [Importent notes](#Importent-notes)
* [Known issues](#Known-issues)
* [Technologies](#technologies)


## General info
This project is a simple watermarking app. It has a few options of watermark types to cutomize an image to your liking:

1. A single watermark-drag & drop watermark wherever you please.
2. Multiple watermarks-cover the whole image.
3. A random 5 digits number-also available as drag & drop
4. Multiple random number watermarks- same number cover the whole image.

Each type can have differente opacity, text size and fonts.\
After each change clicking the preview image button will display an example of the watermark on the image
## Importent notes
1. Single watermark and number of copies is geater than 1- the example text on the display will be the text in Enter Text entry.
2. All fileds of the menu must be filled in order for the app to work proparly
3. When saving more than one copy, the name of the files will be #chosen_name where # start with 0 up to number of copies\
Ex: 0new_image.png
## Known issues
1. Only two fonts are availble
2. Opacity percentage is not displayed with single watermark option
## Technologies
Project is created with:
* Python 3.8.5- main libraries PIL/Pillow, Tkinter
