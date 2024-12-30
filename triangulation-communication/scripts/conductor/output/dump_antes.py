import json

from datetime import datetime
from typing   import TextIO

from ..manage_antes import AntennaNode

from ..trilateration.trilaterate import TRANSMITTER_GAIN_DBM, TRANSMITTER_POWER_DBM

def __json_encode_antenna_node(ante:AntennaNode) -> dict:
	return {
		'id'  : ante.id,
		'x'   : ante.x,
		'y'   : ante.y,
		'gain': ante.gain,
		'dbm' : ante.dbm
	}

def dump_antes(antennas:dict[int, AntennaNode], filedes:TextIO) -> None:
	ts = int(datetime.now().timestamp())
	json_obj = {
		'ts'                : ts,
		'n_antennas'        : len(antennas),
		'transmission_power': TRANSMITTER_POWER_DBM,
		'transmission_gain' : TRANSMITTER_GAIN_DBM,
		'antennas'          : [__json_encode_antenna_node(i) for i in antennas.values()]
	}

	json.dump(json_obj, filedes, indent = '\t')
