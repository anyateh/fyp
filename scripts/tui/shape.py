from abc    import ABC, abstractmethod
from typing import Optional, TextIO

class Shape(ABC):
	@abstractmethod
	def determine_bounding_box_vertices(self) -> tuple[int, int, int, int]:
		pass

	@abstractmethod
	def construct_shape_in_buffer(self) -> None:
		pass

	@abstractmethod
	def flush_shape_in_buffer(self, out:TextIO) -> None:
		pass

	@abstractmethod
	def update_bounding(self,
		x1_limit:Optional[int] = None, x2_limit:Optional[int] = None,
		y1_limit:Optional[int] = None, y2_limit:Optional[int] = None) -> None:
		pass

	@abstractmethod
	def has_overlap_with(self, shape2) -> bool:
		pass

	@abstractmethod
	def blank_painted_region(self, out:TextIO) -> None:
		pass
