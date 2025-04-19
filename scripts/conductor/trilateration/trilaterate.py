from typing_extensions import TYPE_CHECKING
if TYPE_CHECKING:
	from ..manage_antes import AntennaNode
else:
	AntennaNode = 'AntennaNode'

import numpy as np

from typing import Optional

FREQUENCY  = 500e6
SOL        = 299_792_458
WAVELENGTH = SOL / FREQUENCY

# Tentative constants
TRANSMITTER_POWER_DBM = 1.0
TRANSMITTER_GAIN_DBM  = 1.0 # No transmitter dish focusing the signal

def inv_friis(power_received_dbm:float, antenna_gain_dbm:float) -> float:
	return WAVELENGTH / (4 * np.pi * 10**((power_received_dbm - TRANSMITTER_POWER_DBM - TRANSMITTER_GAIN_DBM - antenna_gain_dbm) / 20))

# Currently assuming single device to track.
def estimate_location(antennas:dict[int, AntennaNode], use_avg:bool = False) -> tuple[Optional[float], Optional[float]]:
	# Pick the first antenna in the dict.
	try:
		ref_ant_id, ref_ant = next(iter(antennas.items()))

		remaining_antennas = {k:v for k, v in antennas.items() if v.dbm is not None}
		del remaining_antennas[ref_ant_id]

		# assert len(remaining_antennas) >= 2

		get_inv_frii_fx = lambda ant: ant.inv_friis_avg.avg() if use_avg else ant.inverse_friis()

		x0_x_2, y0_x_2 = ref_ant.x * 2, ref_ant.y * 2
		# d0_sq, x0_sq, y0_sq = inv_friis(ref_ant.dbm, ref_ant.gain) ** 2, ref_ant.x ** 2, ref_ant.y ** 2
		d0_sq, x0_sq, y0_sq = get_inv_frii_fx(ref_ant) ** 2, ref_ant.x ** 2, ref_ant.y ** 2

<<<<<<< HEAD
		matrix_rhs = lambda i: d0_sq - inv_friis(i.dbm, i.gain) ** 2 - x0_sq + i.x ** 2 - y0_sq + i.y ** 2

		if len(remaining_antennas) == 1:
			second_antenna = next(iter(remaining_antennas.values()))
			tri_mat_rhs = matrix_rhs(second_antenna)
			y1_m_y0 = second_antenna.y - ref_ant.y
			x1_m_x0 = second_antenna.x - ref_ant.x

			lingrad_between_ants = y1_m_y0 / x1_m_x0

			x_estimate = (tri_mat_rhs/(2 * y1_m_y0) + ref_ant.x*lingrad_between_ants - ref_ant.y) / (lingrad_between_ants + 1/lingrad_between_ants)

			return x_estimate, ((x_estimate - ref_ant.x) * lingrad_between_ants + ref_ant.y)

		left_side_matrix_rows  = np.array([
			[i.x * 2 - x0_x_2, i.y * 2 - y0_x_2]
			for i in remaining_antennas.values()
		])
		right_side_matrix_rows = np.array([matrix_rhs(i) for i in remaining_antennas.values()])
=======
		left_side_matrix_rows  = np.array([[i.x * 2 - x0_x_2, i.y * 2 - y0_x_2] for i in remaining_antennas.values()])
		right_side_matrix_rows = np.array([d0_sq - get_inv_frii_fx(i) ** 2 - x0_sq + i.x ** 2 - y0_sq + i.y ** 2 for i in remaining_antennas.values()])
>>>>>>> main

		return tuple(np.linalg.lstsq(left_side_matrix_rows, right_side_matrix_rows, rcond = None)[0])

	except StopIteration:
		return None, None

