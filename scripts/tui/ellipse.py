from .colour_render import UniColourRender
from .render_box    import RenderBox
from .shape         import Shape

from typing import Optional, TextIO

class Ellipse(RenderBox, Shape):
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
		if self.y_radius == 0.0:
			return 0.0, 0.0

		x_minus_center_x_nosign_solution = self.x_radius               \
				* (1 - (y - self.center_y)**2 / self.y_radius**2)**0.5

		return \
			round(-x_minus_center_x_nosign_solution + self.center_x), \
			round( x_minus_center_x_nosign_solution + self.center_x)

	def _determine_ellipse_eqn_solns_y(self, x:int) -> tuple[int, int]:
		if self.x_radius == 0.0:
			return 0.0, 0.0

		y_minus_center_y_nosign_solution = self.y_radius               \
				* (1 - (x - self.center_x)**2 / self.x_radius**2)**0.5

		return \
			round(-y_minus_center_y_nosign_solution + self.center_y), \
			round( y_minus_center_y_nosign_solution + self.center_y)

	def _update_ellipse_eqn_solns(self) -> None:
		self.ellipse_eqn_solns = \
			[self._determine_ellipse_eqn_solns(y)
				for y in range(self.center_y - self.y_radius, self.center_y
						+ self.y_radius + 1)]

	def determine_bounding_box_vertices(self) -> tuple[int, int, int, int]:
		return                                 \
			self.center_x - self.x_radius,     \
			self.center_x + self.x_radius + 1, \
			self.center_y - self.y_radius,     \
			self.center_y + self.y_radius + 1

	def set_center(self, x:int, y:int) -> None:
		self.center_x = x
		self.center_y = y

		self._update_ellipse_eqn_solns()

		x1, x2, y1, y2 = self.determine_bounding_box_vertices()
		self.bounds.set_box_vertices(x1, x2, y1, y2)

	def set_x_radius(self, rad:int) -> None:
		self.x_radius = rad

		self._update_ellipse_eqn_solns()

		x1, x2, y1, y2 = self.determine_bounding_box_vertices()
		self.bounds.set_box_vertices(x1, x2, y1, y2)

	def set_y_radius(self, rad:int) -> None:
		self.y_radius = rad

		self._update_ellipse_eqn_solns()

		x1, x2, y1, y2 = self.determine_bounding_box_vertices()
		self.bounds.set_box_vertices(x1, x2, y1, y2)

	def construct_shape_in_buffer(self) -> None:
		self.paint()

	def flush_shape_in_buffer(self, out:TextIO) -> None:
		self.render(out)

	def update_bounding(self,
		x1_limit:Optional[int] = None, x2_limit:Optional[int] = None,
		y1_limit:Optional[int] = None, y2_limit:Optional[int] = None) -> None:
		x1, x2, y1, y2 = self.determine_bounding_box_vertices()
		self.bounds.set_box_vertices(
			max(x1, x1_limit), min(x2, x2_limit),
			max(y1, y1_limit), min(y2, y2_limit)
		)

	def has_overlap_with(self, shape2) -> bool:
		return self.bounds.has_overlap_with(shape2.bounds)

	def blank_painted_region(self, out:TextIO) -> None:
		self.tape_over(out)

class FilledEllipse(Ellipse):
	fill_col:UniColourRender

	def __init__(self, x:int, y:int, radius_x:int, radius_y:int, r:int, g:int, b:int):
		super().__init__(x, y, radius_x, radius_y)

		self.fill_col = UniColourRender(r, g, b)

	def paint_row(self, row_n:int, y:int) -> str:
		if self.x_radius == 0.0 or self.y_radius == 0:
			return ""

		bound_x1 = self.bounds.absolute_x1()
		bound_x2 = self.bounds.absolute_x2()

		if bound_x2 - bound_x1 <= 0:
			return ""

		start_x  = min(max(self.ellipse_eqn_solns[row_n][0], bound_x1), bound_x2)
		end_x    = min(max(self.ellipse_eqn_solns[row_n][1], bound_x1), bound_x2)
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

	def draw_left_half(self, row_n:int, bound_x1:int, bound_x2:int) -> str:
		start_x_above = self.ellipse_eqn_solns[row_n - 1][0]          \
				if row_n != 0 else None
		start_x_below = self.ellipse_eqn_solns[row_n + 1][0]          \
				if row_n != len(self.ellipse_eqn_solns) - 1 else None
		start_x = self.ellipse_eqn_solns[row_n][0]
		if start_x_above != None:
			start_x_above -= bound_x1
		if start_x_below != None:
			start_x_below -= bound_x1
		start_x       -= bound_x1

		start_x_draw_end = start_x + 1
		if start_x_above != None and start_x_above > start_x:
			start_x_draw_end = start_x_above
		elif start_x_below != None and start_x_below > start_x:
			start_x_draw_end = start_x_below

		start_x_draw_end_limit = bound_x2 - bound_x1
		if start_x_draw_end <= 0 or start_x >= start_x_draw_end_limit:
			return ""

		start_x = max(start_x, 0)
		start_x_draw_end = min(start_x_draw_end, start_x_draw_end_limit)
		return ("\x1b[{}C".format(start_x) if start_x > 0 else "") \
			+ "*" * (start_x_draw_end - start_x)

	def paint_row(self, row_n:int, y:int) -> str:
		if self.x_radius == 0.0 or self.y_radius == 0:
			return ""

		bound_x1 = self.bounds.absolute_x1()
		bound_x2 = self.bounds.absolute_x2()

		if bound_x2 - bound_x1 <= 0:
			return ""

		# start_str = self.draw_left_half(row_n, bound_x1, bound_x2)

		# return self.fill_col.ansi_set_fg_colour_256() + start_str

		shape_top = self.center_y - self.y_radius
		relative_y = y - shape_top

		start_x = self.ellipse_eqn_solns[relative_y][0]
		end_x   = self.ellipse_eqn_solns[relative_y][1]

		start_x -= bound_x1
		end_x   -= bound_x1

		right_limit = bound_x2 - bound_x1

		chord_len = end_x - max(start_x, 0)

		draw_start_str = 0 <= start_x <= right_limit

		start_str = "".join((
			"\x1b[{}C".format(start_x) if start_x > 0 else "",
			"*"
		)) if draw_start_str else ""

		if draw_start_str:
			chord_len -= 1

		end_str   = "".join((
			"\x1b[{}C".format(chord_len) if chord_len > 0 else "",
			"*"
		)) if 0 <= end_x <= right_limit and end_x != start_x else ""

		return "{}{}{}{}".format(
			self.fill_col.ansi_set_fg_colour_256(),
			start_str,
			end_str,
			self.fill_col.ansi_colour_reset()
		)

		return "{}{}{}".format(
			("\x1b[{}C".format(start_x) if start_x > 0 else "")
				+ self.fill_col.ansi_set_fg_colour_256()
				+ ("*"),
			("\x1b[{}C".format(chord_len) if chord_len > 0 else ""),
			("*" if end_x != start_x else "") + self.fill_col.ansi_colour_reset()
		)

	def paint(self) -> None:
		y1 = self.bounds.absolute_y1()
		y2 = self.bounds.absolute_y2()

		self.char_rows = [self.paint_row(i, y) for i, y in enumerate(range(y1, y2))]
