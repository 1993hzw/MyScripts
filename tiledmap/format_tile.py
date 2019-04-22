import sys
from PIL import Image
from os import listdir
import os


def transform_file(file_path):
    image = Image.open(file_path)
    width, height = image.size
    if width != 256 or height != 256:
        result = Image.new(image.mode, (256, 256))
        result.paste(image, box=(0, 0))
        result.save(file_path)


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
