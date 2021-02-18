"""Manage grid logic"""

from random import random

import numpy as np

# defaults
HNPOLY = 12         # image height will contain HNPOLY polygons
POLY_W2H = 1        # polygons' w/h ratio
COEF = 0.260451     # [0, 1) move verteces coef dist as ratio to next vert


class Grid():
    def __init__(self, image,
            hnpoly=HNPOLY, coef=COEF, poly_w2h=POLY_W2H):
        self.__nhpoly = hnpoly
        self.__coef = coef
        self.__poly_w2h = poly_w2h

        self.w = None
        self.h = None
        self.image = None
        self.__assing_image(image)

        # (r, g, b, noise) floats
        self.__cells = np.zeros((self.h, self.w),
                dtype=(float, 4))

        self.__parse_image()

    def init_gradient(self, image):
        """Find polygons by gradient search"""
        # do later
        raise NotImplementedError

    def centers(self):
        """Return grid centers"""
        pass

    def polygons(self):
        """"Return 2d array of [polygon verts]"""
        pass

    def shuffle_centers(self, coef=COEF):
        """coef 0..1 Move centers randomly, recalculate polygons"""
        pass

    def shuffle_poly(self, coef=COEF):
        """Re-calculate polygons randomly"""
        pass

    def width(self):
        return self.__w

    def height(self):
        return self.__h

    def count(self):
        return self.__w * self.__h

    def __assing_image(self, image):
        if not isvalid(image):
            raise ValueError('Invalid image')
        # TODO support rectangular images
        # assign: self.image, x, y

    def __parse_image(self):
        pass

def isvalid(image):

    return True
