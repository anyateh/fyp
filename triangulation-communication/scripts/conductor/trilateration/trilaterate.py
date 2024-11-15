from typing_extensions import TYPE_CHECKING
if TYPE_CHECKING:
	from ..manage_antes import AntennaNode
else:
	AntennaNode = 'AntennaNode'

# Currently assuming single device to track.
def estimate_location(antennas:dict[int, AntennaNode]) -> tuple[float, float]:
	pass
