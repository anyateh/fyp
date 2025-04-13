from socket import AF_INET, socket, SOCK_STREAM, timeout
from threading import Thread
from typing import Callable, Iterable, Optional

from .database import get_data_entry

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
	200: (200, "OK"),
	404: (404, "Not Found"),
	501: (501, "Not Implemented")
}

pages_cache = {}

def start_server() -> socket:
	listening_ip = "0.0.0.0"
	port         = 32311

	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind((listening_ip, port))
	sock.listen(1)

	return sock

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

	connection.settimeout(0.01)

	while len(fragment) == __HTTP_RECV_FRAGMENT_SIZE:
		try:
			fragment = connection.recv(__HTTP_RECV_FRAGMENT_SIZE)
			http_fragments.append(fragment)
		except timeout:
			break

	connection.settimeout(None)

	return b''.join(http_fragments)

def find_first_crlf(byte_seq:bytes) -> int:
	prev_b = None
	for i, byte in enumerate(byte_seq):
		if prev_b and prev_b == ord('\r') and byte == ord('\n'):
			return i - 1
		prev_b = byte

	return len(byte_seq)

def extract_http_first_line(byte_seq:bytes) -> str:
	first_crlf = find_first_crlf(byte_seq)
	return byte_seq[:first_crlf].decode(encoding = "utf-8")

# Returns request_type, request_path
def extract_http_info(http_packet:bytes) -> tuple[str, str]:
	first_l = extract_http_first_line(http_packet)

	if not first_l.endswith("HTTP/1.1"):
		return "", ""

	return tuple(first_l.rsplit(' ', 1)[0].split(' ', 1))


def get_basic_headers(content_type:str, content_len:int) -> list[tuple[str, str]]:
	return [
		("Content-Type", f"{content_type}" + ("; charset=UTF-8" if content_type.startswith("text/") else "")),
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

def client_handler(connection:socket, ip:str, port:int) -> None:
	http_req = receive_http_content(connection)

	request_type, path = extract_http_info(http_req)

	data_type, db_content = get_data_entry(path)

	response = main_page_response.encode(encoding = 'utf-8')

	if db_content:
		response = gen_basic_response(__status_text[200], db_content, data_type)

	connection.sendall(response)
	connection.close()

def http_report_handler(sock:socket, is_server_alive_fx:Callable[[], bool]) -> None:
	sock.settimeout(0.5)

	while is_server_alive_fx():
		try:
			connection, (c_ip, c_port) = sock.accept()

			client_thread = Thread(target = client_handler, args = (connection, c_ip, c_port))
			client_thread.start()
		except timeout:
			pass

if __name__ == '__main__':
	http_report_handler(start_server())
