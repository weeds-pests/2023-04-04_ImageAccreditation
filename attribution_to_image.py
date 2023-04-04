# Adds attribition information from file name of iNaturalist downloaded photos to the image
# Assumes file name format is "Genus species_username_licence_photoID.jpeg", i.e., underscores are separators
# Using orange text as default, assuming that a lot of the photos will be green-dominated and somewhat dark

import sys, getopt
from PIL import Image, ExifTags, ImageOps, ImageFont, ImageDraw
import glob

# defaults

infoldername = './'
outfoldername = './'
# textcolour = [222,76,32] (orange)
textcolour = [255, 255, 255]
prefix = 'attributed'


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='#', printEnd="\r"):
    """
	Call in a loop to create terminal progress bar
	@params:
		iteration   - Required  : current iteration (Int)
		total       - Required  : total iterations (Int)
		prefix      - Optional  : prefix string (Str)
		suffix      - Optional  : suffix string (Str)
		decimals    - Optional  : positive number of decimals in percent complete (Int)
		length      - Optional  : character length of bar (Int)
		fill        - Optional  : bar fill character (Str)
		printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
	"""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


# parse parameters

try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:p:s:")
except getopt.GetoptError:
    print('Use: attribution_to_image.py -i <inputdirectory> -o <outputdirectory> -p <prefix> -c <fontcolour>')
    print('More details: reformat_imgs_for_training.py -h')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print(
            'Script for bulk-adding attribution information to folders of images, assuming that information is in file names in format ''genus species_username_licence_imageID.jpeg''.')
        print('\nUse: attribution_to_image.py -i <inputdirectory> -o <outputdirectory> -p <prefix> -c <fontcolour>')
        print('\nParameters')
        print('i: Path to directory containing input image files, default is current working directory')
        print('h: Help, i.e. get this information')
        print('o: Path to output directory, default is current working directory')
        print(
            'p: Prefix to output filenames to ensure that originals are not overwritten and/or to specify class names. Default is ''attributed''')
        print(
            'c: Font colour in format RGB separated by commas without spaces, as in ''255,255,255'' for white. Default is white.')
        sys.exit()
    elif opt == "-i":
        infoldername = arg
        if infoldername[len(infoldername) - 1] != "/":
            infoldername = infoldername + "/"
    elif opt in ("-o"):
        outfoldername = arg
        if outfoldername[len(outfoldername) - 1] != "/":
            outfoldername = outfoldername + "/"
    elif opt in ("-p"):
        prefix = arg
    elif opt in ("-c"):
        textcolourtext = arg
        textcolour = [int(textcolourtext.split(',')[0]), int(textcolourtext.split(',')[1]),
                      int(textcolourtext.split(',')[2])]

# get names of images

imagenamelist = glob.glob(infoldername + '*.jpeg')
imagenamelist.extend(glob.glob(infoldername + '*.JPG'))
imagenamelist.extend(glob.glob(infoldername + '*.JPEG'))
imagenamelist.extend(glob.glob(infoldername + '*.png'))
imagenamelist.extend(glob.glob(infoldername + '*.PNG'))

# load images and process

for i in range(0, len(imagenamelist)):
    testimage = Image.open(imagenamelist[i])
    nameonly = imagenamelist[i].split('/')[len(imagenamelist[i].split('/')) - 1]
    nameparts = nameonly.split('_')
    licence = nameparts[len(nameparts) - 2]
    usernameparts = len(nameparts) - 3
    username = ''
    for j in range(0, usernameparts):
        if username != '':
            username = username + '_'
        username = username + nameparts[1 + j]
    attributiontext = "iNaturalist, " + username + ", " + licence

    width, height = testimage.size
    fontsize = int(height / 30)
    if (len(attributiontext) * int(fontsize * 0.38) + 32) > width:
        fontsize = int(2.6 * width / (len(attributiontext) + 10))
    # fontsize = int(height / 10)
    indent = int(fontsize / 4)

    # img = Image.open("sample_in.jpg")
    draw = ImageDraw.Draw(testimage)
    font = ImageFont.truetype("LiberationSans-Regular.ttf", fontsize)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((indent, int(height - (3 * fontsize))), "Photo credit:", (textcolour[0], textcolour[1], textcolour[2]),
              font=font)
    draw.text((indent, int(height - (1.5 * fontsize))), attributiontext, (textcolour[0], textcolour[1], textcolour[2]),
              font=font)

    testimage.save(outfoldername + prefix + '_' + nameonly)
    testimage.close()
    printProgressBar(i, len(imagenamelist), length=50)
