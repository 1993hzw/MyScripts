# coding=utf-8
import sys
import os
from PIL import Image
from urllib.request import urlretrieve

curdir = os.path.dirname(__file__)


class MapDownload:
    tempfile = os.path.join(curdir, "temptilefile.png")

    def geturl(self, level, row, col, scale=1, type="y"):
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

    def __init__(self, level, start, end):
        self.level = level
        self.start = start
        self.end = end
        self.mapimg = None
        for row in range(start[0], end[0] + 1):
            for col in range(start[1], end[1] + 1):
                self.urllib_download(self.level, row, col)
                self.mergetile(row, col)

        path = "%s-%s_%s-%s_%s.png" % (
            level, start[0], start[1], end[0], end[1]
        )
        self.mapimg.save(os.path.join(curdir, path))
        os.remove(self.tempfile)


if __name__ == '__main__':
    MapDownload(4, (5, 11), (7, 14))
