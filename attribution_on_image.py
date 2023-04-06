# Adds attribition information from file name of iNaturalist downloaded photos to the image
# Assumes file name format is "Genus species_username_licence_photoID.jpeg", i.e., underscores are separators
# Using white text as default, assuming that a lot of the photos will be green-dominated and somewhat dark

import sys, getopt
from PIL import Image, ExifTags, ImageOps, ImageFont, ImageDraw
import glob
import re

# defaults
# textcolour = [222,76,32] (orange)
default_textcolour = [255, 255, 255]
default_prefix = 'attributed'


def add_attribution_to_image(imagepath, attributiontext="", textcolour=default_textcolour) -> Image:
    """
    Adds attribution text to the bottom of an image

    Text colour and attribution text can be specified, otherwise attribution text will be taken from the filename.
    Assumes file name format is "Genus species_username_licence_photoID.jpeg", i.e., underscores are separators


    :param imagepath: path to the image file
    :type imagepath: string
    :param attributiontext: text to add to the image
    :type attributiontext: string
    :param textcolour: colour of the text to add to the image
    :type textcolour: list of 3 integers
    :return: image with attribution text added
    :rtype: PIL Image
    """
    testimage = Image.open(imagepath)
    nameonly = re.split('[\/]', imagepath)[-1]  ## need to test this ...
    print(nameonly)
    # nameonly = imagepath.split('/')[-1]
    nameparts = nameonly.split('_')
    licence = nameparts[len(nameparts) - 2]  ## can we not have this in metadata?? arrays in the filename are a pain
    usernameparts = len(nameparts) - 3
    username = ''
    for j in range(0, usernameparts):
        if username != '':
            username = username + '_'
        username = username + nameparts[1 + j]
    if attributiontext == "":
        attributiontext = "iNaturalist, " + username + ", " + licence

    width, height = testimage.size
    fontsize = int(height / 30)
    if (len(attributiontext) * int(fontsize * 0.38) + 32) > width:
        fontsize = int(2.6 * width / (len(attributiontext) + 10))
    # fontsize = int(height / 10)
    indent = int(fontsize / 4)

    draw = ImageDraw.Draw(testimage)
    # fontpath = "/Users/daneevans/Documents/git/ort_model_benchmarking/venv/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/DejaVuSans.ttf"
    fontpath = "LiberationSans-Regular.ttf"  ## Windows.
    font = ImageFont.truetype(fontpath, fontsize)

    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((indent, int(height - (3 * fontsize))), "Photo credit:", (textcolour[0], textcolour[1], textcolour[2]),
              font=font)
    draw.text((indent, int(height - (1.5 * fontsize))), attributiontext, (textcolour[0], textcolour[1], textcolour[2]),
              font=font)

    return testimage


if __name__ == "__main__":
    infoldername = "./images/"
    ## Find all images in the folder
    imagenamelist = glob.glob(infoldername + '*.jpeg')
    imagenamelist.extend(glob.glob(infoldername + '*.jpg'))
    imagenamelist.extend(glob.glob(infoldername + '*.JPG'))
    imagenamelist.extend(glob.glob(infoldername + '*.JPEG'))
    imagenamelist.extend(glob.glob(infoldername + '*.png'))
    imagenamelist.extend(glob.glob(infoldername + '*.PNG'))

    for imagepath in imagenamelist:
        print(imagepath)
        testimage = add_attribution_to_image(imagepath, textcolour=default_textcolour)
        nameonly = re.split('[\/]', imagepath)[-1]  ## need to test this ...
        testimage.save("./" + default_prefix + '_' + nameonly)
        testimage.close()
