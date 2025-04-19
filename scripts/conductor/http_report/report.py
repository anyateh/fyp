from base64 import b64encode
from hashlib import sha1
from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, timeout
from sys import stderr
from threading import Thread
from typing import Callable, Iterable, Optional

from .database import get_data_entry
from ..manage_antes import gen_json_update
from .websocket_util import create_response_text_frame, extract_text_frame, get_optcode, is_valid_client_frame, TEXT as OPTTEXT

response_header_template = \
'''HTTP/1.1 %d %s\r
Content-Type: text/html\r
Content-Length: 200\r
Connection: close\r\n\r'''

main_page_response = '''HTTP/1.1 404 Not Found\r
Content-Type: text/html\r
Content-Length: 201\r
Connection: close\r\n\r
<!DOCTYPE html>
<html lang="en">
	<head>
		<title>404</title>
	</head>
	<body>
		<h1>Hello World!</h1>
		<p>Oh hi there!</p>
		<p>This is an example of a first HTML page.</p>
	</body>
</html>'''

not_found_tmp = \
'''<!DOCTYPE html>
<html lang="en">
	<head>
		<title>404</title>
	</head>
	<body>
		<h1>Not Found</h1>
	</body>
</html>
'''

__status_text = {
	101: (101, "Switching Protocols"),
	200: (200, "OK"),
	404: (404, "Not Found"),
	501: (501, "Not Implemented")
}

pages_cache = {}

def start_server() -> socket:
	listening_ip = "0.0.0.0"
	port         = 32311

	sock = socket(AF_INET, SOCK_STREAM)
	sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	sock.bind((listening_ip, port))
	sock.listen(1)

	return sock

# https://www.rfc-editor.org/rfc/rfc6455#section-1.3
__ws_append_bytes = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

# https://stackoverflow.com/questions/35977916/generate-sec-websocket-accept-from-sec-websocket-key
def accept_websocket_key(websocket_key_b64:bytes) -> bytes:
	h = sha1(websocket_key_b64 + __ws_append_bytes)
	return b64encode(h.digest())

def is_websocket_req(headers:dict[str, str]) -> bool:
	if "Origin" not in headers:
		return False

	if "Connection" not in headers:
		return False
		
	if "Upgrade" not in headers:
		return False
	
	if "Sec-WebSocket-Key" not in headers:
		return False
	
	if "Sec-WebSocket-Version" not in headers:
		return False
	
	if headers["Connection"] != 'Upgrade':
		return False

	if headers["Upgrade"] != 'websocket':
		return False

	return True

__websocket_approve_template = \
b'''HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accept: %s\r\n\r
'''
def approve_websocket_req(client:socket, websocket_key:bytes) -> None:
	client.sendall(__websocket_approve_template % accept_websocket_key(websocket_key))

def websocket_handler(websocket:socket, headers:dict[str, str], is_server_alive_fx:Callable[[], bool]) -> None:
	approve_websocket_req(websocket, headers["Sec-WebSocket-Key"].encode(encoding = 'utf-8'))
	websocket.settimeout(0.1)
	while is_server_alive_fx():
		try:
			received_bytes = websocket.recv(1024)

			if not received_bytes:
				break

			if not is_valid_client_frame(received_bytes):
				break

			if get_optcode(received_bytes) != OPTTEXT:
				continue

			t = extract_text_frame(received_bytes)

			response = create_response_text_frame(f"Received: {t}")
			websocket.sendall(response)
		except timeout:
			response = create_response_text_frame(gen_json_update())
			websocket.sendall(response)

def is_byte_seq_in_bytes(seq:bytes, s:bytes) -> bool:
	for i in range(len(s) - len(seq) + 1):
		if seq == s[i:i + len(seq)]:
			return True

	return False

