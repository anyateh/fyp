import asyncio
import struct

from random import randint
from sys    import stderr
from typing import Optional, TYPE_CHECKING

from ..packet import DBM_Packet
if TYPE_CHECKING:
	from .server import TrianServer
else:
	TrianServer = 'TrianServer'
from .trilateration.trilaterate import estimate_location

__current_request_id  = 0
__keep_alive = True

class AntennaNode:
	id:int     = 0
	x:float    = 0.0
	y:float    = 0.0

	gain:float = 1.0

	dbm:Optional[float] = None

	signal_fingerprint:Optional[list[float]] = None

	def __init__(self, id:int, x:float, y:float):
		self.id = id
		self.x  = x
		self.y  = y

__antennas_registered:dict[int, AntennaNode] = {}

# Return reply_packet, expecting_response
async def decode_packet(packet:DBM_Packet) -> tuple[Optional[DBM_Packet], bool]:
	if packet.is_login_request():
		return manage_login_request(packet), False
	
	if packet.is_dbm_data_packet():
		pass

def manage_login_request(packet:DBM_Packet) -> DBM_Packet:
	coord_update = packet.data
	if not coord_update:
		# In future, send a coord query
		response_packet:DBM_Packet = DBM_Packet.reject_login_request(packet.identifier_8b)
		return response_packet

	x, y = DBM_Packet.unpack_coord_update(coord_update)
	if x is None or y is None:
		# In future, send a coord query
		response_packet:DBM_Packet = DBM_Packet.reject_login_request(packet.identifier_8b)
		return response_packet

	if register_ante_node(packet.identifier_8b, x, y):
		response_packet:DBM_Packet = DBM_Packet.accept_login_request(packet.identifier_8b)
	else:
		response_packet:DBM_Packet = DBM_Packet.reject_login_request(packet.identifier_8b)

	return response_packet

def register_ante_node(a_id:int, x:float, y:float) -> bool:
	if a_id not in __antennas_registered:
		__antennas_registered[a_id] = AntennaNode(a_id, x, y)

	return True

def deregister_ante_node(a_id:int) -> None:
	if a_id in __antennas_registered:
		del __antennas_registered[a_id]

def get_ante_node_coords(a_id:int) -> tuple[float, float]:
	return __antennas_registered[a_id].x, __antennas_registered[a_id].y

async def update_ante_readings(frame_id:int, server:TrianServer) -> None:
	obtain_data_tasks = []
	for i in __antennas_registered.values():
		# Send request data packets to all antes
		request_pkt = DBM_Packet.create_reading_request(i.id, frame_id)

		obtain_data_tasks.append(server.send_packet_to_client(i.id, request_pkt, True))

		i.dbm = None
	
	results = await asyncio.gather(*obtain_data_tasks)

	if __current_request_id == frame_id:
		for i in results:
			if i:
				manage_data_packet(i, __current_request_id)

async def loop_ante_updates(server:TrianServer) -> None:
	global __keep_alive
	__keep_alive = True
	global __current_request_id
	frame_id = randint(1, (2**32) - 1)
	while __keep_alive:
		frame_id = randint(1, 255)
		__current_request_id = frame_id
		await update_ante_readings(frame_id, server)
		print_antennas()
		await asyncio.sleep(0.5)

async def stop_ante_updates() -> None:
	global __keep_alive
	__keep_alive = False

def manage_data_packet(packet:DBM_Packet, frame_id:int) -> None:
	# dbm = struct.unpack("<d", packet.data)[0]
	dbm, received_frame_id = packet.get_dbm_data()

	if received_frame_id == frame_id and packet.identifier_8b in __antennas_registered:
		__antennas_registered[packet.identifier_8b].dbm = dbm

		# __antennas_registered[packet.identifier_8b].x = packet.reported_x_coord
		# __antennas_registered[packet.identifier_8b].y = packet.reported_y_coord
	
	if can_perform_localization():
		localize_transmitter_pos()

def can_perform_localization() -> bool:
	count = 0
	for ante in __antennas_registered.values():
		if ante.dbm is not None:
			count += 1
		if count >= 3:
			return True

	return False

def localize_transmitter_pos() -> tuple[Optional[float], Optional[float]]:
	# Perform trilateration using data from registered clients
	return estimate_location(__antennas_registered)

def print_antennas() -> None:
	print("\x1b[2J\x1b[H", end = '', file = stderr)
	print("---------", file = stderr)
	print("Antennas:", file = stderr)
	print("---------", file = stderr)
	for i in __antennas_registered.values():
		print(f"Ante {i.id}: x = {i.x}, y = {i.y}, dbm = {i.dbm}.", file = stderr)

	if can_perform_localization():
		print("", file = stderr)

		device_x, device_y = localize_transmitter_pos()

		print("Estimated Location: ", end = '', file = stderr)
		stderr.flush()
		print(device_x, device_y)
