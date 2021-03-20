#!/usr/bin/env python3

"""Simplify image into a grid of polygons"""

from lstrokes.grid import Grid, getcolors
from sys import argv

# TODO cmd args

print(argv)
g = Grid(argv[1])
g.mosaic.save('out.jpg')
g.show_mosaic()
