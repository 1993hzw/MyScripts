import os
import sys
import shutil
import math
from PIL import Image
import argparse

TILE_SIZE = 256


def mkdir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

    os.mkdir(path)


def __find_max_level(image):
    img_width, img_height = image.size
    level = 0
    maxsize = (2 ** level) * TILE_SIZE
    while maxsize < img_width or maxsize < img_height:
        level += 1
        maxsize = (2 ** level) * TILE_SIZE
    return level


def generate_tiles(level, image, root_dir, optimize, color):
    tile_dir = os.path.join(root_dir, str(level))
    mkdir(tile_dir)
    img_width, img_height = image.size
    max_index = 2 ** level
    for row in range(0, max_index):
        if row * TILE_SIZE > img_height:
            return

        for col in range(0, max_index):
            if col * TILE_SIZE > img_width:
                break

            start = (col * TILE_SIZE, row * TILE_SIZE)
            end = (min(start[0] + TILE_SIZE, img_width), min(start[1] + TILE_SIZE, img_height))

            if start[0] == end[0] or start[1] == end[1]:  # no image
                break

            # print("tile: %d %d %d > %s %s" % (level, row, col, image.mode, str(start + end)))

            region = image.crop(start + end)
            original_mode = image.mode
            tile = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), color=color)
            tile.paste(region)
            if region.size == (TILE_SIZE, TILE_SIZE):
                if original_mode == "RGBA":
                    if optimize:
                        tile = tile.convert("RGB")
                        tile.save(os.path.join(tile_dir, "%d_%d.png" % (col, row)), "JPEG")
                    else:
                        tile.save(os.path.join(tile_dir, "%d_%d.png" % (col, row)), "PNG")
                else:
                    tile = tile.convert("RGB")
                    tile.save(os.path.join(tile_dir, "%d_%d.png" % (col, row)), "JPEG")

            else:
                tile.save(os.path.join(tile_dir, "%d_%d.png" % (col, row)), "PNG")


def main(path, optimize, color="#00000000"):
    print("background color = " + color)
    if not os.path.isfile(path):
        raise RuntimeError("invalid image file")

    try:
        image = Image.open(path)
    except IOError:
        raise RuntimeError("Can't open the image file: " + path)

    dir_path = os.path.split(path)[0]
    name = os.path.splitext(path)[0]
    root_dir = os.path.join(dir_path, name)
    mkdir(root_dir)

    max_level = __find_max_level(image)
    max_size = 2 ** max_level * 256
    img_width, img_height = image.size
    print("original size = %s  total level = %s" % (str(image.size), max_level))
    for lvl in range(0, max_level + 1):
        print(lvl)
        scale = (2 ** lvl * 256.0) / max_size
        size = (int(math.ceil(img_width * scale)), int(math.ceil(img_height * scale)))
        scaled_img = image.resize(size, Image.ANTIALIAS)
        print("scaled size = %s %s" % (scale, str(scaled_img.size)))
        generate_tiles(lvl, scaled_img, root_dir, optimize, color)

    print("original size = %s" % str(image.size))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Cut a image into tiles")
    parser.add_argument('filename')
    parser.add_argument('--optimize', '-o', action='store_true',
                        help='Optimize the image size by ignoring transparency.')
    parser.add_argument('--color', '-c',
                        help='Tile background color. The default color is transparent (#00000000).')
    args = parser.parse_args()
    if args.color is None:
        args.color = "#00000000"
    main(args.filename, args.optimize, args.color)
