import asyncio
import struct

from random import randint
from typing import Optional, TYPE_CHECKING

from ..packet import DBM_Packet
if TYPE_CHECKING:
	from ..server import TrianServer
else:
	TrianServer = 'TrianServer'

__current_request_id  = 0
__keep_alive = True

class AntennaNode:
	id:int  = 0
	x:float = 0.0
	y:float = 0.0

	dbm:Optional[float] = None

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
	if register_ante_node(packet.identifier_48b, packet.reported_x_coord, packet.reported_y_coord):
		response_packet:DBM_Packet = DBM_Packet.accept_login_request(packet.identifier_48b, packet.reported_x_coord, packet.reported_y_coord)
	else:
		response_packet:DBM_Packet = DBM_Packet.reject_login_request(packet.identifier_48b, packet.reported_x_coord, packet.reported_y_coord)

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
		request_pkt = DBM_Packet.create_reading_request(i.id, i.x, i.y, frame_id)

		obtain_data_tasks.append(server.send_packet_to_client(i.id, request_pkt, True))

		i.dbm = None
	
	results = await asyncio.gather(*obtain_data_tasks)

	if __current_request_id == frame_id:
		for i in results:
			if i:
				manage_data_packet(i)

async def loop_ante_updates(server:TrianServer) -> None:
	global __keep_alive
	__keep_alive = True
	global __current_request_id
	frame_id = randint(1, (2**32) - 1)
	while __keep_alive:
		frame_id = randint(1, (2**32) - 1)
		__current_request_id = frame_id
		await update_ante_readings(frame_id, server)
		print_antennas()
		await asyncio.sleep(0.5)

async def stop_ante_updates() -> None:
	global __keep_alive
	__keep_alive = False

def manage_data_packet(packet:DBM_Packet) -> None:
	dbm = struct.unpack("<d", packet.data)[0]

	if packet.identifier_48b in __antennas_registered:
		__antennas_registered[packet.identifier_48b].dbm = dbm

		__antennas_registered[packet.identifier_48b].x = packet.reported_x_coord
		__antennas_registered[packet.identifier_48b].y = packet.reported_y_coord

def print_antennas() -> None:
	print("---------")
	print("Antennas:")
	print("---------")
	for i in __antennas_registered.values():
		print(f"Ante {i.id}: x = {i.x}, y = {i.y}, dbm = {i.dbm}.")
