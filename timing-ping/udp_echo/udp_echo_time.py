import logging
from math import floor
from time import time
from socket import AF_INET, gaierror, SOCK_DGRAM, socket
from typing import Optional

_logger = logging.getLogger(__name__)
_logger_console_handler = logging.StreamHandler()

_logger.addHandler(_logger_console_handler)
_logger_console_handler.setFormatter(logging.Formatter(
	"[%(levelname)s] %(message)s"
))
_logger.setLevel(logging.DEBUG)

def udp_echo_time_sender(echo_to_hostname_ip:str, echo_to_port:int, own_hostname_ip:str, listening_port:int) -> tuple[str, bool, Optional[float]]:
	unix_time_str   = str(floor(time()))
	unix_time_bytes = unix_time_str.encode("utf-8")

	sock  = socket(AF_INET, SOCK_DGRAM)
	sock.bind((own_hostname_ip, listening_port))

	sock.setblocking(True)
	sock.settimeout(3)

	_logger.info(f"Sending the unix_timestamp to {echo_to_hostname_ip}:{echo_to_port}")
	_logger.debug(f"UNIX timestamp str -> {unix_time_str}")
	t0 = time()
	sock.sendto(unix_time_bytes, (echo_to_hostname_ip, echo_to_port))

	try:
		_logger.info(f"Awaiting response via {own_hostname_ip}:{listening_port}...")
		received_msg, (from_hostname_ip, from_port) = sock.recvfrom(1024)
		t1 = time()
		time_taken = t1 - t0

		_logger.info(f"Received message: '{received_msg}' from {from_hostname_ip}:{from_port}")
		_logger.info(f"Time measured: {time_taken} seconds")
		return unix_time_str, received_msg.decode("utf-8") == unix_time_str, time_taken
	except TimeoutError:
		_logger.info(f"Timed out waiting response via {own_hostname_ip}:{listening_port}...")
		_logger.info("No response")
		return unix_time_str, False, None

def udp_echo_time_receiver(own_hostname_ip:str, own_port:int, echo_back_port:int) -> None:
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind((own_hostname_ip, own_port))

	sock.setblocking(True)
	_logger.info(f"Awaiting message via {own_hostname_ip}:{own_port}...")
	received_msg, (from_hostname_ip, from_port) = sock.recvfrom(1024)

	_logger.info(f"Received message: '{received_msg}' from {from_hostname_ip}:{from_port}")

	_logger.info(f"Echoing '{received_msg}' back to {from_hostname_ip}:{echo_back_port}")
	sock.sendto(received_msg, (from_hostname_ip, echo_back_port))
