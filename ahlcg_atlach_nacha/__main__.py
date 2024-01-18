import argparse
import pathlib

from .shared import *


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--output',
                      type=pathlib.Path, default='output', help='output path')
  parser.add_argument('--width',
                      type=float, default=63, help='card width (mm)')
  parser.add_argument('--height',
                      type=float, default=89, help='card height (mm)')
  parser.add_argument('--depth',
                      type=float, default=4, help='card stack depth (mm)')
  parser.add_argument('--thickness',
                      type=float, default=3.17, help='wood thickness (mm)')
  parser.add_argument('--kerf',
                      type=float, default=0.07, help='kerf (mm)')
  parser.add_argument('--hole',
                      type=bool, default=True, help='add a hole for the lazy susan')

  parser.add_argument('--tab',
                      type=float, default=4, help='tab size (mm)')
  parser.add_argument('--depth_tab',
                      type=float, default=2, help='depth tab size (mm)')
  parser.add_argument('--finger_cutout',
                      type=float, default=20, help='size of the finger cutout (mm)')
  parser.add_argument('--icon',
                      type=lambda value: pathlib.Path(value) if value else None, default=None, help='logo')
  parser.add_argument('--icon_scale',
                      type=float, default=2, help='logo scale')
  parser.add_argument('--icon_width',
                      type=float, default=32, help='logo width')
  parser.add_argument('--icon_height',
                      type=float, default=32, help='logo height')

  return parser.parse_args()


def main():
  args = parse_args()
  svgs = write_all_svg(args=SVGArgs(
      output=args.output,
      width=args.width,
      height=args.height,
      depth=args.depth,
      thickness=args.thickness,
      kerf=args.kerf,
      hole=args.hole,
      tab=args.tab,
      depth_tab=args.depth_tab,
      finger_cutout=args.finger_cutout,
      icon=args.icon,
      icon_scale=args.icon_scale,
      icon_width=args.icon_width,
      icon_height=args.icon_height,
  ))

  data = [
      (str(filename), svg.attrs.width, svg.attrs.height)
      for (filename, svg) in svgs
  ]
  name_len = max(len(name) for (name, _, _) in data)
  width_len = max(len(f'{width:.2f}') for (_, width, _) in data)
  height_len = max(len(f'{height:.2f}') for (_, _, height) in data)
  for (name, width, height) in data:
    print(f'{name:<{name_len}} @ {width:>{width_len}.2f} x {height:>{height_len}.2f}')


if __name__ == '__main__':
  main()
