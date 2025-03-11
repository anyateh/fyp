import logging
from os import get_terminal_size, name as os_name
from sys import stderr
from typing import Optional

if os_name == 'nt':
	from . import utils_win
else:
	from . import utils_unix

def get_screen_size() -> tuple[int, int]:
	tsize = get_terminal_size()
	return (tsize.columns, tsize.lines)

def set_cursor_pos(x:int, y:int) -> None:
	print(f'\x1b[{y};{x}H', file = stderr)

def clear_screen() -> None:
	print('\x1b[2J', file = stderr)
	print('\x1b[H', file = stderr, end = '')
	# c, r = get_screen_size()
	# print(' ' * (c * (r - 1)), file = stderr, end = '')

def enable_alt_screen() -> None:
	print('\x1b[?1049h', file = stderr)

def disable_alt_screen() -> None:
	print('\x1b[?1049l', file = stderr)

def enable_tui_mode(alt_screen:bool = True) -> None:
	if alt_screen:
		enable_alt_screen()
	if os_name == 'nt':
		utils_win.enable_tui_mode()
	else:
		utils_unix.enable_tui_mode()

def disable_tui_mode(alt_screen:bool = True) -> None:
	if alt_screen:
		disable_alt_screen()
	if os_name == 'nt':
		utils_win.disable_tui_mode()
	else:
		utils_unix.disable_tui_mode()

def read_character_press() -> str:
	if os_name == 'nt':
		return utils_win.read_character_press()
	
	return utils_unix.read_character_press()

def pause() -> None:
	enable_tui_mode(False)
	print("Press any key to continue...", file = stderr, end = '')
	stderr.flush()
	read_character_press()
	print()
	disable_tui_mode(False)

def is_arrow_up_key(key:str, previous_key:Optional[str], second_previous_key:Optional[str]) -> bool:
	if os_name == 'nt':
		return utils_win.is_arrow_up_key(key, previous_key)
	
	return False

def is_arrow_left_key(key:str, previous_key:Optional[str], second_previous_key:Optional[str]) -> bool:
	if os_name == 'nt':
		return utils_win.is_arrow_left_key(key, previous_key)
	
	return False

def is_arrow_right_key(key:str, previous_key:Optional[str], second_previous_key:Optional[str]) -> bool:
	if os_name == 'nt':
		return utils_win.is_arrow_right_key(key, previous_key)
	
	return False

def is_arrow_down_key(key:str, previous_key:Optional[str], second_previous_key:Optional[str]) -> bool:
	if os_name == 'nt':
		return utils_win.is_arrow_down_key(key, previous_key)
	
	return False

def is_home_key(key:str, previous_key:Optional[str], second_previous_key:Optional[str]) -> bool:
	if os_name == 'nt':
		return utils_win.is_home_key(key, previous_key)

	return False

def is_end_key(key:str, previous_key:Optional[str], second_previous_key:Optional[str]) -> bool:
	if os_name == 'nt':
		return utils_win.is_end_key(key, previous_key)

	return False

def is_pgup_key(key:str, previous_key:Optional[str], second_previous_key:Optional[str]) -> bool:
	if os_name == 'nt':
		return utils_win.is_pgup_key(key, previous_key)

	return False

def is_pgdn_key(key:str, previous_key:Optional[str], second_previous_key:Optional[str]) -> bool:
	if os_name == 'nt':
		return utils_win.is_pgdn_key(key, previous_key)

	return False

def is_ctrl_b(key:str) -> bool:
	if os_name == 'nt':
		return utils_win.is_ctrl_b(key)

	return False

def is_ctrl_f(key:str) -> bool:
	if os_name == 'nt':
		return utils_win.is_ctrl_f(key)

	return False

def is_ctrl_d(key:str) -> bool:
	if os_name == 'nt':
		return utils_win.is_ctrl_d(key)

	return False

def is_ctrl_u(key:str) -> bool:
	if os_name == 'nt':
		return utils_win.is_ctrl_u(key)

	return False
