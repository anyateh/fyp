import asyncio
import struct

from random import randint
from sys    import stderr
from typing import Optional, TextIO, TYPE_CHECKING

from ..packet import DBM_Packet
if TYPE_CHECKING:
	from .server              import TrianServer
else:
	TrianServer   = 'TrianServer'
from .trilateration.trilaterate import estimate_location, inv_friis
from ..tui.ellipse        import OutlineEllipse
from ..tui.antenna_screen import AntennaScreen

from .dummy.export_antes import export_antes

__current_request_id  = 0
__keep_alive = True

ring_colours = [
	(66, 129, 164),
	(72, 169, 166),
	(169, 153, 137),
	(212, 180, 131),
	(193, 102, 107)
]

class AntennaNode:
	id:int     = 0
	x:float    = 0.0
	y:float    = 0.0

	gain:float = 1.0

	dbm:Optional[float] = None

	signal_fingerprint:Optional[list[float]] = None

	ring:OutlineEllipse

	def __init__(self, id:int, x:float, y:float):
		self.id = id
		self.x  = x
		self.y  = y

		global ring_colours

		r, g, b = ring_colours[self.id % len(ring_colours)]
		self.ring = OutlineEllipse(int(x), int(y), 0, 0, r, g, b)

	def inverse_friis(self) -> float:
		if self.dbm == None:
			return 0.0
		return inv_friis(self.dbm, self.gain)

__antennas_registered:dict[int, AntennaNode] = {}

antenna_screen = AntennaScreen()
show_screen    = True

lowest_x_coord  = 0.0
highest_x_coord = 0.0
lowest_y_coord  = 0.0
highest_y_coord = 0.0

buffered_output:Optional[TextIO] = None

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
		new_antenna = AntennaNode(a_id, x, y)
		__antennas_registered[a_id] = new_antenna
		antenna_screen.add_antenna(new_antenna)

		export_antes(__antennas_registered)

	return True

def deregister_ante_node(a_id:int) -> None:
	if a_id in __antennas_registered:
		antenna_screen.remove_antenna(__antennas_registered[a_id])
		del __antennas_registered[a_id]

		export_antes(__antennas_registered)

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

	global buffered_output
	buffered_output = open(stderr.fileno(), 'w')

	while __keep_alive:
		frame_id = randint(1, 255)
		__current_request_id = frame_id
		await update_ante_readings(frame_id, server)
		print_antennas()
		await asyncio.sleep(0.5)

	buffered_output.close()
	buffered_output = None

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
	if show_screen:
		if antenna_screen.dimensions_disparity_detected():
			antenna_screen.on_resize()
		antenna_screen.update_antennas()

		antenna_screen.paint()
		if buffered_output != None:
			antenna_screen.render(buffered_output)

			for i in __antennas_registered.values():
				buffered_output.write("\x1b[{};{}H{}".format(antenna_screen.map_y_to_screen(i.y) + 1, antenna_screen.map_x_to_screen(i.x) + 1, i.id))

			if can_perform_localization():
				pointx, pointy = localize_transmitter_pos()
				buffered_output.write("\x1b[{};{}HX".format(antenna_screen.map_y_to_screen(pointy) + 1, antenna_screen.map_x_to_screen(pointx) + 1))

			buffered_output.flush()
		return

	if buffered_output:
		buffered_output.write("\x1b[2J\x1b[H")
		buffered_output.write("\x1b[30;46m Antennas Begin \x1b[0m\n\n")

		for i in __antennas_registered.values():
			dbm_str = f'\x1b[1;32m{i.dbm}\x1b[0m' if i.dbm != None else "\x1b[1;31mno value\x1b[0m"
			buffered_output.write(f"Ante {i.id}: x = {i.x}, y = {i.y}, dbm = {dbm_str}.\n")

		buffered_output.write("\n\x1b[30;46m Antennas End \x1b[0m\n")
		buffered_output.write("\x1b[38:5:147m" + "\u2584" * 21 + "\x1b[0m\n")
		buffered_output.write("\x1b[1;30;48:5:147m EE4002D FYP Project \x1b[0m\n")
		buffered_output.write("\x1b[38:5:147m" + "\u2580" * 21 + "\x1b[0m\n")
		buffered_output.write("\x1b[38:5:147mYou may not see all antennas above because scrolling have not been implemented.\n")

		if can_perform_localization():
			buffered_output.write("The estimated location is below:\n\n")

			device_x, device_y = (f"\x1b[1;30;48:5:111m {i} \x1b[0m" if i != None else "\x1b[1;30;48:5:161m invalid \x1b[0m" for i in localize_transmitter_pos())

			# stderr.flush()
			buffered_output.write(f"\x1b[38:5:147mX = {device_x}\n")
			buffered_output.write(f"\x1b[38:5:147mY = {device_y}\n")
		else:
			buffered_output.write("Need at least three antennas connected before estimation can be shown.\n\n")

		buffered_output.write("\n\x1b[38:5:147mPress <ctrl-c> to quit this server, and shut down all antennas.\x1b[0m\n")

		buffered_output.flush()

	export_antes(__antennas_registered)
