import asyncio

from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket, timeout as socket_timeout
# from time import time
from typing import Callable, Optional

from ..logger import logger
from ..packet import DBM_Packet

from .manage_antes import decode_packet, deregister_ante_node, get_ante_node_coords

class TrianClient:
	hostname_ip:str
	port:int
	connection:socket
	tasks:set = set()

	def __init__(self, hostname_ip:str, port:int, connection:socket) -> None:
		self.hostname_ip = hostname_ip
		self.port        = port
		self.connection  = connection

class TrianServer:
	hostname_ip:str         = "0.0.0.0"
	port:int                = 0
	sock:socket
	tasks:set[asyncio.Task] = set()
	accepting_clients:bool  = False

	clients:dict[int, TrianClient] = {}

	def __init__(self, hostname_ip:str = "0.0.0.0", port:int = 0):
		self.hostname_ip = hostname_ip
		self.port = port
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.sock.setblocking(False)
		self.sock.settimeout(0.001)

	def start(self):
		self.sock.bind((self.hostname_ip, self.port))
		self.sock.listen(1)
		return self

	async def close(self):
		logger.info("Closing Server")
		self.stop_accepting_clients()
		clients = list(self.clients)
		client_close_awaitables = []
		for client_id in clients:
			client_close_awaitables.append(self.close_client(client_id, True, False))

		await asyncio.gather(*client_close_awaitables)

		self.sock.close()
		return self

	async def _listen_for_new_clients(self) -> Optional[TrianClient]:
		if not self.accepting_clients:
			return None
		logger.debug("Checking for potential new clients...")
		try:
			connection, (client_ip, client_port) = self.sock.accept()
			logger.info(f"New Client {client_ip}:{client_port}!")
			connection.setblocking(False)
			connection.settimeout(0.5)

			return TrianClient(client_ip, client_port, connection)
		except socket_timeout:
			return None
	
	def __decode_packet_callback(self, tsk:asyncio.Task) -> None:
		self.tasks.discard(tsk)
		response = tsk.result()
		if response:
			reply_packet, expecting_response = response
			send_pkt = asyncio.create_task(self.send_packet_to_client(reply_packet.identifier_8b, reply_packet, expecting_response))
			send_pkt.add_done_callback(self.__decode_packet_callback)
			self.tasks.add(send_pkt)

	def __client_receiver_done(self, tsk:asyncio.Task) -> None:
		self.tasks.discard(tsk)
		packet = tsk.result()
		if packet:
			decode_packet_task = asyncio.create_task(decode_packet(packet))
			decode_packet_task.add_done_callback(self.__decode_packet_callback)
			self.tasks.add(decode_packet_task)
	
	async def _search_client_loop(self) -> None:
		awaiting_client_task = None
		while self.accepting_clients:
			if awaiting_client_task and awaiting_client_task.done():
				new_client = awaiting_client_task.result()
				if new_client:
					new_client_receiver = asyncio.create_task(self._receive_client_content(new_client))
					new_client_receiver.add_done_callback(self.__client_receiver_done)
					self.tasks.add(new_client_receiver)
				awaiting_client_task = None
			elif not awaiting_client_task:
				awaiting_client_task = asyncio.create_task(self._listen_for_new_clients())
			await asyncio.sleep(0)

	async def start_accepting_clients(self):
		self.accepting_clients = True
		search_client_loop = asyncio.create_task(self._search_client_loop())
		search_client_loop.add_done_callback(self.tasks.discard)
		self.tasks.add(search_client_loop)
		return self
	
	def stop_accepting_clients(self):
		self.accepting_clients = False
		return self

	async def _receive_client_content(self, client:TrianClient) -> Optional[DBM_Packet]:
		conn = client.connection
		try:
			header = conn.recv(DBM_Packet.PACKET_SIZE)

			if not header:
				logger.info(f"Couldn't get header from {client.hostname_ip}:{client.port}")
				return None

			header_packet, reported_data_size = DBM_Packet.from_bytes_with_size(header)

			if header_packet.identifier_8b in self.clients:
				if header_packet.is_login_request():
					await self.close_client(header_packet.identifier_8b, False, False)
					self.clients[header_packet.identifier_8b] = client
			else:
				self.clients[header_packet.identifier_8b] = client

			if reported_data_size > 0:
				data = conn.recv(reported_data_size)

				logger.debug(f"Received message from {client.hostname_ip}:{client.port}.")

				if data:
					header_packet.data = data
					return header_packet

			return header_packet
		except socket_timeout:
			return None

	async def close_client(self, client_id:int, part_of_svr_exit:bool, as_ack:bool) -> None:
		client = self.clients[client_id]

		# x, y = get_ante_node_coords(client_id)
		deregister_ante_node(client_id)

		svr_close_pkt = DBM_Packet.create_server_exit_noti(client_id) \
				if part_of_svr_exit else \
				(DBM_Packet.create_remove_ante_ack(client_id) \
	 				if as_ack else \
					DBM_Packet.create_remove_ante_req(client_id))

		logger.debug(f"Sending kick packet to antenna {client_id}")
		ack_pkt = await self.send_packet_to_client(client_id, svr_close_pkt, as_ack)
		if not as_ack:
			if ack_pkt and ack_pkt.is_kick_request():
				logger.debug(f"Received logoff acknowledgement from {client_id}")
			else:
				logger.debug(f"No acknowledgement from {client_id}")

		del self.clients[client_id]
		client.connection.close()
	
	async def send_packet_to_client(self, client_id:int, packet:DBM_Packet, expecting_response:bool) -> Optional[DBM_Packet]:
		client = self.clients[client_id]

		conn   = client.connection
		try:
			conn.sendall(bytes(packet))

			if expecting_response:
				await asyncio.sleep(0)
				# t0 = time()
				return await self._receive_client_content(client)
				# while True:
				# 	logger.debug(f'Waiting for data from {client_id}')
				# 	node_data = await self._receive_client_content(client)
				# 	if not node_data:
				# 		if time() - t0 > 60:
				# 			return None
				# 		await asyncio.sleep(0)
				# 		continue

				# 	return node_data

			return None
		except socket_timeout:
			return None
		except BrokenPipeError:
			del self.clients[client_id]
			deregister_ante_node(client_id)
