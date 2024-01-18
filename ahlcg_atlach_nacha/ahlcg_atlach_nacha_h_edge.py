import pathlib

from pysvg import length, path, svg

from .shared import *


@register_svg
def write_svg(args: SVGArgs):

  top_path = path.d([
      path.d.h(args.thickness),
      path.d.h(args.tab * 3),
  ])

  right_path = path.d.v(args.depth)

  bottom_path = -path.d([
      args.h_tab_half(args.tab),
      args.h_tab(args.tab, True),
      args.h_tab_half(args.tab),
      path.d.h(args.thickness),
  ])

  left_path = -path.d([
      path.placeholder(lambda w, h: path.d.v((args.depth - h) / 2)),
      args.v_tab(args.depth_tab, False),
      path.placeholder(lambda w, h: path.d.v((args.depth - h) / 2)),
  ])

  d = path.d([
      path.d.m(0, 0),
      top_path,
      right_path,
      bottom_path,
      left_path,
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
      ],
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  return filename, s
