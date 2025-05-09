from base64 import b64encode
from hashlib import sha1
from math import isinf, isnan
from os import path
from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, timeout
from sys import stderr
from traceback import format_exc, TracebackException
from threading import Thread
from typing import Callable, Iterable, Optional

from .database import get_data_entry
from ..dummy.set_dummy_coord import set_dummy_coord
from ..manage_antes import gen_json_update, set_dbm_averaging_size, set_radii_averaging_size, set_use_avg_dbm, set_use_avg_rad, update_ante_coords
from ..trilateration.trilaterate import calibrate_space_path_loss, calibrate_reference_distance, calibrate_transmitter_frequency, calibrate_transmitter_power
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
	204: (204, "No Content"),
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

	poll_timeout = 0.1

	websocket.settimeout(poll_timeout)

	while is_server_alive_fx():
		try:
			received_bytes = websocket.recv(1024)

			if not received_bytes:
				break

			if not is_valid_client_frame(received_bytes):
				break

			if get_optcode(received_bytes) != OPTTEXT:
				continue

			new_timeout_text = extract_text_frame(received_bytes)

			try:
				poll_timeout = float(new_timeout_text)
				if not isinf(poll_timeout) and not isnan(poll_timeout):
					websocket.settimeout(poll_timeout)
			except ValueError:
				continue
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

def extract_http_first_line(byte_seq:bytes) -> str:
	return byte_seq.split(b'\r\n', 1)[0].decode(encoding = "utf-8")

# Returns request_type, request_path, headers
def extract_http_info(http_packet:bytes) -> tuple[str, str, dict[str, str]]:
	first_l = extract_http_first_line(http_packet)

	__html_header_content_split = http_packet.split(b'\r\n\r\n', 1)[0].split(b'\r\n', 1)

	if len(__html_header_content_split) != 2:
		return

	first_l, headers = __html_header_content_split

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

def send_plain_text_message_response(status:tuple[int, str], client:socket, text:str) -> None:
	response = gen_basic_response(status, text.encode(encoding = 'utf-8'), "text/plain")
	client.sendall(response)

def send_censored_traceback(e:Exception, client:socket) -> None:
	exc_tb = TracebackException(type(e), e, e.__traceback__)
	# https://stackoverflow.com/questions/69925180/python-tracebacks-how-to-hide-absolute-paths
	for frame_sum in exc_tb.stack:
		frame_sum.filename = path.relpath(frame_sum.filename)

	# response = gen_basic_response(__status_text[200], format_exc().encode(encoding = 'utf-8'), "text/plain")
	response = gen_basic_response(__status_text[200], ''.join(exc_tb.format()).encode(encoding = 'utf-8'), "text/plain")
	client.sendall(response)

def handle_set_dummy_coord_req(client:socket, post_content:bytes) -> None:
	decoded_content = post_content.decode(encoding = 'utf-8')

	try:
		kv_pairs = decoded_content.split("&")

		coords = {k: v for k, v in (i.split('=') for i in kv_pairs)}

		x = float(coords['x'])
		y = float(coords['y'])

		assert not isnan(x)
		assert not isnan(y)
		assert not isinf(x)
		assert not isinf(y)

		set_dummy_coord(x, y, True)

		send_plain_text_message_response(__status_text[200], client, "Attempted to move dummy node.")
	except Exception as e:
		send_censored_traceback(e, client)

def handle_set_use_avg_req(client:socket, post_content:bytes, avg_dbm:bool = False) -> None:
	set_use_avg:Callable[[bool], None] = \
		lambda x: set_use_avg_dbm(x) if avg_dbm else set_use_avg_rad(x)

	if post_content == b'on':
		set_use_avg(True)
	elif post_content == b'off':
		set_use_avg(False)

	send_plain_text_message_response(__status_text[204], client, "")

def handle_set_x_y_id_req(client:socket, post_content:bytes) -> None:
	decoded_content = post_content.decode(encoding = 'utf-8')
	kv_pairs = decoded_content.split("&")
	info = {k: v for k, v in (i.split('=') for i in kv_pairs)}

	try:
		x = float(info['x'])
		y = float(info['y'])
		aid = int(info['id'])

		assert not isnan(x)
		assert not isnan(y)
		assert not isinf(x)
		assert not isinf(y)

		update_ante_coords(aid, x, y)

		# response = gen_basic_response(
		# 	__status_text[200], b"Attempted to move Antenna #"
		# 	+ info['id'].encode(encoding = 'utf-8') + b".",
		# 	"text/plain"
		# )
		# client.sendall(response)
		send_plain_text_message_response(__status_text[200], client,
			"Attempted to move Antenna #{} to ({}, {})." \
				.format(info['id'], info['x'], info['y'])
		)
	except Exception as e:
		send_censored_traceback(e, client)

