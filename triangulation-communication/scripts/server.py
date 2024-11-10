import asyncio

from socket import AF_INET, SOCK_STREAM, socket
from typing import Callable, Optional

from .logger import logger
from .packet import DBM_Packet

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
	hostname_ip:str              = "0.0.0.0"
	port:int                     = 0
	sock:socket
	tasks:set[asyncio.coroutine] = set()
	accepting_clients:bool       = False

	def __init__(self, hostname_ip:str = "0.0.0.0", port:int = 0):
		self.hostname_ip = hostname_ip
		self.port = port
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.setblocking(False)
		self.sock.settimeout(0.5)

	def start(self):
		self.sock.bind((self.hostname_ip, self.port))
		self.sock.listen(1)
		return self

	def close(self):
		self.sock.close()
		return self

	async def _listen_for_new_clients(self) -> Optional[TrianClient]:
		logger.debug("Checking for potential new clients...")
		try:
			connection, (client_ip, client_port) = self.sock.accept()
			logger.info(f"New Client {client_ip}:{client_port}!")
			connection.setblocking(False)
			connection.settimeout(0.5)

			return TrianClient(client_ip, client_port, connection)
		except TimeoutError:
			return None
	
	async def _search_client_loop(self) -> None:
		awaiting_client_task = None
		while self.accepting_clients:
			if awaiting_client_task and awaiting_client_task.done():
				new_client = awaiting_client_task.result()
				if new_client:
					pass
					# new_client_receiver = asyncio.create_task(receive_client_content(new_client))
					# new_client_receiver.add_done_callback(lambda tsk: receive_client_content_done(new_client, tsk.result(), tsk, client_tasks))
					# self.tasks.add(new_client_receiver)
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

	async def _receive_client_content(client:TrianClient) -> Optional[bytes]:
		conn = client.connection
		try:
			data = conn.recv(1024)

			if data:
				logger.debug(f"Received message from {client.hostname_ip}:{client.port}.")
				return data

			return None
		except TimeoutError:
			return None
