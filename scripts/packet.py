# Packet structure
# 
# Multi-byte values are stored in little-endian format
# Flags are stored in big endian
# 
# Original Proposal:
#
# ################################################################
# #                      Identifier (31:0)                       #
# ################################################################
# #      Identifier (47:32)     ##A|R|D|X| Flags (15:0)  |K|P|G|L#
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
# New Proposal: 4-byte header
#
# ################################################################
# #       Identifier (7:0)      ##A|R|D|X|  Flags (7:0)  |K|U|G|L#
# ################################################################
# #    Frame Identifier (7:0)   ##        Data size (7:0)        #
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
	identifier_8b:int     = 0 # 1 byte
	# Flags to turn on or off
	#  ARDXKUGL
	#   . -> Unused bit
	#   A -> Request Accepted
	#   R -> Request Rejected
	#   D -> Use Dummy values provided
	#   X -> Part of server exit
	#   L -> Log-on request
	#   G -> Get Antenna Signal Strengths request
	#   U -> Request to update information
	#   K -> Kick out antenna node (Remove node)
	#        If sent by antenna node it means request to kick
	#         itself out of the system. Respond with A flag.
	flags_8b:int           = 0 # 1 byte
	# Reported X coordinate of the antenna node. (Double precision floats)
	# reported_x_coord:float = 0 # 8-byte
	# Reported Y coordinate of the antenna node. (Double precision floats)
	# reported_y_coord:float = 0 # 8-byte
	# Identifier to coordinate the antenna nodes.
	# frame_identifier:int   = 0 # 4-byte
	# The size of the data portion of the packet.
	# In Bytes
	def data_size(self) -> int: # 4-byte
		return len(self.data)

	# Data to be sent in bytes
	data:bytes

	PACKET_SIZE = 3

	# Flags bitfields
	FLAG_ACCEPT_REQ = 0x80
	FLAG_REJECT_REQ = 0x40
	FLAG_DUMMY_VAL  = 0x20
	FLAG_SVR_EXIT   = 0x10
	FLAG_KICK_ANT   = 0x08
	FLAG_UPDATE_ANT = 0x04
	FLAG_GET_ANT_SG = 0x02
	FLAG_LOGON_REQ  = 0x01

	def __init__(self, identifier:int, flags:int, data:bytes):
		self.identifier_8b    = identifier & 0xff
		self.flags_8b         = flags
		# self.reported_x_coord = x
		# self.reported_y_coord = y
		# self.frame_identifier = frame_ref
		self.data             = data

	def __bytes__(self) -> bytes:
		identifier_bytes = struct.pack("<B", self.identifier_8b)
		flags_bytes      = struct.pack(">B", self.flags_8b)
		# x_coord_bytes    = struct.pack("<d", self.reported_x_coord)
		# y_coord_bytes    = struct.pack("<d", self.reported_y_coord)
		# frame_id_bytes   = struct.pack("<B", self.frame_identifier)
		data_size_bytes  = struct.pack("<B", self.data_size())

		assert len(identifier_bytes) == 1
		assert len(flags_bytes)      == 1
		# assert len(x_coord_bytes)    == 8
		# assert len(y_coord_bytes)    == 8
		# assert len(frame_id_bytes)   == 1
		assert len(data_size_bytes)  == 1

		return identifier_bytes + flags_bytes + data_size_bytes + self.data

	@staticmethod
	def from_bytes(packet:bytes):
		packet_len = len(packet)
		assert packet_len >= DBM_Packet.PACKET_SIZE

		identifier = struct.unpack("<B", packet[0:1])[0]
		flags      = struct.unpack(">B", packet[1:2])[0]
		# frame_id   = struct.unpack("<B", packet[2])[0]

		# identifier = struct.unpack("<Q", packet[ 0: 6] + b'\x00\x00')[0]
		# flags      = struct.unpack(">H", packet[ 6: 8])[0]
		# x_coord    = struct.unpack("<d", packet[ 8:16])[0]
		# y_coord    = struct.unpack("<d", packet[16:24])[0]
		# frame_id   = struct.unpack("<I", packet[24:28])[0]
		# data_size  = struct.unpack("<I", packet[28:32])[0]

		# if packet_len - DBM_Packet.PACKET_SIZE != data_size:
		# 	warn(f"Size of actual data attached with packet of {packet_len - DBM_Packet.PACKET_SIZE} bytes does not match the expected data size of {data_size} bytes.")

		return DBM_Packet(identifier, flags, packet[DBM_Packet.PACKET_SIZE:])

	@staticmethod
	def from_bytes_with_size(packet:bytes) -> tuple[any, int]:
		packet_len = len(packet)
		assert packet_len >= DBM_Packet.PACKET_SIZE

		data_size = struct.unpack("<B", packet[2:3])[0]

		return DBM_Packet.from_bytes(packet), data_size

	def is_login_request(self) -> bool:
		return self.flags_8b & DBM_Packet.FLAG_LOGON_REQ != 0

	def is_login_request_accepted(self) -> bool:
		bits_to_check = (DBM_Packet.FLAG_ACCEPT_REQ | DBM_Packet.FLAG_LOGON_REQ)
		return self.flags_8b & bits_to_check == bits_to_check

	QUERY_TYPE_COORD = 1
	QUERY_TYPE_DBM   = 2

	def is_query_packet(self) -> bool:
		return self.flags_8b & DBM_Packet.FLAG_GET_ANT_SG != 0

	def is_dbm_data_request(self) -> bool:
		if self.flags_8b & DBM_Packet.FLAG_GET_ANT_SG == 0:
			return False

		return self.data and self.data[0] == DBM_Packet.QUERY_TYPE_DBM

	def is_dbm_data_packet(self) -> bool:
		bits_to_check = (DBM_Packet.FLAG_ACCEPT_REQ | DBM_Packet.FLAG_GET_ANT_SG)
		return self.flags_8b & bits_to_check == bits_to_check

	def get_frame_id(self) -> Optional[int]:
		if not self.is_dbm_data_request():
			return None

		return struct.unpack('<B', self.data[1:2])[0]

	# Returns dbm, frame_id
	def get_dbm_data(self) -> tuple[Optional[float], Optional[int]]:
		if not self.is_dbm_data_packet():
			return None, None

		return struct.unpack('<f', self.data[2:6])[0], struct.unpack('<B', self.data[1:2])[0]
	
	def is_kick_request(self) -> bool:
		return self.flags_8b & DBM_Packet.FLAG_KICK_ANT != 0

	def is_server_closing_noti(self) -> bool:
		bits_to_check = (DBM_Packet.FLAG_SVR_EXIT | DBM_Packet.FLAG_KICK_ANT)
		return self.flags_8b & bits_to_check == bits_to_check

	def is_server_closing_ack(self) -> bool:
		bits_to_check = (DBM_Packet.FLAG_ACCEPT_REQ | DBM_Packet.FLAG_SVR_EXIT | DBM_Packet.FLAG_KICK_ANT)
		return self.flags_8b & bits_to_check == bits_to_check
	
	def is_coord_update_request(self) -> bool:
		return self.flags_8b & DBM_Packet.FLAG_UPDATE_ANT != 0;

	@staticmethod
	def _create_login_request_fx(identifier:int, x:float, y:float):
		return DBM_Packet(identifier, DBM_Packet.FLAG_LOGON_REQ, DBM_Packet.pack_coord_update(x, y))

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
	def accept_login_request(identifier:int):
		return DBM_Packet(identifier, DBM_Packet.FLAG_ACCEPT_REQ | DBM_Packet.FLAG_LOGON_REQ, b'')

	@staticmethod
	def _package_query_dbm_data(frame_id:int) -> bytes:
		return struct.pack('<B', DBM_Packet.QUERY_TYPE_DBM) + struct.pack('<B', frame_id & 0xff)

	@staticmethod
	def _package_query_dbm_data_response(frame_id:int, dbm_reading:float) -> bytes:
		return struct.pack('<B', DBM_Packet.QUERY_TYPE_DBM) + struct.pack('<B', frame_id & 0xff) + struct.pack('<f', dbm_reading)

	@staticmethod
	def accept_login_request_and_get_reading(identifier:int, frame_id:int):
		return DBM_Packet(identifier, DBM_Packet.FLAG_ACCEPT_REQ | DBM_Packet.FLAG_GET_ANT_SG | DBM_Packet.FLAG_LOGON_REQ, DBM_Packet._package_query_dbm_data(frame_id))

	@staticmethod
	def reject_login_request(identifier:int):
		return DBM_Packet(identifier, DBM_Packet.FLAG_REJECT_REQ | DBM_Packet.FLAG_LOGON_REQ, b'')

	@staticmethod
	def create_reading_request(identifier:int, frame_id:int):
		return DBM_Packet(identifier, DBM_Packet.FLAG_GET_ANT_SG, DBM_Packet._package_query_dbm_data(frame_id))

	# Use double-precision floats (not anymore)
	@staticmethod
	def create_power_dbm_data_packet(identifier:int, frame_id:int, dbm_reading:float):
		return DBM_Packet(identifier, DBM_Packet.FLAG_ACCEPT_REQ | DBM_Packet.FLAG_GET_ANT_SG, DBM_Packet._package_query_dbm_data_response(frame_id, dbm_reading))

	@staticmethod
	def create_remove_ante_req(identifier:int):
		return DBM_Packet(identifier, DBM_Packet.FLAG_KICK_ANT, b'')

	@staticmethod
	def create_remove_ante_ack(identifier:int):
		return DBM_Packet(identifier, DBM_Packet.FLAG_ACCEPT_REQ | DBM_Packet.FLAG_KICK_ANT, b'')

	@staticmethod
	def create_server_exit_noti(identifier:int):
		return DBM_Packet(identifier, DBM_Packet.FLAG_SVR_EXIT | DBM_Packet.FLAG_KICK_ANT, b'')

	@staticmethod
	def create_server_exit_ack(identifier:int):
		return DBM_Packet(identifier, DBM_Packet.FLAG_ACCEPT_REQ | DBM_Packet.FLAG_SVR_EXIT | DBM_Packet.FLAG_KICK_ANT, b'')

	# @staticmethod
	# def create_server_exit_ack(identifier:int):
	# 	return DBM_Packet(identifier, DBM_Packet.FLAG_SVR_EXIT | DBM_Packet.FLAG_KICK_ANT, 0, b'')

	UPDATE_TYPE_PING  = 0
	UPDATE_TYPE_COORD = 1

	@staticmethod
	def pack_coord_update(x:float, y:float) -> bytes:
		return struct.pack('<B', 1) + struct.pack('<f', x) + struct.pack('<f', y)

	@staticmethod
	def unpack_coord_update(pkt:bytes) -> tuple[Optional[float], Optional[float]]:
		if pkt[0:1] != b'\x01':
			return None, None

		return struct.unpack('<f', pkt[1:5])[0], struct.unpack('<f', pkt[5:9])[0]

	@staticmethod
	def create_coord_update(identifier:int, x:float, y:float):
		coord_upd = DBM_Packet.pack_coord_update(x, y)
		return DBM_Packet(identifier, DBM_Packet.FLAG_UPDATE_ANT, 0, coord_upd)
