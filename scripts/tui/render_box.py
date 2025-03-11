from sys import stderr
from typing import Optional, TextIO

from .bounding_box import BoundingBox

FONT_H_T_W_RATIO = 1.5

class RenderBox:
	bounds:BoundingBox
	painted_bounds:Optional[BoundingBox]

	char_rows:list[str]

	def __init__(self, x1:int, x2:int, y1:int, y2:int):
		self.bounds = BoundingBox(x1, x2, y1, y2)
		self.painted_bounds = BoundingBox(x1, x2, y1, y2)

	def paint_row(self, row_n:int, y:int) -> str:
		x1 = self.bounds.absolute_x1()
		x2 = self.bounds.absolute_x2()
		return ' ' * (x2 - x1)

	def paint(self) -> None:
		y1 = self.bounds.absolute_y1()
		y2 = self.bounds.absolute_y2()

		self.char_rows = [self.paint_row(i, y) for i, y in enumerate(range(y1, y2))]

	def render_row(self, row_n:int, y:int, out:TextIO) -> None:
		out.write(self.char_rows[row_n])

	def render(self, out:TextIO) -> None:
		self.tape_over(out)
		leftmost_x = self.bounds.absolute_x1()
		for n, row in enumerate(range(self.bounds.absolute_y1(), self.bounds.absolute_y2())):
			out.write(f"\x1b[{row + 1};{leftmost_x + 1}H")
			self.render_row(n, row, out)

		x1, x2, y1, y2 = self.bounds.unpack_vertices()
		self.painted_bounds = BoundingBox(x1, x2, y1, y2)

	def tape_over(self, out:TextIO) -> None:
		if not self.painted_bounds:
			return

		x1, x2, y1, y2 = self.painted_bounds.unpack_vertices()
		for row in range(y1, y2):
			out.write(f"\x1b[{row + 1};{x1 + 1}H")
			out.write(" " * (x2 - x1))
