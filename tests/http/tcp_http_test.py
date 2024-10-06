#!/usr/bin/env python3

import logging
import re

from   signal import SIGINT, signal
from   socket import AF_INET, SOCK_STREAM, socket
from   time   import sleep
from   typing import Iterator, Iterable, Optional

_logger = logging.getLogger(__name__)
_logger_console_handler = logging.StreamHandler()

_logger.addHandler(_logger_console_handler)
_logger_console_handler.setFormatter(logging.Formatter(
	"[%(levelname)s] %(message)s"
))
_logger.setLevel(logging.DEBUG)

main_page_response = '''HTTP/1.1 200 OK\r
Content-Type: text/html\r
Content-Length: 200\r\n\r
<!DOCTYPE html>
<html lang="en">
	<head>
		<title>Hello World!</title>
	</head>
	<body>
		<h1>Hello World!</h1>
		<p>Oh hi there!</p>
		<p>This is an example of a first HTML page.</p>
	</body>
</html>'''

def start_server() -> socket:
	listening_ip = "192.168.1.73"
	port         = 2310

	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind((listening_ip, port))
	sock.listen(1)

	return sock

def listen_for_a_http_req(sock:socket) -> None:
	client_connect, (client_ip, client_port) = sock.accept()

	_logger.info(f'Oh! Hi there! {client_ip}:{client_port}')

	request_bytes = []

	# header_end_detected = lambda packet: packet.decode(encoding = "utf-8").find("\r\n\r\n") != -1
	header_end_detected = lambda : request_bytes[-4:] == [13, 10, 13, 10]

	_logger.debug(f"Attempting to read from {client_ip}:{client_port}...")
	data = client_connect.recv(1024)
	request_bytes.extend(list(data))
	while not header_end_detected():
		_logger.debug(f"Attempting to read from {client_ip}:{client_port}...")
		data = client_connect.recv(1024)
		if not data:
			break
		request_bytes.extend(list(data))
	
	client_req = "".join(bytes(request_bytes).decode(encoding = "utf-8"))

	_logger.debug("Received request:")
	for line in client_req.split('\n'):
		_logger.debug(f"{line}")
	
	client_connect.sendall(main_page_response.encode(encoding = 'utf-8'))

	client_connect.close()

def close_server(sock:socket) -> None:
	sock.close()

def main() -> None:
	while True:
		try:
			sock = start_server()

			def handle_ctrl_c(sig, frame) -> None:
				close_server(sock)
				exit(0)

			signal(SIGINT, handle_ctrl_c)

			while True:
				listen_for_a_http_req(sock)
			break
		except OSError as e:
			_logger.error(f"{e}")
			sleep(1)

if __name__ == '__main__':
	main()
