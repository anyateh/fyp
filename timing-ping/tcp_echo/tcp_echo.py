import logging
from math import floor
from time import time
from socket import AF_INET, gaierror, SOCK_STREAM, socket
from sys import stderr
from typing import Optional

_logger = logging.getLogger(__name__)
_logger_console_handler = logging.StreamHandler()

_logger.addHandler(_logger_console_handler)
_logger_console_handler.setFormatter(logging.Formatter(
	"[%(levelname)s] %(message)s"
))
_logger.setLevel(logging.DEBUG)

# Returns 
#   echo_results         - list[tuple[try_no, msg, success, time_taken]]
#   time_taken_establish - Optional[float]
#   total_time_taken     - Optional[float]
def tcp_echo_time_sender(echo_to_hostname_ip:str, echo_to_port:int, own_hostname_ip:str, listening_port:int, n_times:int) -> tuple[list[tuple[int, str, bool, Optional[float]]], Optional[float], Optional[float]]:
	echo_results = []

	sock  = socket(AF_INET, SOCK_STREAM)
	sock.bind((own_hostname_ip, listening_port))
	sock.setblocking(True)

	t0 = time()

	# Establish connection to echo-ee first
	_logger.info(f"Establishing connection to echo-ee {echo_to_hostname_ip}:{echo_to_port}...")
	sock.connect((echo_to_hostname_ip, echo_to_port))
	_logger.info(f"Established connection to echo-ee!")

	t1 = time()

	for i in range(n_times):
		unix_time_str   = str(floor(time()))
		unix_time_bytes = unix_time_str.encode("utf-8")

		_logger.info(f"Sending the unix_timestamp to {echo_to_hostname_ip}:{echo_to_port}")
		_logger.debug(f"UNIX timestamp str        ->        {unix_time_str}")
		t2 = time()
		sock.sendall(unix_time_bytes)

		_logger.info(f"Awaiting response via {own_hostname_ip}:{listening_port}...")
		received_msg = sock.recv(1024)

		t3 = time()

		echo_results.append((i+1, unix_time_str, received_msg.decode("utf-8") == unix_time_str, t3 - t2))
		_logger.info(f"Received message:             '{received_msg}'")
		_logger.info(f"From:                         {echo_to_hostname_ip}:{echo_to_port}")
		_logger.info(f"Try {i+1} echo time measured: {t3 - t2} seconds")

	time_taken_establish = t1 - t0
	time_taken_total     = t3 - t0

	_logger.info(f"Established time measured:    {time_taken_establish} seconds")
	_logger.info(f"Total time measured:          {time_taken_total} seconds")

	_logger.info(f"Closing connection to {echo_to_hostname_ip}:{echo_to_port}")
	sock.close()

	return echo_results, time_taken_establish, time_taken_total
	# return [i[0] for i in echo_results], [i[1] for i in echo_results], time_taken_establish, [i[2] for i in echo_results], time_taken_total

def tcp_echo_time_receiver(own_hostname_ip:str, own_port:int) -> None:
	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind((own_hostname_ip, own_port))
	sock.setblocking(True)
	sock.listen(1)

	_logger.info("Waiting for request...")
	connection, (echoer_ip, echoer_port) = sock.accept()
	_logger.info(f"Got connection request from {echoer_ip}:{echoer_port}")


	while True:
		print("\n[REMINDER] Press ctrl-c to terminate\n", file = stderr)

		# _logger.info(f"Awaiting message via {own_hostname_ip}:{own_port}...")
		received_msg = connection.recv(1024)
		if not received_msg:
			_logger.info(f"Closing connection to {echoer_ip}:{echoer_port}")
			connection.close()
			break

		_logger.info(f"Received message: '{received_msg}' from {echoer_ip}:{echoer_port}")

		_logger.info(f"Echoing '{received_msg}' back to {echoer_ip}:{echoer_port}")
		connection.sendall(received_msg)
