from ctypes import byref, c_ulong
import logging
from msvcrt import getch, kbhit
from sys import stderr, stdin
from typing import Optional

if __name__ == '__main__':
	from windows_console_settings import ENABLE_ECHO_INPUT, ENABLE_LINE_INPUT, GetConsoleMode, GetStdHandle, SetConsoleMode, STD_INPUT_HANDLE, wintypes
else:
	from .windows_console_settings import ENABLE_ECHO_INPUT, ENABLE_LINE_INPUT, GetConsoleMode, GetStdHandle, SetConsoleMode, STD_INPUT_HANDLE, wintypes

stdin_handle = GetStdHandle(STD_INPUT_HANDLE)

__attr_before_enable = None

def enable_tui_mode() -> None:
	global __attr_before_enable
	__attr_before_enable = wintypes.DWORD(0)

	retval = GetConsoleMode(stdin_handle, byref(__attr_before_enable))
	logging.debug(f"GetConsoleMode return value -> {retval}")

	SetConsoleMode(stdin_handle, c_ulong(__attr_before_enable.value & ~(ENABLE_ECHO_INPUT | ENABLE_LINE_INPUT)))

def disable_tui_mode() -> None:
	global __attr_before_enable
	if not __attr_before_enable:
		logging.debug("disable_tui_mode: TUI mode not enabled.")
		return
	
	SetConsoleMode(stdin_handle, __attr_before_enable)
	__attr_before_enable = None

def read_character_press() -> str:
	return getch().decode(encoding = "raw_unicode_escape")

def data_remaining_in_stdin() -> bool:
	return kbhit()

def is_arrow_up_key(key:str, previous_key:Optional[str]) -> bool:
	return (previous_key == chr(0) or previous_key == chr(224)) and key == 'H'

def is_arrow_left_key(key:str, previous_key:Optional[str]) -> bool:
	return (previous_key == chr(0) or previous_key == chr(224)) and key == 'K'

def is_arrow_right_key(key:str, previous_key:Optional[str]) -> bool:
	return (previous_key == chr(0) or previous_key == chr(224)) and key == 'M'

def is_arrow_down_key(key:str, previous_key:Optional[str]) -> bool:
	return (previous_key == chr(0) or previous_key == chr(224)) and key == 'P'

def is_home_key(key:str, previous_key:Optional[str]) -> bool:
	return (previous_key == chr(0) or previous_key == chr(224)) and key == 'G'

def is_end_key(key:str, previous_key:Optional[str]) -> bool:
	return (previous_key == chr(0) or previous_key == chr(224)) and key == 'O'

def is_pgup_key(key:str, previous_key:Optional[str]) -> bool:
	return (previous_key == chr(0) or previous_key == chr(224)) and key == 'I'

def is_pgdn_key(key:str, previous_key:Optional[str]) -> bool:
	return (previous_key == chr(0) or previous_key == chr(224)) and key == 'Q'

def is_ctrl_b(key:str) -> bool:
	return key == chr(2)

def is_ctrl_f(key:str) -> bool:
	return key == chr(6)

def is_ctrl_d(key:str) -> bool:
	return key == chr(4)

def is_ctrl_u(key:str) -> bool:
	return key == chr(21)

# -- Below is code to test the functions -- 

if __name__ == '__main__':
	logging.basicConfig(level = logging.DEBUG, format = '[%(levelname)s] %(message)s')
	logging.getLogger("httpx").setLevel(logging.WARNING)
	logging.getLogger("httpcore").setLevel(logging.WARNING)
	logging.getLogger("requests").setLevel(logging.WARNING)
	logging.getLogger("urllib3").setLevel(logging.WARNING)
	logging.getLogger("chardet").setLevel(logging.WARNING)
	logging.getLogger("asyncio").setLevel(logging.WARNING)

	logging.info("Non-canonical demo")
	print()
	logging.debug("Enabling TUI mode")
	logging.debug("Each keypress should be registered one-by-one.")
	logging.info("Press 'q' to exit.")
	print()

	enable_tui_mode()
	keypressed = ''
	while keypressed != 'q':
		keypressed = read_character_press()
		print("You've entered ->", keypressed, f"(ASCII code -> {ord(keypressed)})", f"[Is stdin atty? {stdin.isatty()}]", file = stderr)

	print()
	logging.info("You've pressed 'q', now exiting.")
	logging.debug("Disabling TUI mode")
	logging.debug("The command line should return to the default behaviour.")
	print()
	disable_tui_mode()
