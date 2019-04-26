import sys
from PIL import Image, ImageDraw, ImageFont
from os import listdir
import os


def transform_file(file_path):
    image = Image.open(file_path)
    copy = image.copy()
    width, height = image.size
    font = ImageFont.truetype("Arial.ttf", 14)
    draw = ImageDraw.Draw(copy)
    draw.text((0, 0), "TiledMap", fill=(255, 255, 255, 50), font=font)
    copy.save(file_path)


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
