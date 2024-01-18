import pathlib

from pysvg import length, path, svg

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  tab = 5

  tab_out = path.d([
      path.d.m(0, 0),
      path.d.h(10),
      args.v_tab_half(tab),
      args.v_tab(tab, True),
      args.v_tab(tab, True),
      args.v_tab_half(tab),
      -path.d.h(10),
      -path.placeholder(lambda w, h: path.d.v(h)),
  ])

  tab_in = path.d([
      path.d.m(10 + args.tab + 2, 0),
      path.d.h(10),
      args.v_tab_half(tab),
      args.v_tab(tab, False),
      args.v_tab(tab, False),
      args.v_tab_half(tab),
      -path.d.h(10),
      -path.placeholder(lambda w, h: path.d.v(h)),
  ])

  d = path.d([
      tab_out,
      tab_in,
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
                  path.d.m(15 + tab - (args.thickness / 2) + args.kerf, tab),
                  path.d.v(tab - (args.kerf * 2)),
                  path.d.h(args.thickness),
                  -path.d.v(tab - (args.kerf * 2)),
                  -path.d.h(args.thickness),
              ]),
          ) | args.cut),
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m(15 + tab - (args.thickness / 2) + args.kerf, tab * 3),
                  path.d.v(tab - (args.kerf * 2)),
                  path.d.h(args.thickness),
                  -path.d.v(tab - (args.kerf * 2)),
                  -path.d.h(args.thickness),
              ]),
          ) | args.cut),
      ]
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  return filename, s
