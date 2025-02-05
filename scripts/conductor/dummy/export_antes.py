from os import mkdir, path

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from ..manage_antes import AntennaNode
else:
	AntennaNode = 'AntennaNode'
from ..output.dump_antes import dump_antes

DUMMY_DBM_FOLDER = '__dummy_dbm_data__'

def export_antes(antennas:dict[int, AntennaNode]) -> None:
	if not path.exists(DUMMY_DBM_FOLDER):
		mkdir(DUMMY_DBM_FOLDER)

	dummy_ante_list = path.join(DUMMY_DBM_FOLDER, 'antes.json')

	with open(dummy_ante_list, 'w', encoding = 'utf-8') as f:
		dump_antes(antennas, f)
