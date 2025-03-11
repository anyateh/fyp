from sys import stderr
from typing import TextIO

from .bounding_box import BoundingBox

FONT_H_T_W_RATIO = 1.5

class RenderBox:
	bounds:BoundingBox
	painted_bounds:BoundingBox

	char_rows:list[str]

	def __init__(self, x1:int, x2:int, y1:int, y2:int):
		self.bounds = BoundingBox(x1, x2, y1, y2)
		self.previous_bounds = BoundingBox(0, 0, 0, 0)

	def paint(self) -> None:
		x1 = self.bounds.absolute_x1()
		x2 = self.bounds.absolute_x2()
		y1 = self.bounds.absolute_y1()
		y2 = self.bounds.absolute_y2()

		self.char_rows = [' ' * (x2 - x1)] * (y2 - y1)

	def render_row(self, row_n:int, y:int, out:TextIO) -> None:
		out.write(self.char_rows[row_n])

	def render(self, out:TextIO) -> None:
		leftmost_x = self.bounds.absolute_x1()
		for n, row in enumerate(range(self.bounds.absolute_y1(), self.bounds.absolute_y2())):
			out.write(f"\x1b[{row + 1};{leftmost_x + 1}H")
			self.render_row(n, row, out)

		self.painted_bounds = self.bounds
