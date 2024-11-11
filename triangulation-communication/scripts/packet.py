# Packet structure
# 
# Multi-byte values are stored in little-endian format
# Flags are stored in big endian
# 
# ################################################################
# #                      Identifier (31:0)                       #
# ################################################################
# #      Identifier (47:32)     ##A|R|D|   Flags (15:0)  |K|P|G|L#
# ################################################################
# #                 Reported X Coordinate (31:0)                 #
# ################################################################
# #                Reported X Coordinate (63:32)                 #
# ################################################################
# #                 Reported Y Coordinate (31:0)                 #
# ################################################################
# #                Reported Y Coordinate (63:32)                 #
# ################################################################
# #            Frame / Transaction Identifier (31:0)             #
# ################################################################
# #                Data size (Limit 4GiB) (31:0)                 #
# ################################################################
# #           Antenna power values / Other information           #
# #                                                              #
# 

from random            import randint
from typing            import Optional
# from typing_extensions import Self
from warnings          import warn

import struct

class DBM_Packet:
	# A 48-bit identifier. Could be MAC address,
	# or spoofed MAC address.
	identifier_48b:int     = 0 # 6 bytes
	# Flags to turn on or off
	#  ARD.........KPGL
	#   . -> Unused bit
	#   L -> Log-on request
	#   G -> Get Antenna Signal Strengths request
	#   P -> Ping the antenna node (Add A flag for response)
	#   K -> Kick out antenna node (Remove node)
	#        If sent by antenna node it means request to kick
	#         itself out of the system. Respond with A flag.
	#   A -> Request Accepted
	#   R -> Request Rejected
	#   D -> Use Dummy values provided
	flags_16b:int          = 0 # 2 bytes
	# Reported X coordinate of the antenna node. (Double precision floats)
	reported_x_coord:float = 0 # 8-byte
	# Reported Y coordinate of the antenna node. (Double precision floats)
	reported_y_coord:float = 0 # 8-byte
	# Identifier to coordinate the antenna nodes.
	frame_identifier:int   = 0 # 4-byte
	# The size of the data portion of the packet.
	# In Bytes
	def data_size(self) -> int: # 4-byte
		return len(self.data)

	# Data to be sent in bytes
	data:bytes

	PACKET_SIZE = 32

	# Flags bitfields
	FLAG_ACCEPT_REQ = 0x8000
	FLAG_REJECT_REQ = 0x4000
	FLAG_DUMMY_VAL  = 0x2000

	FLAG_KICK_ANT   = 0x0008
	FLAG_PING_ANT   = 0x0004
	FLAG_GET_ANT_SG = 0x0002
	FLAG_LOGON_REQ  = 0x0001

	def __init__(self, identifier:int, flags:int, x:float, y:float, frame_ref:int, data:bytes):
		self.identifier_48b   = identifier
		self.flags_16b        = flags
		self.reported_x_coord = x
		self.reported_y_coord = y
		self.frame_identifier = frame_ref
		self.data             = data

	def __bytes__(self) -> bytes:
		identifier_bytes = struct.pack("<Q", self.identifier_48b)[:-2]
		flags_bytes      = struct.pack(">H", self.flags_16b)
		x_coord_bytes    = struct.pack("<d", self.reported_x_coord)
		y_coord_bytes    = struct.pack("<d", self.reported_y_coord)
		frame_id_bytes   = struct.pack("<I", self.frame_identifier)
		data_size_bytes  = struct.pack("<I", self.data_size())

		assert len(identifier_bytes) == 6
		assert len(flags_bytes)      == 2
		assert len(x_coord_bytes)    == 8
		assert len(y_coord_bytes)    == 8
		assert len(frame_id_bytes)   == 4
		assert len(data_size_bytes)  == 4

		return identifier_bytes + flags_bytes + x_coord_bytes + y_coord_bytes + frame_id_bytes + data_size_bytes + self.data

	@staticmethod
	def from_bytes(packet:bytes) -> tuple[any, int]:
		packet_len = len(packet)
		assert packet_len >= DBM_Packet.PACKET_SIZE

		identifier = struct.unpack("<Q", packet[ 0: 6] + b'\x00\x00')[0]
		flags      = struct.unpack(">H", packet[ 6: 8])[0]
		x_coord    = struct.unpack("<d", packet[ 8:16])[0]
		y_coord    = struct.unpack("<d", packet[16:24])[0]
		frame_id   = struct.unpack("<I", packet[24:28])[0]
		data_size  = struct.unpack("<I", packet[28:32])[0]

		if packet_len - DBM_Packet.PACKET_SIZE != data_size:
			warn(f"Size of actual data attached with packet of {packet_len - DBM_Packet.PACKET_SIZE} bytes does not match the expected data size of {data_size} bytes.")

		return DBM_Packet(identifier, flags, x_coord, y_coord, frame_id, packet[DBM_Packet.PACKET_SIZE:])
	
	def is_login_request(self) -> bool:
		return self.flags_16b & DBM_Packet.FLAG_LOGON_REQ != 0

	def is_login_request_accepted(self) -> bool:
		bits_to_check = (DBM_Packet.FLAG_ACCEPT_REQ | DBM_Packet.FLAG_LOGON_REQ)
		return self.flags_16b & bits_to_check == bits_to_check

	def is_dbm_data_request(self) -> bool:
		return self.flags_16b & DBM_Packet.FLAG_GET_ANT_SG != 0

	def is_dbm_data_packet(self) -> bool:
		bits_to_check = (DBM_Packet.FLAG_ACCEPT_REQ | DBM_Packet.FLAG_GET_ANT_SG)
		return self.flags_16b & bits_to_check == bits_to_check

	@staticmethod
	def _create_login_request_fx(identifier:int, x:float, y:float):
		return DBM_Packet(identifier, DBM_Packet.FLAG_LOGON_REQ, x, y, 0, b'')

	@staticmethod
	def create_login_request(identifier:Optional[int], x:float, *y:float):
		y1 = 0
		if y:
			y1 = y[0]
		else:
			x, y1 = identifier, x
			identifier = randint(1, (2**48) - 1);

		return DBM_Packet._create_login_request_fx(identifier, x, y1)

	@staticmethod
	def accept_login_request(identifier:int, x:float, y:float):
		return DBM_Packet(identifier, DBM_Packet.FLAG_ACCEPT_REQ | DBM_Packet.FLAG_LOGON_REQ, x, y, 0, b'')

	@staticmethod
	def accept_login_request_and_get_reading(identifier:int, x:float, y:float, frame_id:int):
		return DBM_Packet(identifier, DBM_Packet.FLAG_ACCEPT_REQ | DBM_Packet.FLAG_GET_ANT_SG | DBM_Packet.FLAG_LOGON_REQ, x, y, frame_id, b'')

	@staticmethod
	def reject_login_request(identifier:int, x:float, y:float):
		return DBM_Packet(identifier, DBM_Packet.FLAG_REJECT_REQ | DBM_Packet.FLAG_LOGON_REQ, x, y, 0, b'')

	@staticmethod
	def create_reading_request(identifier:int, x:float, y:float, frame_id:int):
		return DBM_Packet(identifier, DBM_Packet.FLAG_GET_ANT_SG, x, y, frame_id, b'')

	# Use double-precision floats
	@staticmethod
	def create_power_dbm_data_packet(identifier:int, x:float, y:float, frame_id:int, dbm_reading:float):
		return DBM_Packet(identifier, DBM_Packet.FLAG_GET_ANT_SG, x, y, frame_id, struct.pack("<d", dbm_reading))
