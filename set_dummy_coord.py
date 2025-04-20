#!/usr/bin/env python3
import json
import numpy as np
import struct

from os  import path
from sys import argv, stderr
from typing import Any

from scripts.conductor.trilateration.trilaterate import TRANSMITTER_GAIN_DBM, TRANSMITTER_POWER_DBM, WAVELENGTH
from scripts.logger import logger

DUMMY_DBM_FOLDER = '__dummy_dbm_data__'

def print_usage(arg0:str) -> None:
	print(f'usage: {arg0} x y', file = stderr)
	print(f'Sets the dummy readings for the antennas.', file = stderr)

def friis(d:Any, gain:float) -> float:
	return TRANSMITTER_POWER_DBM + TRANSMITTER_GAIN_DBM     \
		+ gain + 20 * np.log10(WAVELENGTH / (4 * np.pi * d))

def set_dummy_coord(x:float, y:float, raise_errors = False) -> int:
	dummy_ante_list = path.join(DUMMY_DBM_FOLDER, 'antes.json')

	if not raise_errors and \
		(not path.isdir(DUMMY_DBM_FOLDER) or not path.exists(dummy_ante_list)):
		logger.error(f"The file {dummy_ante_list} does not exist.")
		return 1

	with open(dummy_ante_list, 'r', encoding = 'utf-8') as f:
		data = json.load(f)

	if not raise_errors and 'antennas' not in data:
		logger.error(f"Antenna list not found in {dummy_ante_list}.")
		return 1

	for i in data['antennas']:
		given_source_loc = np.array([[x, y]])
		anchor  = np.array([[i['x'], i['y']]])
		dist    = np.linalg.norm(anchor - given_source_loc, axis = 1)

		val     = friis(dist[0], i['gain'])

		ante_id = i['id']

		with open(path.join(DUMMY_DBM_FOLDER, f'ante_{ante_id}.txt'), 'wb') as f:
			f.write(struct.pack('<f', val))

	return 0

def main() -> None:
	if len(argv) < 3:
		print_usage(argv[0])
		return

	exit(set_dummy_coord(float(argv[1]), float(argv[2])))

if __name__ == '__main__':
	main()
