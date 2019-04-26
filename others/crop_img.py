import sys
from PIL import Image, ImageDraw, ImageFont
from os import listdir
import os

Image.MAX_IMAGE_PIXELS = None


def transform_file(file_path):
    image = Image.open(file_path)
    width, height = image.size

    start = ((width - width / 4) / 2, (height - height / 4) / 2)
    end = (start[0] + width / 4 + 120, start[1] + height / 4 + 120)
    cropimg = image.crop(start + end)

    print(start)  # 4575,3840
    dir_path = os.path.split(file_path)[0]
    name = os.path.splitext(file_path)[0]
    ext = os.path.splitext(file_path)[1]
    cropimg.save(os.path.join(dir_path, name + "_crop" + ext))


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
