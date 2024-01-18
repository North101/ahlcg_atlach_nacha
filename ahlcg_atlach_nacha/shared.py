import math
import pathlib
from typing import NamedTuple, Protocol

from pysvg import PresentationAttributes, path, svg


class SVGArgs(NamedTuple):
  output: pathlib.Path
  width: float
  height: float
  depth: float
  thickness: float
  kerf: float
  hole: bool
  tab: float
  depth_tab: float
  finger_cutout: float
  icon: pathlib.Path
  icon_scale: float
  icon_width: float
  icon_height: float

  def h_tab_half(self, tab):
    return path.d.h(tab / 2)

  def h_tab(self, tab: float, out: bool):
    kerf = -self.kerf if out else self.kerf
    thickness = -path.d.v(self.thickness) if out else path.d.v(self.thickness)
    return path.d([
        path.d.h((tab / 2) + kerf),
        thickness,
        path.d.h(tab + -kerf + -kerf),
        -thickness,
        path.d.h(kerf + (tab / 2)),
    ])

  def h_tabs(self, tab: float, width: float, out: bool):
    h_tab = self.h_tab(tab, out)
    count = math.floor(width / h_tab.width)
    return path.d([
        h_tab
        for _ in range(count)
    ])

  def v_tab_half(self, tab):
    return path.d.v(tab / 2)

  def v_tab(self, tab: float, out: bool):
    kerf = -self.kerf if out else self.kerf
    thickness = -path.d.h(self.thickness) if out else path.d.h(self.thickness)
    return path.d([
        path.d.v((tab / 2) + kerf),
        -thickness,
        path.d.v(tab + -kerf + -kerf),
        thickness,
        path.d.v(kerf + (tab / 2)),
    ])

  def v_tabs(self, tab: float, height: float, out: bool):
    v_tab = self.v_tab(tab, out)
    count = math.floor(height / v_tab.height)
    return path.d([
        v_tab
        for _ in range(count)
    ])

  cut = PresentationAttributes(
      fill='none',
      stroke='black',
      stroke_width=0.001,
  )

  engrave = PresentationAttributes(
      fill='black',
      stroke='none',
      stroke_width=0.001,
  )


class RegisterSVGCallable(Protocol):
  def __call__(self, args: SVGArgs) -> tuple[pathlib.Path, svg]:
    ...


svg_list: list[RegisterSVGCallable] = []


def register_svg(f: RegisterSVGCallable):
  svg_list.append(f)
  return f


def write_all_svg(args: SVGArgs):
  args.output.mkdir(parents=True, exist_ok=True)
  data = [
      write_svg(args)
      for write_svg in svg_list
  ]
  for (filename, svg_data) in data:
    filename.write_text(format(svg_data, '.3f'))

  return data
