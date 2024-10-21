#!/usr/bin/env python3

import asyncio
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
Content-Length: 200\r
Connection: close\r\n\r
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
	listening_ip = "0.0.0.0"
	port         = 2310

	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind((listening_ip, port))
	sock.listen(1)

	return sock

def create_http_response(code:int, code_msg:str, content_type:str, content:bytes, headers:Optional[dict[str,str]] = None) -> bytes:
	res_headers  = f"HTTP/1.1 {code} {code_msg}\r\n"
	res_headers += f"Content-Type: {content_type}\r\n"
	res_headers += f"Content-Length: {len(content)}\r\n"
	if headers:
		for h, v in headers.items():
			res_headers += f"{h}: {v}\r\n"
	res_headers += "\r\n"

	return res_headers.encode(encoding = "utf-8") + content

def _find_seq_index(bytes_list:list[int], seq:list[int]) -> int:
	seq_len = len(seq)
	seq_pos = 0
	for potential_patt in (bytes_list[i:i + seq_len] for i in range(len(bytes_list) - seq_len + 1)):
		if potential_patt == seq:
			return seq_pos
		seq_pos += 1
	
	return -1

# Returns -1 if headers are incomplete
def _get_headers_len(received_info:list[int]) -> int:
	seq = [13, 10, 13, 10]
	seq_pos = 0
	for potential_patt in (received_info[i:i + 4] for i in range(len(received_info) - 3)):
		if potential_patt == seq:
			return seq_pos
		seq_pos += 1
	
	return -1

def _get_content_len(http_req_res:list[int]) -> Optional[int]:
	len_line = None
	content_len_header = list(b'Content-Length:')

	def split_int_iter_by_int(int_seq:Iterable[int], n:int) -> Iterator[list[int]]:
		spl = []
		for i in int_seq:
			spl.append(i)
			if i == n:
				yield spl
				spl = []

	def int_list_begins_with(ilist:list[int], patt:list[int]) -> bool:
		if len(patt) > len(ilist):
			return False
		
		return ilist[:len(patt)] == patt

	for line in split_int_iter_by_int(http_req_res, 10):
		if int_list_begins_with(line, content_len_header):
			len_line = line
			break

	if not len_line:
		return None

	l = int("".join(chr(i) for i in len_line if 48 <= i < 58))

	return l

def is_http_in_header(http_req:list[int]) -> bool:
	first_crlf = _find_seq_index(http_req, [13, 10])
	if first_crlf < 4:
		return False
	
	for segment in (http_req[i:i + 4] for i in range(len(http_req[:first_crlf]) - 3)):
		if segment == list(b'HTTP'):
			return True

	return False

def _is_complete_http_req(received_info:list[int]) -> bool:
	if not is_http_in_header(received_info):
		return False
	
	headers_len = _get_headers_len(received_info)
	if headers_len == -1:
		return False

	content_len = _get_content_len(received_info)
	if not content_len:
		content_len = 0

	return len(received_info) == content_len + headers_len + 4

def listen_for_a_http_req(sock:socket) -> None:
	client_connect, (client_ip, client_port) = sock.accept()

	_logger.info(f'Oh! Hi there! {client_ip}:{client_port}')

	request_bytes = []

	# header_end_detected = lambda packet: packet.decode(encoding = "utf-8").find("\r\n\r\n") != -1
	# header_end_detected = lambda : request_bytes[-4:] == [13, 10, 13, 10]

	client_connect.setblocking(False)

	_logger.debug(f"Attempting to read from {client_ip}:{client_port}...")
	data = client_connect.recv(1024)
	request_bytes.extend(list(data))
	while not _is_complete_http_req(request_bytes):
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

# Async version below

async def start_http_server(listening_ip:str = '0.0.0.0', port = 2310) -> socket:
	sock = socket(AF_INET, SOCK_STREAM)

	sock.bind((listening_ip, port))
	sock.setblocking(False)
	sock.settimeout(0.5)
	sock.listen(1)

	return sock

async def handle_client(connection:socket, client_ip:str, client_port:int, content:bytes) -> None:
	client_req = "".join(content.decode(encoding = "utf-8"))
	await asyncio.sleep(0)

	_logger.debug("Received request:")
	for line in client_req.split('\n'):
		_logger.debug(f"{line}")
	
	_logger.debug(f"from {client_ip}:{client_port}")
	
	connection.sendall(main_page_response.encode(encoding = 'utf-8'))

	await asyncio.sleep(0)

	connection.close()

async def accept_new_client(sock:socket) -> tuple[Optional[socket], Optional[str], Optional[int], Optional[bytes]]:
	try:
		connection, (client_ip, client_port) = sock.accept()

		_logger.info(f'Oh! Hi there! {client_ip}:{client_port}')

		request_bytes = []

		connection.setblocking(False)
		connection.settimeout(0.5)

		_logger.debug(f"Attempting to read from {client_ip}:{client_port}...")

		try:
			data = connection.recv(1024)
		except TimeoutError:
			await asyncio.sleep(0)

		request_bytes.extend(list(data))

		while not _is_complete_http_req(request_bytes):
			_logger.debug(f"Attempting to read from {client_ip}:{client_port}...")

			try:
				data = connection.recv(1024)
			except TimeoutError:
				connection.close()
				return None, None, None, None

			if not data:
				await asyncio.sleep(0)
				break

			request_bytes.extend(list(data))
			await asyncio.sleep(0)
	
		return connection, client_ip, client_port, bytes(request_bytes)
	except TimeoutError:
		return None, None, None, None

async def main_loop() -> None:
	sock = await start_http_server()

	clients = []

	new_client_task = None
	client_handlers = set()

	def handle_ctrl_c(sig, frame) -> None:
		close_server(sock)
		exit(0)

	signal(SIGINT, handle_ctrl_c)

	def client_handler_done(handler_task:asyncio.Task) -> None:
		client_handlers.discard(handler_task)

	def client_task_done(task:asyncio.Task[tuple[socket, str, int]]) -> None:
		nonlocal new_client_task
		new_client_task = None
		connection, clientip, clientport, content = task.result()
		if connection:
			handler_task = asyncio.create_task(handle_client(connection, clientip, clientport, content))
			handler_task.add_done_callback(client_handler_done)
			client_handlers.add(handler_task)

	while True:
		if not new_client_task:
			new_client_task = asyncio.create_task(accept_new_client(sock))
			new_client_task.add_done_callback(client_task_done)
		await asyncio.sleep(0)

if __name__ == '__main__':
	# main()
	asyncio.run(main_loop())
