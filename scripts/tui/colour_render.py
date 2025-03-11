class UniColourRender:
	r:int = 0
	g:int = 0
	b:int = 0

	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b

	@staticmethod
	def ansi_216_cols_from_rgb(r:int, g:int, b:int) -> int:
		return 16 + 36 * (r // 5) + 6 * (g // 5) + (b // 5)

	def ansi_set_fg_colour_256(self) -> str:
		return f'\x1b[38:5:{UniColourRender.ansi_216_cols_from_rgb(self.r, self.g, self.b)}m'

	def ansi_set_fg_colour_24bit(self) -> str:
		return f'\x1b[38:2::{self.r}:{self.g}:{self.b}m'

	def ansi_set_bg_colour_256(self) -> str:
		return f'\x1b[48:5:{UniColourRender.ansi_216_cols_from_rgb(self.r, self.g, self.b)}m'

	def ansi_set_bg_colour_24bit(self) -> str:
		return f'\x1b[48:2::{self.r}:{self.g}:{self.b}m'

	def ansi_colour_reset(self) -> str:
		return '\x1b[0m'
