#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from numpy import arange
from numpy import array
from numpy import column_stack
from numpy import cos
from numpy import linspace
from numpy import pi
from numpy import sin
from numpy.random import randint
from numpy.random import random

BG = [0,0,0,1]
FRONT = [1,1,1,0.01]

TWOPI = 2.0*pi

SIZE = 5000
PIX = 1.0/SIZE

GRID_X = 1
GRID_Y = 1
GNUM = 5

EDGE = 0.5
RAD = 1
LEAP_X = 0.4
LEAP_Y = 0.4

STEPS = 300
INUM = 3000

GAMMA = 2.2

STP = 0.0000001


def f(x, y):
  while True:
    yield array([[x,y]])

def spline_iterator():
  from modules.sandSpline import SandSpline

  splines = []
  for x in linspace(EDGE, 1.0-EDGE, GRID_X):
    for y in linspace(EDGE, 1.0-EDGE, GRID_Y):
      guide = f(x,y)
      pnum = randint(10,150)

      a = random()*TWOPI + linspace(0, TWOPI, pnum)
      path = column_stack((cos(a), sin(a))) * LEAP_Y

      scale = arange(pnum).astype('float')*STP

      s = SandSpline(
          guide,
          path,
          INUM,
          scale
          )
      splines.append(s)

  itt = 0
  while True:
    for w, s in enumerate(splines):
      xy = next(s)
      itt += 1
      yield itt, w, xy


def main():
  import sys, traceback
  from fn import Fn
  from sand import Sand
  from modules.helpers import get_colors

  sand = Sand(SIZE)
  sand.set_bg(BG)
  sand.set_rgba(FRONT)

  colors = get_colors('colors/dark_cyan_white_black.gif')
  nc = len(colors)

  fn = Fn(prefix='./res/', postfix='.png')
  si = spline_iterator()

  while True:
    try:
      itt, w, xy = next(si)
      rgba = colors[w%nc] + [0.005]
      sand.set_rgba(rgba)
      sand.paint_dots(xy)
      if not itt%(50):
        print("ci:"+str(itt))
      if not itt%(5000):
        if os.path.isfile("./res/dump1.png"):
          print("printing to dump2:"+str(itt))
          sand.write_to_png("./res/dump2.png", GAMMA)
          os.remove("./res/dump1.png")
        else:
          print("printing to dump1:"+str(itt))
          sand.write_to_png("./res/dump1.png", GAMMA)
          if os.path.isfile("./res/dump2.png"):
            os.remove("./res/dump2.png")
    except Exception as e:
      print(e)
      sand.write_to_png("./res/current.png", GAMMA)
      traceback.print_exc(file=sys.stdout)


if __name__ == '__main__':
  main()

