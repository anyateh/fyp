#!/usr/bin/env python3
from sys import argv, stderr

from scripts.conductor.dummy.set_dummy_coord import set_dummy_coord

DUMMY_DBM_FOLDER = '__dummy_dbm_data__'

def print_usage(arg0:str) -> None:
	print(f'usage: {arg0} x y', file = stderr)
	print(f'Sets the dummy readings for the antennas.', file = stderr)

def main() -> None:
	if len(argv) < 3:
		print_usage(argv[0])
		return

	exit(set_dummy_coord(float(argv[1]), float(argv[2])))

if __name__ == '__main__':
	main()
