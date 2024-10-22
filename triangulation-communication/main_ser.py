#!/usr/bin/env python3

import asyncio

from signal import signal, SIGINT
from socket import AF_INET, SOCK_STREAM, socket
from typing import Optional

from logger import logger

DEFAULT_LISTEN_IP   = '0.0.0.0'
DEFAULT_LISTEN_PORT = 3112

class TrianClient:
	hostname_ip:str
	port:int
	connection:socket

	def __init__(self, hostname_ip:str, port:int, connection:socket) -> None:
		self.hostname_ip = hostname_ip
		self.port        = port
		self.connection  = connection

async def establish_tcp_listen(hostname_ip:str = DEFAULT_LISTEN_IP, port:int = DEFAULT_LISTEN_PORT) -> socket:
	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind((hostname_ip, port))
	await asyncio.sleep(0)
	sock.setblocking(False)
	sock.settimeout(0.5)
	sock.listen(1)
	return sock

async def close_tcp_listen(sock:socket) -> None:
	sock.close()

async def accept_client_connection(sock:socket) -> Optional[TrianClient]:
	logger.debug("Checking for potential new clients...")
	try:
		connection, (client_ip, client_port) = sock.accept()
		logger.info(f"New Client {client_ip}:{client_port}!")
		connection.setblocking(False)
		connection.settimeout(0.5)

		return TrianClient(client_ip, client_port, connection)
	except TimeoutError:
		return None

async def receive_client_content(client:TrianClient) -> Optional[bytes]:
	conn = client.connection
	try:
		data = conn.recv(1024)

		if data:
			logger.debug(f"Received message from {client.hostname_ip}:{client.port}.")
			return data

		return None
	except TimeoutError:
		return None

def receive_client_content_done(client:TrianClient, content:Optional[bytes], task_itself:asyncio.Task, client_tasks:set[asyncio.Task]) -> None:
	client_tasks.discard(task_itself)
	if content:
		new_client_handler = asyncio.create_task(handle_client_content(client, content))
		new_client_handler.add_done_callback(client_tasks.discard)
		client_tasks.add(new_client_handler)

async def handle_client_content(client:TrianClient, content:bytes) -> None:
	conn = client.connection
	conn.sendall("Received your message: {}".format(content).encode(encoding = 'utf-8'))
	logger.debug(f"Sent message to {client.hostname_ip}:{client.port}.")
	conn.close()

async def main_loop() -> None:
	awaiting_client_task = None
	client_tasks = set()

	sock = None

	while True:
		try:
			sock = await establish_tcp_listen()
			break
		except OSError as e:
			logger.info(f"{e}")
			logger.info("Waiting for port to be available again...")
			await asyncio.sleep(1)
	
	if not sock:
		return

	def handle_ctrl_c(sig, frame) -> None:
		sock.close()
		exit(0)

	signal(SIGINT, handle_ctrl_c)

	while True:
		if awaiting_client_task and awaiting_client_task.done():
			new_client = awaiting_client_task.result()
			if new_client:
				new_client_receiver = asyncio.create_task(receive_client_content(new_client))
				new_client_receiver.add_done_callback(lambda tsk: receive_client_content_done(new_client, tsk.result(), tsk, client_tasks))
				client_tasks.add(new_client_receiver)
			awaiting_client_task = None
		elif not awaiting_client_task:
			awaiting_client_task = asyncio.create_task(accept_client_connection(sock))
		await asyncio.sleep(0)

if __name__ == '__main__':
	asyncio.run(main_loop())
