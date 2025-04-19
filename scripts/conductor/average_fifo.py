
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

	def __len__(self) -> int:
		return len(self.buffer)
