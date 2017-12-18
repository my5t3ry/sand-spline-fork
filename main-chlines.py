#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy import pi
from numpy import array

from numpy import linspace
from numpy import arange
from numpy import zeros
from numpy import column_stack


BG = [0, 0, 0, 1]
FRONT = [1, 1, 1, 0.01]
GAMMA = 2.5

TWOPI = 2.0*pi
FRONT = [1,1,1,1]
BACK = [0,1,1,0.001]

SIZE = 5000
PIX = 1.0/SIZE

GRID_Y = 100

EDGE = 0.08
LEAP_Y = (1.0-2*EDGE)/(GRID_Y-1)*0.5*0.75

STEPS = 300
INUM = 1000

# STP = 0.0000004
STP = 0.0000003*0.15


def f(x, y):
  while True:
    yield array([[x,y]])

def spline_iterator():
  from modules.sandSpline import SandSpline

  splines = []
  for i, y in enumerate(linspace(EDGE, 1.0-EDGE, GRID_Y)):
    pnum = 4+i
    guide = f(0.5,y)

    ## hlines
    x = linspace(-1,1.0, pnum)*(1.0-2*EDGE)*0.5
    y = zeros(pnum,'float')
    path = column_stack([x,y])

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
      yield itt,w, xy


def main():
  import sys, traceback
  from fn import Fn
  from sand import Sand

  sand = Sand(SIZE)
  sand.set_bg(BG)
  sand.set_rgba(FRONT)

  fn = Fn(prefix='./res/', postfix='.png')
  si = spline_iterator()
  from modules.helpers import get_colors
  colors = get_colors('colors/dark_cyan_white_black2.gif')
  nc = len(colors)

  while True:
    try:
      itt,w, xy = next(si)
      sand.paint_dots(xy)
      rgba = colors[w%nc] + [0.005]
      sand.set_rgba(rgba)
      if not itt%(500*GRID_Y):
        print(itt)
        sand.write_to_png("./res/currenrt.png", GAMMA)
    except Exception as e:
      print(e)
      sand.write_to_png(fn.name(), GAMMA)
      traceback.print_exc(file=sys.stdout)


if __name__ == '__main__':
  main()

