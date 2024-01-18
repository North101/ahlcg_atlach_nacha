import pathlib

from pysvg import length, path, svg

from .shared import *


@register_svg
def write_svg_logo(args: SVGArgs):
  lock_width = 14
  lock_stop_height = 2.5
  lock_stop_width = 3.5

  d = path.d([
      path.d.m(0, args.thickness + lock_stop_height),
      path.d.h((lock_width - lock_stop_width) / 2),
      -path.d.v(lock_stop_height),
      path.d.h((lock_stop_width - args.thickness) / 2),
      -path.d.v(args.thickness),
      path.d.h(args.thickness),
      path.d.v(args.thickness),
      path.d.h((lock_stop_width - args.thickness) / 2),
      path.d.v(lock_stop_height),
      path.d.h((lock_width - lock_stop_width) / 2),
      path.d.v(args.thickness),
      -path.placeholder(lambda w, h: path.d.h(w)),
      -path.d.v(args.thickness),
      path.d.z(),

  ])

  s = svg(
      attrs=svg.attrs(
          width=length(d.width, 'mm'),
          height=length(d.height, 'mm'),
          viewBox=(0, 0, d.width, d.height),
      ),
      children=[
          path(attrs=path.attrs(
              d=d,
          ) | args.cut),
      ]
  )

  filename = pathlib.Path(__file__).with_suffix('.svg').name
  return args.output / filename, s
