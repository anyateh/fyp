from typing import TypeVar, Union

AverageFIFO = TypeVar("AverageFIFO")

class AverageFIFO:
	buffer = []
	capacity:int

	readings_sum = 0.0

	current_ptr = 0

	def __init__(self, last_n_readings:int = 16) -> None:
		self.capacity = last_n_readings
		self.buffer = []

	def __increment_ptr(self) -> None:
		self.current_ptr += 1
		if self.current_ptr >= self.capacity:
			self.current_ptr = 0

	def add(self, reading:float) -> None:
		if len(self.buffer) < self.capacity:
			self.buffer.append(reading)
			self.readings_sum += reading
			self.__increment_ptr()
			return

		self.readings_sum -= self.buffer[self.current_ptr]
		self.buffer[self.current_ptr] = reading
		self.readings_sum += reading
		self.__increment_ptr()

	def avg(self) -> float:
		nitems = len(self.buffer)
		if nitems == 0:
			return 0
		return self.readings_sum / nitems

	def clear(self) -> None:
		self.buffer.clear()
		self.readings_sum = 0.0
		self.current_ptr = 0

	def clone_to_size(self, size:int) -> AverageFIFO:
		new_a = AverageFIFO(size)

		for i in self:
			new_a.add(i)

		return new_a

	def __len__(self) -> int:
		return len(self.buffer)

	def __iter__(self):
		return AverageFIFOIterator(self.buffer, self.capacity, self.current_ptr)

	def seralize_to_dict(self) -> dict[str, Union[list, int, float]]:
		return {
			'buffer': self.buffer,
			'n_items': len(self.buffer),
			'capacity': self.capacity,
			'ptr': self.current_ptr,
			'sum': self.readings_sum
		} 

class AverageFIFOIterator:
	def __init__(self, buffer:list, capacity:int, ptr:int) -> None:
		self.i = ptr
		self.buffer = buffer
		self.n_remaining = capacity
		self.capacity = capacity

	def __iter__(self):
		return self

	def __increment_ptr(self) -> None:
		self.i += 1
		if self.i >= self.capacity:
			self.i = 0

	def __next__(self):
		if self.n_remaining > 0:
			r = self.buffer[self.i]
			self.__increment_ptr()
			self.n_remaining -= 1
			return r
		else:
			raise StopIteration
