#!/usr/bin/env python3

"""Simplify image into a grid of polygons"""

from grid import Grid, getcolors
from sys import argv

# TODO cmd args

g = Grid(argv[1], int(argv[2]), float(argv[3]))
print(getcolors(g.image))
print(g.w, g.h, g.image.size)
g.show_origin()
g.show_mosaic()
