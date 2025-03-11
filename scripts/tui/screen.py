from os import get_terminal_size
from typing import TextIO

from .render_box import RenderBox

class Screen:
	layers:list[RenderBox] = []

	def add_item(self, item:RenderBox) -> None:
		self.layers.append(item)

	def insert_item_below(self, item_to_insert:RenderBox,
						  existing_item_right_above:RenderBox) -> None:
		if existing_item_right_above in self.layers:
			self.layers.insert(self.layers.index(existing_item_right_above), item_to_insert)

	def get_item_at(self, i:int) -> RenderBox:
		return self.layers[i]

	def get_width(self) -> int:
		return get_terminal_size().columns

	def get_height(self) -> int:
		return get_terminal_size().rows

	def on_resize(self) -> None:
		pass

	def paint(self) -> None:
		for item in self.layers:
			item.paint()

	def render(self, out:TextIO) -> None:
		for item in self.layers:
			item.render(out)
