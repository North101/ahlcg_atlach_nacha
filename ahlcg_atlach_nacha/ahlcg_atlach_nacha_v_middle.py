import pathlib

from pysvg import length, path, svg

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  top_path = path.d([
      path.d.h(args.tab * 3),
      path.d.h(args.thickness),
      path.d.h(args.tab * 3),
  ])

  right_path = path.d.v(args.depth)

  bottom_path = -path.d([
      args.h_tab_half(args.tab),
      args.h_tab(args.tab, True),
      args.h_tab_half(args.tab),
      path.d.h(args.thickness),
      args.h_tab_half(args.tab),
      args.h_tab(args.tab, True),
      args.h_tab_half(args.tab),
  ])

  left_path = -right_path

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
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m((top_path.width - args.thickness) / 2, (args.depth - args.depth_tab) / 2),
                  path.d.h(args.thickness),
                  path.d.v(args.depth_tab - (args.kerf * 2)),
                  -path.d.h(args.thickness),
                  -path.d.v(args.depth_tab - (args.kerf * 2)),
                  path.d.z(),
              ]),
          ) | args.cut)
      ],
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  return filename, s
