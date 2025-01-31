from random import uniform

import numpy as np
# from numpy.typing import ArrayLike as NPArrayLike
from typing import Any

from .client import AnteClient

DUMMY_POINT_X = 25
DUMMY_POINT_Y = 12

from ..conductor.trilateration.trilaterate import TRANSMITTER_POWER_DBM, TRANSMITTER_GAIN_DBM, WAVELENGTH

def friis(d:Any, gain:float) -> float:
	return TRANSMITTER_POWER_DBM + TRANSMITTER_GAIN_DBM + gain + 20 * np.log10(WAVELENGTH / (4 * np.pi * d))

def get_rss(true_position:Any, antenna:AnteClient) -> tuple[Any, Any]:
	anchor    = np.array([[antenna.x, antenna.y]])
	distances = np.linalg.norm(anchor - true_position, axis = 1)

	received_dbm = np.array([friis(d, antenna.gain) for d in distances])

	return received_dbm, distances

async def measure_dbm(antenna:AnteClient) -> float:
	received_dbm = get_rss(np.array([[DUMMY_POINT_X, DUMMY_POINT_Y]]), antenna)[0]
	return received_dbm
