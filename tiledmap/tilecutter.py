import os
import sys
import shutil
import math
from PIL import Image
import argparse
import warnings


class TileCutter:
    tile_size = None
    path = None
    compress = False
    bgcolor = None

    _min_level = None
    _max_level = None
    _src_img_level = None
    _upperleft = None
    _output = None

    def __init__(self, path, compress=False, bgcolor="#00000000", tile_size=256,
                 src_level=None,
                 min_level=0,
                 max_level=None,
                 upperleft=(0, 0),
                 output=None):

        if bgcolor is None:
            bgcolor = "#00000000"
        if upperleft is None or not isinstance(upperleft, tuple):
            upperleft = (0, 0)

        self.tile_size = tile_size
        self.path = path
        self.compress = compress
        self.bgcolor = bgcolor
        self._src_img_level = src_level
        self._min_level = max(min_level, 0)
        self._max_level = max_level
        self._upperleft = upperleft
        self._output = output

        if self._src_img_level is not None and self._src_img_level < 0:
            raise RuntimeError("source image level must be equal or greater than 0")

        if self._max_level is not None and self._max_level < self._min_level:
            raise RuntimeError("max_level must be equal or greater than min_level")

    def mkdir(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)

        os.mkdir(path)

    def __find_max_level(self, image):
        img_width, img_height = image.size
        level = 0
        maxsize = (2 ** level) * self.tile_size
        while maxsize < img_width or maxsize < img_height:
            level += 1
            maxsize = (2 ** level) * self.tile_size
        return level

    def generate_tiles(self, level, image, root_dir):
        tile_dir = os.path.join(root_dir, str(level))
        self.mkdir(tile_dir)
        img_width, img_height = image.size
        max_index = 2 ** level
        for row in range(0, max_index):
            if row * self.tile_size > img_height:
                return

            for col in range(0, max_index):
                if col * self.tile_size > img_width:
                    break

                start = (col * self.tile_size, row * self.tile_size)
                end = (min(start[0] + self.tile_size, img_width),
                       min(start[1] + self.tile_size, img_height))

                if start[0] == end[0] or start[1] == end[1]:  # no image
                    break

                # print("tile: %d %d %d > %s %s" % (level, row, col, image.mode, str(start + end)))

                region = image.crop(start + end)
                original_mode = image.mode
                tile = Image.new("RGBA", (self.tile_size, self.tile_size), color=self.bgcolor)
                tile.paste(region)
                if region.size == (self.tile_size, self.tile_size):
                    if original_mode == "RGBA":
                        if self.compress:
                            tile = tile.convert("RGB")
                            tile.save(os.path.join(tile_dir, "%d_%d.png" % (col, row)), "JPEG")
                        else:
                            tile.save(os.path.join(tile_dir, "%d_%d.png" % (col, row)), "PNG")
                    else:
                        tile = tile.convert("RGB")
                        tile.save(os.path.join(tile_dir, "%d_%d.png" % (col, row)), "JPEG")

                else:
                    tile.save(os.path.join(tile_dir, "%d_%d.png" % (col, row)), "PNG")

    def cut(self):
        if not os.path.isfile(self.path):
            raise RuntimeError("invalid image file")

        try:
            image = Image.open(self.path)
        except IOError:
            raise RuntimeError("Can't open the image file: " + self.path)

        dir_path = os.path.split(self.path)[0]
        name = os.path.splitext(self.path)[0]
        if self._output is None:
            self._output = os.path.join(dir_path, name)
        self.mkdir(self._output)

        if self._src_img_level is None:
            self._src_img_level = self.__find_max_level(image)
        if self._max_level is None:
            self._max_level = max(self._src_img_level, self._min_level)

        max_size = 2 ** self._src_img_level * 256
        img_width, img_height = image.size
        for lvl in range(self._min_level, self._max_level + 1):
            print(lvl)
            scale = (2 ** lvl * 256.0) / max_size
            scaled_w = math.ceil(img_width * scale)
            scaled_h = img_height * scale
            if scaled_w < 1 or scaled_h < 1:
                print("%s is too small, skip it! " % str((scaled_w, scaled_h)))
                continue

            size = (int(scaled_w), int(math.ceil(scaled_h)))
            scaled_img = image.resize(size, Image.ANTIALIAS)
            print("scaled size = %s %s" % (scale, str(scaled_img.size)))
            self.generate_tiles(lvl, scaled_img, self._output)

        print("Finished!")
        print("Level=[%s, %s]" % (self._min_level, self._max_level))
        print(
            "Source image: size = %s, level = %s, upper left location = %s" % (
                str(image.size), self._src_img_level, str(self._upperleft)))
        print("Output: " + self._output)
        if self._src_img_level < self._max_level:
            print(
                "Warnings: The max level %s is greater than source image level %s, which will lead to blurred tiles above level %s" \
                % (self._max_level, self._src_img_level, self._src_img_level))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Cut a image into tiles")
    parser.add_argument('filename')
    parser.add_argument('--compress', '-c', action='store_true',
                        help='Compress the image size by ignoring transparency.')
    parser.add_argument('--bgcolor', '-b',
                        help='''Tile background color, given as #rgba or #rrggbbaa.
                        The default color is transparent (#00000000).''')
    parser.add_argument('--srclevel', '-level', type=int,
                        help='''The source image level. 
                        The default value is computed by the image size.''')
    parser.add_argument('--minlevel', '-min', type=int,
                        help='''The min level for cutting tiles. 
                        The default value is 0.''')
    parser.add_argument('--maxlevel', '-max', type=int,
                        help='''The max level for cutting tiles.
                         The default value is the source image level.''')
    parser.add_argument('--upperleft', '-ul',
                        help='''The upper left location of image in full map, given as x,y, in px.
                         The default value is 0,0.''')
    parser.add_argument('--output', '-o',
                        help='''The output tiles dir path.
                         The default path is the same with the input path.''')
    args = parser.parse_args()
    upperleft = [0, 0]
    if args.upperleft is not None:
        strs = args.upperleft.split(",")
        if len(strs) > 0:
            upperleft[0] = int(strs[0])
        if len(strs) > 1:
            upperleft[1] = int(strs[1])

    cutter = TileCutter(path=args.filename, compress=args.compress, bgcolor=args.bgcolor,
                        src_level=args.srclevel, min_level=args.minlevel, max_level=args.maxlevel,
                        upperleft=tuple(upperleft),
                        output=args.output)
    print("\n++++++++++++++++ begin ++++++++++++++++++++")
    cutter.cut()
    print("+++++++++++++++++ end +++++++++++++++++++++\n")
