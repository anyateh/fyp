import asyncio

from socket import AF_INET, SOCK_STREAM, socket, timeout as socket_timeout
from typing import Optional

from ..packet import DBM_Packet

class AnteClient:
	identifier:int       = 0
	x:float              = 0.0
	y:float              = 0.0
	gain:float           = 1.0
	dest_hostname_ip:str = "0.0.0.0"
	port:int             = 0
	sock:socket

	def __init__(self, mac_identifier:int, x:float, y:float, dest_hostname_ip:str = "0.0.0.0", port:int = 0):
		self.identifier = mac_identifier
		self.x = x
		self.y = y
		self.dest_hostname_ip = dest_hostname_ip
		self.port = port
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.setblocking(True)
		# self.sock.settimeout(0.5)

	def start(self):
		self.sock.connect((self.dest_hostname_ip, self.port))
		return self

	def close(self):
		self.sock.close()
		return self

	def request_login(self) -> Optional[DBM_Packet]:
		login_request_pkt = DBM_Packet.create_login_request(self.identifier, self.x, self.y)

		self.sock.sendall(bytes(login_request_pkt))

		header = self.sock.recv(DBM_Packet.PACKET_SIZE)
		if not header:
			return None

		pkt_header:DBM_Packet = DBM_Packet.from_bytes(header)
		if pkt_header.is_login_request_accepted() or pkt_header.is_dbm_data_request():
			return pkt_header

		return None

	def request_logout(self) -> Optional[DBM_Packet]:
		self.sock.settimeout(0.5)
		logout_req_pkt = DBM_Packet.create_remove_ante_req(self.identifier)

		try:
			self.sock.sendall(bytes(logout_req_pkt))

			header = self.sock.recv(DBM_Packet.PACKET_SIZE)
			if not header:
				return None

			pkt_header:DBM_Packet = DBM_Packet.from_bytes(header)
			return pkt_header

		except socket_timeout:
			return None

	def receive_packet_request(self) -> Optional[DBM_Packet]:
		header = self.sock.recv(DBM_Packet.PACKET_SIZE)

		if not header:
			return None

		pkt_header, data_size = DBM_Packet.from_bytes_with_size(header)

		if not pkt_header:
			return None

		if data_size > 0:
			data = self.sock.recv(data_size)
			pkt_header.data = data

		return pkt_header
	
	def send_requested_data(self, frame_id:int, dbm:float) -> None:
		pkt:DBM_Packet = DBM_Packet.create_power_dbm_data_packet(self.identifier, frame_id, dbm)
		self.sock.sendall(bytes(pkt))
	
	def send_kick_out_ack(self) -> None:
		pkt = DBM_Packet.create_remove_ante_ack(self.identifier)

		self.sock.sendall(bytes(pkt))

	def send_server_close_ack(self) -> None:
		pkt = DBM_Packet.create_server_exit_ack(self.identifier)

		self.sock.sendall(bytes(pkt))