def calibrate_trilateration_float(
		client:socket, post_content:bytes,
		calibrate_fx:Callable[[float], None], 
		key_name:str, val_desc:str, success_msg_fmt:str
	) -> None:
	decoded_content = post_content.decode(encoding = 'utf-8')
	
	try:
		kv_pairs = decoded_content.split("&")
		info = {k: v for k, v in (i.split('=') for i in kv_pairs)}

		float_val = float(info[key_name])

		if isnan(float_val):
			raise ValueError(f"{val_desc} given is NaN.")

		if isinf(float_val):
			raise ValueError(f"{val_desc} given is a form of infinity.")

		calibrate_fx(float_val)

		send_plain_text_message_response(
			__status_text[200], client, success_msg_fmt % (float_val,)
		)
	except Exception as e:
		send_censored_traceback(e, client)

def adjust_dbm_avg_size(
		client:socket, post_content:bytes
	) -> None:
	decoded_content = post_content.decode(encoding = 'utf-8')
	
	try:
		kv_pairs = decoded_content.split("&")
		info = {k: v for k, v in (i.split('=') for i in kv_pairs if '=' in i)}
		size = int(info["size"])

		if size <= 0:
			raise ValueError("Cannot set to Negative Values.")

		set_dbm_averaging_size(size)

		send_plain_text_message_response(
			__status_text[200], client,
			f"Set dBm averaging to last {size} items."
		)
	except Exception as e:
		send_censored_traceback(e, client)

def adjust_radius_avg_size(
		client:socket, post_content:bytes
	) -> None:
	decoded_content = post_content.decode(encoding = 'utf-8')
	
	try:
		kv_pairs = decoded_content.split("&")
		info = {k: v for k, v in (i.split('=') for i in kv_pairs if '=' in i)}
		size = int(info["size"])

		if size <= 0:
			raise ValueError("Cannot set to Negative Values.")

		set_radii_averaging_size(size)

		send_plain_text_message_response(
			__status_text[200], client,
			f"Set radii averaging to last {size} items."
		)
	except Exception as e:
		send_censored_traceback(e, client)

def handle_http_request(client:socket, req_type:str, path:str, headers:dict[str, str], request_content:bytes) -> None:
	if req_type == 'POST':
		if path == '/set_dummy_coords':
			handle_set_dummy_coord_req(client, request_content);
			return
		if path == '/set_use_averaging' or path == '/set_use_averaging_rad':
			handle_set_use_avg_req(client, request_content, False);
			return
		if path == '/set_use_averaging_dbm':
			handle_set_use_avg_req(client, request_content, True);
			return
		if path == '/set_ante_coords':
			handle_set_x_y_id_req(client, request_content);
			return
		if path == '/calibrate_transmitter_power':
			calibrate_trilateration_float(
				client, request_content,
				calibrate_transmitter_power,
				"dbm",
				"Transmitter power dBm value",
				"Transmitter power (value of P0) is calibrated to %f."
			);
			return
		if path == '/calibrate_reference_distance':
			calibrate_trilateration_float(
				client, request_content,
				calibrate_reference_distance,
				"d0",
				"Reference distance value",
				"Reference distance (value of d0) is calibrated to %f."
			);
			return
		if path == '/calibrate_signal_frequency':
			calibrate_trilateration_float(
				client, request_content,
				calibrate_transmitter_frequency,
				"frequency",
				"Signal frequency value",
				"Signal frequency is calibrated to %f."
			);
			return
		if path == '/calibrate_path_loss':
			calibrate_trilateration_float(
				client, request_content,
				calibrate_space_path_loss,
				"loss",
				"Path loss value",
				"Path loss is calibrated to %f."
			);
			return
		if path == '/set_dbm_avg_size':
			adjust_dbm_avg_size(client, request_content);
			return
		if path == '/set_radii_avg_size':
			adjust_radius_avg_size(client, request_content);
			return

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

			# TODO: Make below crash-proof
			request_type, path, headers = extract_http_info(http_req)

			if is_websocket_req(headers):
				websocket_handler(connection, headers, is_server_alive_fx)
				break

			handle_http_request(connection, request_type, path, headers, http_req.split(b'\r\n\r\n', 1)[1])
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
