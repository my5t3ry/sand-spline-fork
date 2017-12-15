#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy import arange
from numpy import array
from numpy import column_stack
from numpy import cos
from numpy import linspace
from numpy import pi
from numpy import sin
from numpy.random import randint
from numpy.random import random

BG = [0, 0, 0, 1]
FRONT = [1, 1, 1, 0.01]

TWOPI = 2.0 * pi
EDGE = 0.08
SIZE = 3000
PIX = 1.0 / SIZE

INUM = 1000

GAMMA = 2.2

STP = 0.00000003


def f(x, y):
  while True:
    yield array([[x, y]])


def spline_iterator():
  from modules.sandSpline import SandSpline

  splines = []
  for _ in range(30):
    guide = f(0.5, 0.5)
    pnum = randint(30, 150)

    a = random() * TWOPI + linspace(EDGE, 1.0 - EDGE, pnum)
    # a = linspace(0, TWOPI, pnum)
    path = column_stack((cos(a), sin(a))) * (0.30 + (randint(0, 5) * 0.005))

    scale = arange(pnum).astype('float') * STP

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
      rgba = colors[w % nc] + [0.0005]
      sand.set_rgba(rgba)
      sand.paint_dots(xy)
      if not itt % (40000):
        print(itt)
        sand.write_to_png("./res/current.png", GAMMA)
    except Exception as e:
      print(e)
      sand.write_to_png("./res/current.png", GAMMA)
      traceback.print_exc(file=sys.stdout)


if __name__ == '__main__':
  main()
