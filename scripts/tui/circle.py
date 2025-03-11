from .colour_render import UniColourRender
from .render_box    import RenderBox

from typing import TextIO

class Ellipse(RenderBox):
	center_x:int
	center_y:int

	x_radius:int
	y_radius:int

	ellipse_eqn_solns:list[tuple[int, int]]

	def __init__(self, x:int, y:int, radius_x:int, radius_y:int):
		super().__init__(x - radius_x, x + radius_x + 1, y - radius_y, y + radius_y + 1)
		self.center_x = x
		self.center_y = y
		self.x_radius = radius_x
		self.y_radius = radius_y

		self._update_ellipse_eqn_solns()

	def _determine_ellipse_eqn_solns(self, y:int) -> tuple[int, int]:
		x_minus_center_x_nosign_solution = self.x_radius               \
				* (1 - (y - self.center_y)**2 / self.y_radius**2)**0.5

		return \
			round(-x_minus_center_x_nosign_solution + self.center_x), \
			round( x_minus_center_x_nosign_solution + self.center_x)

	def _update_ellipse_eqn_solns(self) -> None:
		self.ellipse_eqn_solns = \
			[self._determine_ellipse_eqn_solns(y)
				for y in range(self.center_y - self.y_radius, self.center_y
						+ self.y_radius + 1)]

	def _determine_vertices(self) -> tuple[int, int, int, int]:
		return                                 \
			self.center_x - self.x_radius,     \
			self.center_x + self.x_radius + 1, \
			self.center_y - self.y_radius,     \
			self.center_y + self.y_radius + 1

	def set_center(self, x:int, y:int) -> None:
		self.center_x = x
		self.center_y = y

		self._update_ellipse_eqn_solns()

		x1, x2, y1, y2 = self._determine_vertices()
		self.bounds.set_box_vertices(x1, x2, y1, y2)

	def set_x_radius(self, rad:int) -> None:
		self.x_radius = rad

		self._update_ellipse_eqn_solns()

		x1, x2, y1, y2 = self._determine_vertices()
		self.bounds.set_box_vertices(x1, x2, y1, y2)

	def set_y_radius(self, rad:int) -> None:
		self.y_radius = rad

		self._update_ellipse_eqn_solns()

		x1, x2, y1, y2 = self._determine_vertices()
		self.bounds.set_box_vertices(x1, x2, y1, y2)

class FilledEllipse(Ellipse):
	fill_col:UniColourRender

	def __init__(self, x:int, y:int, radius_x:int, radius_y:int, r:int, g:int, b:int):
		super().__init__(x, y, radius_x, radius_y)

		self.fill_col = UniColourRender(r, g, b)

	def paint_row(self, row_n:int, y:int) -> str:
		bound_x1 = self.bounds.absolute_x1()
		bound_x2 = self.bounds.absolute_x2()

		if bound_x2 - bound_x1 <= 0:
			return ""

		yr_sqrt_1_min_k = self.x_radius * (1 - (y - self.center_y)**2 / self.y_radius**2)**0.5

		start_x = min(max(self.ellipse_eqn_solns[row_n][0], bound_x1), bound_x2)
		end_x   = min(max(self.ellipse_eqn_solns[row_n][1], bound_x1), bound_x2)
		start_x -= bound_x1
		end_x   -= bound_x1

		chord_len = end_x - start_x

		return "{}{}{}".format(
			("\x1b[{}C".format(start_x) if start_x > 0 else "")
				+ self.fill_col.ansi_set_bg_colour_256(),
			" " * chord_len,
			self.fill_col.ansi_colour_reset()
		)

class OutlineEllipse(FilledEllipse):
	def __init__(self, x, y, radius_x, radius_y, r, g, b):
		super().__init__(x, y, radius_x, radius_y, r, g, b)

	def paint_row(self, row_n:int, y:int) -> str:
		bound_x1 = self.bounds.absolute_x1()
		bound_x2 = self.bounds.absolute_x2()

		if bound_x2 - bound_x1 <= 0:
			return ""

		yr_sqrt_1_min_k = self.x_radius * (1 - (y - self.center_y)**2 / self.y_radius**2)**0.5

		start_x = min(max(self.ellipse_eqn_solns[row_n][0], bound_x1), bound_x2)
		end_x   = min(max(self.ellipse_eqn_solns[row_n][1], bound_x1), bound_x2)

		start_x -= bound_x1
		end_x   -= bound_x1

		chord_len = end_x - start_x

		return "{}{}{}".format(
			("\x1b[{}C".format(start_x) if start_x > 0 else "")
				+ self.fill_col.ansi_set_fg_colour_256()
				+ ("*"),
			("\x1b[{}C".format(chord_len) if chord_len > 0 else ""),
			("*" if end_x != start_x else "") + self.fill_col.ansi_colour_reset()
		)
