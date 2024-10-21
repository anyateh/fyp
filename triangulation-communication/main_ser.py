#!/usr/bin/env python3

import asyncio

from socket import AF_INET, SOCK_STREAM, socket

from .logger import logger

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
	sock.setblocking(False)
	sock.settimeout(0.5)
	sock.listen(1)

async def close_tcp_listen(sock:socket) -> None:
	sock.close()

async def receive_client_connection(sock:socket, clients:list[TrianClient]) -> None:
	logger.debug("Checking for potential new clients...")
	try:
		connection, (client_ip, client_port) = sock.accept()
		logger.info(f"New Client {client_ip}:{client_port}!")
		connection.setblocking(False)
		connection.settimeout(0.5)
		clients.append(TrianClient(client_ip, client_port, connection))
	except TimeoutError:
		asyncio.create_task(receive_client_connection(sock, clients))

async def handle_client_connection(client:TrianClient) -> None:
	conn = client.connection
	try:
		data = conn.recv(1024)

		if data:
			logger.debug(f"Received message from {client.hostname_ip}:{client.port}.")
			conn.sendall("Received your message: {}".format(data))
			logger.debug(f"Sent message to {client.hostname_ip}:{client.port}.")
	except TimeoutError:
		asyncio.sleep(0.1)
