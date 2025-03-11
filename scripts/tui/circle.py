from .colour_render import UniColourRender
from .render_box    import RenderBox

from typing import TextIO

class Ellipse(RenderBox):
	center_x:int
	center_y:int

	x_radius:int
	y_radius:int

	def __init__(self, x:int, y:int, radius_x:int, radius_y:int):
		super().__init__(x - radius_x, x + radius_x + 1, y - radius_y, y + radius_y + 1)
		self.center_x = x
		self.center_y = y
		self.x_radius = radius_x
		self.y_radius = radius_y

	def _determine_vertices(self) -> tuple[int, int, int, int]:
		return                                 \
			self.center_x - self.x_radius,     \
			self.center_x + self.x_radius + 1, \
			self.center_y - self.y_radius,     \
			self.center_y + self.y_radius + 1

	def set_center(self, x:int, y:int) -> None:
		self.center_x = x
		self.center_y = y

		x1, x2, y1, y2 = self._determine_vertices()
		self.bounds.set_box_vertices(x1, x2, y1, y2)

	def set_x_radius(self, rad:int) -> None:
		self.x_radius = rad

		x1, x2, y1, y2 = self._determine_vertices()
		self.bounds.set_box_vertices(x1, x2, y1, y2)

	def set_y_radius(self, rad:int) -> None:
		self.y_radius = rad

		x1, x2, y1, y2 = self._determine_vertices()
		self.bounds.set_box_vertices(x1, x2, y1, y2)

class FilledEllipse(Ellipse):
	fill_col:UniColourRender

	def __init__(self, x:int, y:int, radius_x:int, radius_y:int, r:int, g:int, b:int, x2_limit:int = None):
		super().__init__(x, y, radius_x, radius_y)

		self.fill_col = UniColourRender(r, g, b)

	def paint(self):
		x1, x2, y1, y2 = self.bounds.unpack_vertices()
		width = x2 - x1
		height = y2 - y1

		# The resulting scaled shape is an ellipse
		hori_radius = ((width - 1) // 2)
		vert_radius = ((height - 1) // 2)

		def gen_ansi_fmt(y:int) -> str:
			yr_sqrt_1_min_k = hori_radius * (1 - (y - vert_radius)**2 / vert_radius**2)**0.5

			start_x = round(-yr_sqrt_1_min_k + hori_radius)
			end_x   = round(yr_sqrt_1_min_k + hori_radius)

			chord_len = end_x - start_x

			return "\x1b[{}C".format(start_x + 1) + self.fill_col.ansi_set_bg_colour_256() + " " * chord_len + self.fill_col.ansi_colour_reset()

		self.char_rows = [
			gen_ansi_fmt(i) for i in range(self.y_radius * 2 + 1)
		]

		# self.char_rows = [
		# 	[
		# 		'o' if is_inside_ellipse(j, i) else ' ' for j in range(width)
		# 	] for i in range(height)
		# ]

		self.char_rows[0] = self.fill_col.ansi_set_fg_colour_256() + self.char_rows[0]
		self.char_rows[self.y_radius * 2] += self.fill_col.ansi_colour_reset()
		
		# self.char_rows = [''.join(i) for i in self.char_rows]
