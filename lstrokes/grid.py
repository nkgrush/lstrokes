"""Manage grid logic"""

import math
from random import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# defaults
HNPOLY = 64         # image height will contain HNPOLY polygons
COEF = 0.560451     # [0, 1) move verteces coef dist as ratio to next vert
NCOLORS = 128        # reduce pallete to NCOLORS


class Grid():
    def __init__(self, image,
            hnpoly=HNPOLY, coef=COEF, ncolors=NCOLORS):
        # config
        self.__nhpoly = hnpoly
        self.__coef = coef
        self.__ncolors = ncolors

        # units in cells
        self.w = 0
        self.h = 0

        # in pixels
        self.__poly_side = 0

        self.image = None
        self.mosaic = None
        self.__assing_image(image)

        self.__cells = np.zeros((self.h, self.w), 
                dtype=[('rgb', int, 3), ('noise', float), ('sharpness', float)]
        )
        self.__dots = np.zeros((self.h+1, self.w+1), dtype=[('x', float), ('y', float)])
        self.__place_dots()

        self.__parse_image()
        self.__shuffle_dots()
        self.__render_mosaic()

    def width(self):
        return self.w

    def height(self):
        return self.h

    def count(self):
        return self.w * self.h

    def show_mosaic(self):
        self.mosaic.show()

    def show_origin(self):
        self.image.show()

    def __assing_image(self, image):
        im = Image.open(image)
        if im is None:
            raise ValueError

        # TODO rectangular images
        wpx, hpx = im.size
        if wpx > hpx:
            im = im.crop((0, 0, hpx, hpx))
        elif hpx > wpx:
            im = im.crop((0, 0, wpx, wpx))

        h = self.__nhpoly
        side = hpx / self.__nhpoly
        hpx = side * h

        w = h
        wpx = side * w

        # TODO work with pre-defined palette
        im = im.convert("P", palette=Image.ADAPTIVE, colors=self.__ncolors)
        im = im.convert("RGB", palette=Image.ADAPTIVE, colors=self.__ncolors)

        self.image = im
        self.h = h
        self.w = w
        self.__poly_side = side

    def __shuffle_dots(self):
        R = self.__poly_side * self.__coef
        # Body
        for i in range(1, self.h):
            for j in range(1, self.w):
                dot = self.__dots[i, j]
                t = 2 * math.pi * random()
                r = R * random()
                dot['y'] += r * math.sin(t)
                dot['x'] += r * math.cos(t)
        # Perimeter
        for j in range(1, self.w):
            self.__dots[0, j]['x'] += R * random()
        for j in range(1, self.w):
            self.__dots[self.h, j]['x'] += R * random()
        for i in range(1, self.h):
            self.__dots[i, 0]['y'] += R * random()
        for i in range(1, self.h):
            self.__dots[i, self.w]['y'] += R * random()

    def __render_mosaic(self):
        img = Image.new('RGB', self.image.size)
        self.mosaic = img
        draw = ImageDraw.Draw(img)
        for y in range(self.h):
            for x in range(self.w):
                cell = self.__cells[y, x]
                dots = self.__dots
                xy = [(d['x'], d['y']) for d in [
                    dots[y, x],     # up-left
                    dots[y, x+1],   # up-right
                    dots[y+1, x+1], # down-right
                    dots[y+1, x]    # down-left
                ]]
                col = (*cell['rgb'],)
                draw.polygon(xy, fill=col, outline=col)
        img.filter(ImageFilter.SMOOTH_MORE)

    def __parse_cell(self, y, x):
        cell = self.__cells[y, x]
        lu = self.__dots[y, x]
        rd = self.__dots[y+1, x+1]
        crop = self.image.crop((lu['x'], lu['y'], rd['x'], rd['y']))

        cols = getcolors(crop)
        cell['rgb'] = cols[0]
        # TODO
        cell['noise'] = 0
        cell['sharpness'] = 0

    def __place_dots(self):
        h, w = self.__dots.shape
        side = self.__poly_side
        for i in range(h):
            for j in range(w):
                d = self.__dots[i, j]
                d['y'] = int(i * side)
                d['x'] = int(j * side)

    def __parse_image(self):
        for y in range(self.h):
            for x in range(self.w):
                self.__parse_cell(y, x)

def getcolors(img, n=2, ncolors=256):
    cols = img.getcolors(ncolors)
    cols = sorted(cols, key=lambda x: x[0], reverse=True)[:n]
    return [e[1] for e in cols]
