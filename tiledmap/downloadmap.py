# coding=utf-8
import sys
import os
from PIL import Image
from urllib.request import urlretrieve
import argparse

curdir = os.path.dirname(__file__)

PROJECTION_WM = "wm"
PROJECTION_LL = "lnglat"


class MapDownload:
    tempfile = os.path.join(curdir, "__temptilefile__.png")

    # https://t0.tianditu.gov.cn/img_c/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=c&FORMAT=tiles&TILEMATRIX=5&TILEROW=6&TILECOL=24&tk=b34f09c6586e9741629c42f716b7494b

    def geturl(self, level, row, col, scale=1, type="y"):
        if self.projection == PROJECTION_LL:
            return "https://t0.tianditu.gov.cn/img_c/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=c&FORMAT=tiles&TILEMATRIX=%d&TILEROW=%d&TILECOL=%d&tk=b34f09c6586e9741629c42f716b7494b" % (
                level, row, col)
        else:
            return "https://mt0.google.cn/maps/vt?lyrs=%s&scale=%s&hl=zh-CN&x=%d&y=%d&z=%d" % (
                type, scale, col, row, level)

    def urllib_download(self, level, row, col, scale=2, imgtype="y"):
        url = self.geturl(level, row, col, scale, imgtype)
        print(url)
        urlretrieve(url, self.tempfile)

    def mergetile(self, row, col):
        image = Image.open(self.tempfile)
        width, height = image.size
        if self.mapimg is None:
            self.mapimg = Image.new("RGBA", (width * (self.end[1] - self.start[1] + 1),
                                             height * (self.end[0] - self.start[0] + 1)))
        self.mapimg.paste(image, (width * (col - self.start[1]), height * (row - self.start[0])))

    def __init__(self, level, start, end, projection=PROJECTION_WM, output=None):
        self.level = level
        self.start = start
        self.end = end
        self.mapimg = None
        self.projection = projection
        self.output = output

        for row in range(start[0], end[0] + 1):
            for col in range(start[1], end[1] + 1):
                self.urllib_download(self.level, row, col)
                self.mergetile(row, col)

        if self.output is None:
            path = "%s_%s-%s_%s-%s_%s.png" % (
                self.projection, level, start[0], start[1], end[0], end[1]
            )
            path = os.path.join(curdir, path)
        else:
            path = self.output

        self.mapimg.save(path)
        os.remove(self.tempfile)


def parseTileIndex(s):
    strs = s.split(",")
    index = [0, 0]
    if len(strs) > 0:
        index[0] = int(strs[0])
    if len(strs) > 1:
        index[1] = int(strs[1])
    return index


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get a map by downloading tiles.")
    parser.add_argument('level', type=int,
                        help='''The tile level. ''')
    parser.add_argument('start',
                        help='''The start index of tile, given as "row,col". ''')
    parser.add_argument('end',
                        help='''The end index of tile, given as "row,col". ''')
    parser.add_argument('-t', '--tianditu', action='store_true', default=False,
                        help='''tiles source from Tianditu map.
                        The default source is Google map''')
    parser.add_argument('-o', '--output',
                        help='''The output map dir path.
                     The default path is the same with the input path.''')

    args = parser.parse_args()
    # MapDownload(4, (5, 11), (7, 14))

    projection = PROJECTION_WM
    if args.tianditu:
        projection = PROJECTION_LL

    MapDownload(level=args.level,
                start=parseTileIndex(args.start),
                end=parseTileIndex(args.end),
                projection=projection,
                output=args.output)
