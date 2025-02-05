from random import uniform

import numpy as np
# from numpy.typing import ArrayLike as NPArrayLike
import struct

from os     import path
from typing import Any

from .client import AnteClient

DUMMY_POINT_X = 25
DUMMY_POINT_Y = 12

DUMMY_DBM_FOLDER = '__dummy_dbm_data__'

from ..conductor.trilateration.trilaterate import TRANSMITTER_POWER_DBM, TRANSMITTER_GAIN_DBM, WAVELENGTH

def friis(d:Any, gain:float) -> float:
	return TRANSMITTER_POWER_DBM + TRANSMITTER_GAIN_DBM + gain + 20 * np.log10(WAVELENGTH / (4 * np.pi * d))

def get_rss(true_position:Any, antenna:AnteClient) -> tuple[Any, Any]:
	anchor    = np.array([[antenna.x, antenna.y]])
	distances = np.linalg.norm(anchor - true_position, axis = 1)

	received_dbm = np.array([friis(d, antenna.gain) for d in distances])

	return received_dbm, distances

async def measure_dbm(antenna:AnteClient) -> float:
	file_to_read = path.join(DUMMY_DBM_FOLDER, f'ante_{antenna.identifier}.txt')
	if path.isfile(file_to_read):
		with open(file_to_read, 'rb') as f:
			val = f.read()

		return struct.unpack('<f', val)[0]

	received_dbm = get_rss(np.array([[DUMMY_POINT_X, DUMMY_POINT_Y]]), antenna)[0]
	return received_dbm
