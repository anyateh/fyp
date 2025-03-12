from os import get_terminal_size
from typing import TextIO

from .render_box import RenderBox
from .shape      import Shape

class Screen:
	layers:list[list[Shape, bool]] = []

	prev_x:int
	prev_y:int
	prev_width:int
	prev_height:int

	due_to_clear:bool = True

	def __init__(self):
		self.update_current_dimensions()

	def update_current_dimensions(self) -> None:
		self.prev_x = 0
		self.prev_y = 0
		self.prev_width = self.get_width()
		self.prev_height = self.get_height()

	def dimensions_disparity_detected(self) -> bool:
		return self.prev_x != 0 or self.prev_y != 0 or \
			self.prev_width != self.get_width()     or \
			self.prev_height != self.get_height()

	def add_item(self, item:Shape) -> None:
		self.layers.append([item, True])

	def insert_item_below(self, item_to_insert:Shape,
						  existing_item_right_above:Shape) -> None:
		if existing_item_right_above in self.layers:
			self.layers.insert(self.layers.index(existing_item_right_above), item_to_insert)

	def get_item_at(self, i:int) -> Shape:
		return self.layers[i]

	def mark_item_for_paint(self, item:Shape) -> None:
		for entry in (i for i in self.layers if item.has_overlap_with(i[0])):
			entry[1] = True

	def get_width(self) -> int:
		return get_terminal_size().columns

	def get_height(self) -> int:
		return get_terminal_size().lines

	def on_resize(self) -> None:
		self.due_to_clear = True
		for entry in self.layers:
			entry[0].update_bounding(
				0, self.get_width(),
				0, self.get_width()
			)
			entry[1] = True

	def paint(self) -> None:
		for entry in self.layers:
			if entry[1]:
				entry[0].construct_shape_in_buffer()
				entry[1] = False

	def render(self, out:TextIO) -> None:
		if self.dimensions_disparity_detected():
			self.update_current_dimensions()

		if self.due_to_clear:
			self.clear(out)
			self.due_to_clear = False

		for entry in filter(lambda a: a[1], self.layers):
			entry[0].blank_painted_region(out)

		for entry in self.layers:
			if entry[1]:
				entry[0].construct_shape_in_buffer()
				entry[1] = False

			entry[0].flush_shape_in_buffer(out)

	def clear(self, out:TextIO) -> None:
		out.write("\x1b[2J")
