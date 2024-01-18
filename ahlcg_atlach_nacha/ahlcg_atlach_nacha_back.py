import pathlib

from pysvg import Element, g, length, path, rect, svg, transforms

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  total_height = args.thickness + args.height + args.thickness + args.height + args.thickness
  half_cutout = args.finger_cutout / 2

  top_path = path.d([
      args.h_tab_half(args.tab),
      args.h_tabs(args.tab, args.tab * 2, False),
      path.placeholder(lambda w, h: path.d.h((args.width - w) / 2)),
      args.h_tab_half(args.tab),
      path.d.v(args.thickness),
      path.d.c(0, half_cutout, half_cutout, half_cutout, half_cutout, half_cutout),
      path.d.c(0, 0, half_cutout, 0, half_cutout, -half_cutout),
      -path.d.v(args.thickness),
      args.h_tab_half(args.tab),
      path.placeholder(lambda w, h: path.d.h((args.width - w) / 2)),
      args.h_tabs(args.tab, args.tab * 2, False),
      args.h_tab_half(args.tab),
  ])

  top_right_path = path.d([
      path.d.v(args.thickness),
      args.v_tab_half(args.tab),
      args.v_tabs(args.tab, args.tab * 2, False),
      path.placeholder(lambda w, h: path.d.v(((args.height + args.thickness) / 2) - h)),
  ])

  top_left_path = -path.d([
      path.placeholder(lambda w, h: path.d.v(((args.height + args.thickness) / 2) - h)),
      args.v_tabs(args.tab, args.tab * 2, False),
      args.v_tab_half(args.tab),
      path.d.v(args.thickness),
  ])

  right_path = path.d([
      path.d.v(args.thickness),
      args.v_tab_half(args.tab),
      args.v_tabs(args.tab, args.tab * 2, False),
      path.placeholder(lambda w, h: path.d.v((total_height - h) / 2)),
      args.v_tabs(args.tab, args.tab * 2, False),
      args.v_tab_half(args.tab),
      path.d.v(args.thickness),
      args.v_tab_half(args.tab),
      args.v_tabs(args.tab, args.tab * 2, False),
      path.placeholder(lambda w, h: path.d.v((total_height - h) / 2)),
      args.v_tabs(args.tab, args.tab * 2, False),
      args.v_tab_half(args.tab),
      path.d.v(args.thickness),
  ])

  d = path.d([
      path.d.m(0, 0),
      path.d([
          path.d.h(args.thickness),
          top_path,
          path.d.h(args.thickness),
          top_right_path,
          top_path,
          top_left_path,
          path.d.h(args.thickness),
          top_path,
          path.d.h(args.thickness),
      ]),
      right_path,
      -path.d([
          path.d.h(args.thickness),
          top_path,
          path.d.h(args.thickness),
          top_right_path,
          top_path,
          top_left_path,
          path.d.h(args.thickness),
          top_path,
          path.d.h(args.thickness),
      ]),
      -right_path,
      path.d.z(),
  ])

  h_slot = path.d([
      path.d.m((args.tab / 2) + args.kerf, 0),
      path.d.h(args.tab - (args.kerf * 2)),
      path.d.v(args.thickness),
      -path.d.h(args.tab - (args.kerf * 2)),
      -path.d.v(args.thickness),
      path.d.m(args.tab + (args.tab / 2) + args.kerf, 0),
  ])

  v_slot = path.d([
      path.d.m(0, (args.tab / 2) + args.kerf),
      path.d.v(args.tab - (args.kerf * 2)),
      path.d.h(args.thickness),
      -path.d.v(args.tab - (args.kerf * 2)),
      -path.d.h(args.thickness),
      path.d.m(0, args.tab + (args.tab / 2) + args.kerf),
  ])

  children = list[Element | str]()
  if args.icon:
    children.append(g(
        attrs=g.attrs(transform=transforms.translate(
            x=(((args.thickness + args.width) * 3) + args.thickness - (args.icon_width * args.icon_scale)) / 2,
            y=(((args.thickness + args.height) * 2) + args.thickness - (args.icon_height * args.icon_scale)) / 2,
        )),
        children=[
            g(
                attrs=g.attrs(transform=transforms.scale(args.icon_scale)) | args.engrave,
                children=[
                    args.icon.read_text().strip(),
                ],
            ),
        ],
    ))
  if args.hole:
    hole_size = args.thickness - args.kerf
    children.append(rect(attrs=rect.attrs(
        x=(((args.thickness + args.width) * 3) + args.thickness - hole_size) / 2,
        y=(((args.thickness + args.height) * 2) + args.thickness - hole_size) / 2,
        width=hole_size,
        height=hole_size,
    ) | args.cut))

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
                  path.d.m(args.thickness + (args.tab / 2), args.thickness + args.height),
                  h_slot,
                  path.d.z(),
              ]),
          ) | args.cut),
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m(args.thickness + args.width - h_slot.width - (args.tab / 2) +
                           (args.kerf * 2), args.thickness + args.height),
                  h_slot,
                  path.d.z(),
              ]),
          ) | args.cut),
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m(((args.thickness + args.width) * 2) + args.thickness +
                           (args.tab / 2), args.thickness + args.height),
                  h_slot,
                  path.d.z(),
              ]),
          ) | args.cut),
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m(((args.thickness + args.width) * 3) -
                           h_slot.width - (args.tab / 2) + (args.kerf * 2), args.thickness + args.height),
                  h_slot,
                  path.d.z(),
              ]),
          ) | args.cut),
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m(args.thickness + args.width, args.thickness +
                           (args.height / 2) + ((args.thickness + args.tab) / 2)),
                  v_slot,
                  path.d.z(),
              ]),
          ) | args.cut),
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m(args.thickness + args.width, args.thickness +
                           args.height - (args.tab / 2) - (v_slot.height) + (args.kerf * 2)),
                  v_slot,
                  path.d.z(),
              ]),
          ) | args.cut),
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m(args.thickness + args.width, args.thickness +
                           args.height + args.thickness + (args.tab / 2)),
                  v_slot,
                  path.d.z(),
              ]),
          ) | args.cut),
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m(args.thickness + args.width, args.thickness + (args.height / 2) +
                           args.thickness + args.height - v_slot.height - ((args.thickness + args.tab) / 2) + (args.kerf * 2)),
                  v_slot,
                  path.d.z(),
              ]),
          ) | args.cut),
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m(args.thickness + args.width + args.thickness + args.width,
                           args.thickness + (args.height / 2) + ((args.thickness + args.tab) / 2)),
                  v_slot,
                  path.d.z(),
              ]),
          ) | args.cut),
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m(args.thickness + args.width + args.thickness + args.width, args.thickness +
                           args.height - (args.tab / 2) - v_slot.height + (args.kerf * 2)),
                  v_slot,
                  path.d.z(),
              ]),
          ) | args.cut),
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m(args.thickness + args.width + args.thickness + args.width, args.thickness +
                           args.height + args.thickness + (args.tab / 2)),
                  v_slot,
                  path.d.z(),
              ]),
          ) | args.cut),
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m(args.thickness + args.width + args.thickness + args.width, args.thickness + (args.height / 2) +
                           args.thickness + args.height - v_slot.height - ((args.thickness + args.tab) / 2) + (args.kerf * 2)),
                  v_slot,
                  path.d.z(),
              ]),
          ) | args.cut),
          *children,
      ],
  )

  filename = pathlib.Path(__file__).with_suffix('.svg').name
  return args.output / filename, s
