import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from os import listdir
import os


def transform_file(file_path):
    try:
        image = Image.open(file_path)
        copy = image.filter(ImageFilter.CONTOUR)
        copy.save(file_path)
    except Exception:
        pass


def transform_dir(dir_path):
    for name in listdir(dir_path):
        abspath = dir_path + os.sep + name
        if os.path.isdir(abspath):
            transform_dir(abspath)
        else:
            transform_file(abspath)


def main(path):
    if os.path.isdir(path):
        transform_dir(path)
    else:
        transform_file(path)


if __name__ == '__main__':
    main(sys.argv[1])
