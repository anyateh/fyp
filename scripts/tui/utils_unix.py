#!/usr/bin/env python3

import logging
from select import select
from sys import stdin, stderr
from termios import ECHO, ICANON, tcgetattr, TCSAFLUSH, TCSANOW, tcsetattr, VMIN, VTIME

__c_iflag = 0
__c_oflag = 1
__c_cflag = 2
__c_lflag = 3
__c_ispeed = 4
__c_ospeed = 5
__c_cc = 6

stdin_fd = stdin.fileno()

__attr_before_enable = None

def enable_tui_mode() -> None:
	global __attr_before_enable
	__attr_before_enable = tcgetattr(stdin_fd)

	new = tcgetattr(stdin_fd)
	new[__c_lflag] &= ~ICANON & ~ECHO
	new[__c_cc][VMIN] = 1
	new[__c_cc][VTIME] = 10

	tcsetattr(stdin_fd, TCSAFLUSH, new)

def disable_tui_mode() -> None:
	global __attr_before_enable
	if not __attr_before_enable:
		logging.debug("disable_tui_mode: TUI mode not enabled.")
		return
	
	tcsetattr(stdin_fd, TCSANOW, __attr_before_enable)
	__attr_before_enable = None

def read_character_press() -> str:
	return stdin.read(1)

# Yeah.. code from https://stackoverflow.com/questions/2408560/non-blocking-console-input
# didn't work..
def data_remaining_in_stdin() -> bool:
	return select([stdin], [], [], 0) == ([stdin], [], [])

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
		print("You've entered ->", keypressed, f"(ASCII code -> {ord(keypressed)})", f"[Data remaining -> {select([stdin], [], [], 0)}]", file = stderr)

	print()
	logging.info("You've pressed 'q', now exiting.")
	logging.debug("Disabling TUI mode")
	logging.debug("The command line should return to the default behaviour.")
	print()
	disable_tui_mode()
