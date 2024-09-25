import logging
from math import floor
from time import time
from socket import AF_INET, gaierror, SOCK_DGRAM, socket

_logger = logging.getLogger(__name__)
_logger_console_handler = logging.StreamHandler()

_logger.addHandler(_logger_console_handler)
_logger_console_handler.setFormatter(logging.Formatter(
	"[%(levelname)s] %(message)s"
))
_logger.setLevel(logging.DEBUG)

def udp_echo_time_sender(echo_to_hostname_ip:str, echo_to_port:int, own_hostname_ip:str, listening_port:int) -> tuple[float]:
	unix_time_str = str(floor(time()))

	sock  = socket(AF_INET, SOCK_DGRAM)
	sock.bind((own_hostname_ip, listening_port))

	rsock = socket(AF_INET, SOCK_DGRAM)
	rsock.bind((own_hostname_ip, listening_port))
	rsock.setblocking(True)
	rsock.settimeout(3)

	_logger.info(f"Sending the unix_timestamp to {echo_to_hostname_ip}:{echo_to_port}")
	_logger.debug(f"UNIX timestamp str -> {unix_time_str}")
	t0 = time()
	sock.sendto(unix_time_str.encode(encoding = "utf-8"), (echo_to_hostname_ip, echo_to_port))

	_logger.info(f"Awaiting response via {own_hostname_ip}:{listening_port}...")
	received_msg, (from_hostname_ip, from_port) = rsock.recvfrom(1024)
	t1 = time()
	time_taken = t1 - t0

	_logger.info(f"Received message: '{received_msg}' from {from_hostname_ip}:{from_port}")
	_logger.info(f"Time measured: {time_taken} seconds")
	return time_taken

def udp_echo_time_receiver(own_hostname_ip:str, own_port:int, echo_back_port:int) -> None:
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind((own_hostname_ip, own_port))

	sock.setblocking(True)
	_logger.info(f"Awaiting message via {own_hostname_ip}:{own_port}...")
	received_msg, (from_hostname_ip, from_port) = sock.recvfrom(1024)

	_logger.info(f"Received message: '{received_msg}' from {from_hostname_ip}:{from_port}")

	_logger.info(f"Echoing '{received_msg}' back to {from_hostname_ip}:{echo_back_port}")
	sock.sendto(received_msg, (from_hostname_ip, echo_back_port))