__HTTP_RECV_FRAGMENT_SIZE = 1024
def receive_http_content(connection:socket) -> bytes:
	http_fragments = []

	fragment = connection.recv(__HTTP_RECV_FRAGMENT_SIZE)
	http_fragments.append(fragment)

	original_timeout = connection.gettimeout()

	connection.settimeout(0.01)

	while len(fragment) == __HTTP_RECV_FRAGMENT_SIZE:
		try:
			fragment = connection.recv(__HTTP_RECV_FRAGMENT_SIZE)
			http_fragments.append(fragment)
		except timeout:
			break

	connection.settimeout(original_timeout)

	return b''.join(http_fragments)

# def find_first_crlf(byte_seq:bytes) -> int:
# 	prev_b = None
# 	for i, byte in enumerate(byte_seq):
# 		if prev_b and prev_b == ord('\r') and byte == ord('\n'):
# 			return i - 1
# 		prev_b = byte

# 	return len(byte_seq)

def extract_http_first_line(byte_seq:bytes) -> str:
	return byte_seq.split(b'\r\n', 1)[0].decode(encoding = "utf-8")

# Returns request_type, request_path, headers
def extract_http_info(http_packet:bytes) -> tuple[str, str, dict[str, str]]:
	first_l = extract_http_first_line(http_packet)

	first_l, headers = http_packet.split(b'\r\n\r\n', 1)[0].split(b'\r\n', 1)

	first_l = first_l.decode(encoding = 'utf-8')

	if not first_l.endswith("HTTP/1.1"):
		return "", "", []

	headers = (
		i.decode(encoding = 'utf-8').split(': ', 1)
			for i in headers.split(b'\r\n')
	)

	headers = {k: v for k, v in headers}

	return tuple(first_l.rsplit(' ', 1)[0].split(' ', 1)) + (headers,)

def get_basic_headers(content_type:str, content_len:int) -> list[tuple[str, str]]:
	return [
		("Content-Type", f"{content_type}"
   			 + ("; charset=UTF-8" if content_type.startswith("text/") else "")),
		("Content-Length", f"{content_len}")
	]

def gen_http_response_header(status:tuple[int, str], content_type:str, content_len:int, additional_headers:Iterable[tuple[str, str]] = None) -> bytes:
	s_code, s_name = status
	lines = [
		f"HTTP/1.1 {s_code} {s_name}".encode(encoding = 'utf-8')
	]

	headers = get_basic_headers(content_type, content_len)

	if additional_headers:
		headers.extend(additional_headers)

	lines.extend((f"{n}: {v}".encode(encoding = 'utf-8') for n, v in headers))

	return b'\r\n'.join(lines) + b'\r\n\r\n'

def gen_basic_response(status:tuple[int, str], content:bytes, content_type:str) -> bytes:
	header = gen_http_response_header(status, content_type, len(content))

	return header + content

def handle_http_request(client:socket, req_type:str, path:str, headers:dict[str, str]) -> None:
	data_type, db_content = get_data_entry(path)

	response = main_page_response.encode(encoding = 'utf-8')

	if db_content:
		response = gen_basic_response(__status_text[200], db_content, data_type)

	client.sendall(response)

def client_handler(connection:socket, ip:str, port:int, is_server_alive_fx:Callable[[], bool]) -> None:
	connection.settimeout(0.5)
	while is_server_alive_fx():
		try:
			http_req = receive_http_content(connection)
			if not http_req:
				break

			request_type, path, headers = extract_http_info(http_req)

			if is_websocket_req(headers):
				websocket_handler(connection, headers, is_server_alive_fx)
				break

			handle_http_request(connection, request_type, path, headers)
		except timeout:
			pass

	connection.close()

def http_report_handler(sock:socket, is_server_alive_fx:Callable[[], bool]) -> None:
	sock.settimeout(0.5)

	while is_server_alive_fx():
		try:
			connection, (c_ip, c_port) = sock.accept()

			connection.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

			client_thread = Thread(target = client_handler, args = (connection, c_ip, c_port, is_server_alive_fx))
			client_thread.start()
		except timeout:
			pass
