from os import get_terminal_size

class BoundingBox:
	x1:int
	x2:int
	y1:int
	y2:int

	def __init__(self, x1:int, x2:int, y1:int, y2:int):
		self.set_box_vertices(x1, x2, y1, y2)

	def absolute_x1(self) -> int:
		return self.x1

	def absolute_x2(self) -> int:
		return self.x2

	def absolute_y1(self) -> int:
		return self.y1

	def absolute_y2(self) -> int:
		return self.y2

	def set_box_vertices(self, x1:int, x2:int, y1:int, y2:int) -> None:
		tsize = get_terminal_size()
		self.x1 = min(max(x1, 0), tsize.columns)
		self.x2 = min(max(x2, 0), tsize.columns)
		self.y1 = min(max(y1, 0), tsize.lines)
		self.y2 = min(max(y2, 0), tsize.lines)

	def unpack_vertices(self) -> tuple[int, int, int, int]:
		return self.absolute_x1(), self.absolute_x2(),\
			self.absolute_y1(), self.absolute_y2()

	def notify_resize(self) -> None:
		pass

class ScaledBoundingBox(BoundingBox):
	scale_x:float
	scale_y:float

	apparent_x1:int
	apparent_x2:int
	apparent_y1:int
	apparent_y2:int

	def __init__(self, x1:int, x2:int, y1:int, y2:int, scale_x:float, scale_y:float):
		self.apparent_x1 = x1
		self.apparent_x2 = x2
		self.apparent_y1 = y1
		self.apparent_y2 = y2
		self.scale_x = scale_x
		self.scale_y = scale_y
		super().__init__(
			self.convert_to_absolute(x1, scale_x), 
			self.convert_to_absolute(x2, scale_x), 
			self.convert_to_absolute(y1, scale_y), 
			self.convert_to_absolute(y2, scale_y)
		)

	def convert_to_absolute(self, n:int, scale:float) -> int:
		return round(n * scale)

	def convert_to_absolute_x(self, n:int) -> int:
		return round(n * self.scale_x)

	def convert_to_absolute_y(self, n:int) -> int:
		return round(n * self.scale_y)

	def set_box_vertices(self, x1:int, x2:int, y1:int, y2:int) -> None:
		self.apparent_x1 = x1
		self.apparent_x2 = x2
		self.apparent_y1 = y1
		self.apparent_y2 = y2
		super().set_box_vertices(
			self.convert_to_absolute_x(x1), 
			self.convert_to_absolute_x(x2), 
			self.convert_to_absolute_y(y1), 
			self.convert_to_absolute_y(y2)
		)

	def update_box_vertices(self) -> None:
		super().set_box_vertices(
			self.convert_to_absolute_x(self.apparent_x1), 
			self.convert_to_absolute_x(self.apparent_x2), 
			self.convert_to_absolute_y(self.apparent_y1), 
			self.convert_to_absolute_y(self.apparent_y2)
		)

	def update_scaling_factors(self, sf:float) -> None:
		self.scaling_factor = sf
		self.update_box_vertices()

class TypographySpecificBoundingBox(ScaledBoundingBox):
	def __init__(self, x1:int, x2:int, y1:int, y2:int, font_height_to_width:float):
		super().__init__(x1, x2, y1, y2, font_height_to_width, 1.0)

class ScreenSizeAwareBoundingBox(ScaledBoundingBox):
	screen_to_width_ratio:float

	def __init__(self, x1:int, x2:int, y1:int, y2:int, screen_to_width_ratio:float):
		super().__init__(x1, x2, y1, y2, screen_to_width_ratio)

	def notify_resize(self, w:int, h:int) -> None:
		self.screen_to_width_ratio = 100 / w
		self.update_scaling_factors(self.screen_to_width_ratio, self.screen_to_width_ratio)
