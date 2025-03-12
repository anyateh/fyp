from .screen import Screen

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
	from ..conductor.manage_antes import AntennaNode
else:
	AntennaNode = 'AntennaNode'

class AntennaScreen(Screen):
	antennas:list[AntennaNode] = []

	ante_min_x:Optional[float] = None
	ante_min_y:Optional[float] = None
	ante_max_x:Optional[float] = None
	ante_max_y:Optional[float] = None

	padding_x:int = 4
	padding_y:int = 2

	x_scale:float = 1.0
	y_scale:float = 1.0
	x_offset:float = 0.0
	y_offset:float = 0.0

	# Call when antenna coordinates change
	def update_antenna_boundings(self) -> None:
		self.ante_min_x = None
		self.ante_min_y = None
		self.ante_max_x = None
		self.ante_max_y = None
		for ante in self.antennas:
			self.update_antenna_bounding_new_xy(ante.x, ante.y)
		self.update_scale_offset()

	def update_antenna_bounding_new_xy(self, x:float, y:float) -> None:
		# Lowest X-coordinate
		self.ante_min_x = min(self.ante_min_x, x) \
			if self.ante_min_x != None else x
		# Highest X-coordinate
		self.ante_max_x = max(self.ante_max_x, x) \
			if self.ante_max_x != None else x
		# Lowest Y-coordinate
		self.ante_min_y = min(self.ante_min_y, y) \
			if self.ante_min_y != None else x
		# Highest Y-coordinate
		self.ante_max_y = max(self.ante_max_y, y) \
			if self.ante_max_y != None else x

	def add_antenna(self, antenna:AntennaNode) -> None:
		self.antennas.append(antenna)
		self.add_item(antenna.ring)

		self.update_antenna_bounding_new_xy(antenna.x, antenna.y)
		self.update_scale_offset()
		self.due_to_clear = True

	def remove_antenna(self, antenna:AntennaNode) -> None:
		if antenna in self.antennas:
			self.antennas.remove(antenna)

		if antenna.ring in self.layers:
			self.layers.remove(antenna.ring)

	# Call when terminal screen is resized
	def on_resize(self):
		self.update_scale_offset()
		super().on_resize()

	# Call when antenna readings gets updated
	def update_antennas(self) -> None:
		for ante in self.antennas:
			self.update_antenna(ante)

		for entry in self.layers:
			entry[1] = True

	def get_viewport_width(self) -> int:
		return self.get_width() - self.padding_x * 2

	def get_viewport_height(self) -> int:
		return self.get_height() - self.padding_y * 2

	def update_scale_offset(self) -> None:
		self.x_offset = 0.0 if self.ante_min_x == None else self.ante_min_x
		self.y_offset = 0.0 if self.ante_max_y == None else self.ante_max_y

		if self.ante_min_x != None and self.ante_max_x != None:
			coord_width = self.ante_max_x - self.ante_min_x
			self.x_scale = 1.0 if coord_width == 0 else self.get_viewport_width() / coord_width
		else:
			self.x_scale = 1.0

		if self.ante_min_y != None and self.ante_max_y != None:
			coord_height = self.ante_min_y - self.ante_max_y
			self.y_scale = -1.0 if coord_height == 0 else self.get_viewport_height() / coord_height
		else:
			self.y_scale = -1.0

	def map_x_to_screen(self, x:float) -> int:
		return int((x - self.x_offset) * self.x_scale) + self.padding_x

	def map_y_to_screen(self, y:float) -> int:
		return int((y - self.y_offset) * self.y_scale) + self.padding_y

	def update_antenna(self, antenna:AntennaNode) -> None:
		antenna.ring.set_center(self.map_x_to_screen(antenna.x), self.map_y_to_screen(antenna.y))
		antenna.ring.set_x_radius(int(antenna.inverse_friis() * self.x_scale))
		antenna.ring.set_y_radius(int(abs(antenna.inverse_friis() * self.y_scale)))

		# print(self.x_scale, self.y_scale, self.x_offset, self.y_offset, file = stderr)
