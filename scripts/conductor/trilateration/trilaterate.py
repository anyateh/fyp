from typing_extensions import TYPE_CHECKING
if TYPE_CHECKING:
	from ..manage_antes import AntennaNode
else:
	AntennaNode = 'AntennaNode'

import numpy as np

from math   import isnan, isinf
from typing import Callable, Optional

FREQUENCY  = 500e6
SOL        = 299_792_458
WAVELENGTH = SOL / FREQUENCY

# Tentative constants
TRANSMITTER_POWER_DBM = 1.0
TRANSMITTER_GAIN_DBM  = 0.0 # No transmitter dish focusing the signal

# Calibration Settings
object_power_calibration_dbm   = -30.0
object_p0_distance_calibration = 1.0
object_signal_frequency        = 742.12417e6

path_loss = 2

def is_dbm_valid_for_trilat(dbm:float) -> bool:
	return dbm is not None and not isnan(dbm) and not isinf(dbm)

def calculate_distance(p_recv_dbm:Optional[float]) -> Optional[float]:
	if p_recv_dbm is None:
		return None

	pwr_dbm_diff = p_recv_dbm - object_power_calibration_dbm

	return object_p0_distance_calibration        \
		* (10                                    \
	 		 ** (                                \
				pwr_dbm_diff / (-10 * path_loss) \
			)                                    \
		)

# Deprecated: Use calculate_distance instead
def inv_friis(power_received_dbm:float, antenna_gain_dbm:float = 0.0) -> float:
	return object_p0_distance_calibration * (10 ** ((power_received_dbm - object_power_calibration_dbm) / (-10 * path_loss)))
	# return WAVELENGTH / (4 * np.pi * 10**((power_received_dbm - TRANSMITTER_POWER_DBM - TRANSMITTER_GAIN_DBM - antenna_gain_dbm) / 20))

# Currently assuming single device to track.
def estimate_location(antennas:dict[int, AntennaNode]) -> tuple[Optional[float], Optional[float]]:
	antennas_clone = antennas.copy()

	# Pick the first antenna in the dict.
	try:
		ref_ant_id, ref_ant = next(iter(antennas_clone.items()))
		while not is_dbm_valid_for_trilat(ref_ant.dbm()):
			ref_ant_id, ref_ant = next(iter(antennas_clone.items()))

		remaining_antennas = {k:v for k, v in antennas_clone.items() if is_dbm_valid_for_trilat(v.dbm())}
		if ref_ant_id in remaining_antennas:
			del remaining_antennas[ref_ant_id]

		assert len(remaining_antennas) >= 1

		x0_x_2, y0_x_2 = ref_ant.x * 2, ref_ant.y * 2
		# d0_sq, x0_sq, y0_sq = inv_friis(ref_ant.dbm, ref_ant.gain) ** 2, ref_ant.x ** 2, ref_ant.y ** 2
		d0_sq, x0_sq, y0_sq = ref_ant.radius() ** 2, ref_ant.x ** 2, ref_ant.y ** 2

		matrix_rhs:Callable[[AntennaNode], float] = \
			lambda i: d0_sq - i.radius() ** 2 - x0_sq + i.x ** 2 - y0_sq + i.y ** 2

		if len(remaining_antennas) == 1:
			second_antenna = next(iter(remaining_antennas.values()))

			tri_mat_rhs = matrix_rhs(second_antenna)
			y1_m_y0 = second_antenna.y - ref_ant.y
			x1_m_x0 = second_antenna.x - ref_ant.x

			assert y1_m_y0 != 0 or x1_m_x0 != 0

			if y1_m_y0 == 0:
				x_estimate = tri_mat_rhs / (2 * x1_m_x0)
				return x_estimate, ref_ant.y

			if x1_m_x0 == 0:
				y_estimate = tri_mat_rhs / (2 * y1_m_y0)
				return ref_ant.x, y_estimate

			lingrad_between_ants = y1_m_y0 / x1_m_x0

			x_estimate = (tri_mat_rhs/(2 * y1_m_y0)              \
				 + ref_ant.x*lingrad_between_ants - ref_ant.y)   \
				   / (lingrad_between_ants + 1/lingrad_between_ants)

			return x_estimate, ((x_estimate - ref_ant.x) * lingrad_between_ants + ref_ant.y)

		left_side_matrix_rows  = np.array([
			[i.x * 2 - x0_x_2, i.y * 2 - y0_x_2]
			for i in remaining_antennas.values()
		])
		right_side_matrix_rows = np.array([
			matrix_rhs(i) for i in remaining_antennas.values()
		])

		return tuple(np.linalg.lstsq(left_side_matrix_rows, right_side_matrix_rows, rcond = None)[0])

	except StopIteration:
		return None, None
	except ZeroDivisionError:
		return None, None

def calibrate_transmitter_power(pdbm:float) -> None:
	global object_power_calibration_dbm
	object_power_calibration_dbm = pdbm

def calibrate_reference_distance(d:float) -> None:
	global object_p0_distance_calibration
	object_p0_distance_calibration = d

def calibrate_transmitter_frequency(f:float) -> None:
	global object_signal_frequency
	object_signal_frequency = f

def calibrate_space_path_loss(n:float) -> None:
	global path_loss
	path_loss = n

def seralize_calibration_json_dict() -> dict[str, float]:
	return {
		"p0dbm": object_power_calibration_dbm,
		"d0": object_p0_distance_calibration,
		"signal_frequency": object_signal_frequency,
		"path_loss": path_loss
	}