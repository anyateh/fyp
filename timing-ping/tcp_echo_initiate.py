#!/usr/bin/env python3

import logging
from argparse import ArgumentParser
from statistics import mean
from sys import stderr
from time import sleep

from tcp_echo.tcp_echo import tcp_echo_time_sender

DEFAULT_N_TIMES        = 5
DEFAULT_PORT           = 2310
DEFAULT_LISTENING_PORT = 2311

_logger = logging.getLogger(__name__)
_logger_console_handler = logging.StreamHandler()

_logger.addHandler(_logger_console_handler)
_logger_console_handler.setFormatter(logging.Formatter(
	"[%(levelname)s] %(message)s"
))
_logger.setLevel(logging.INFO)

# Return dest_ip, dest_port, own_ip, own_port, n_times
def parse_opts() -> tuple[str, int, str, int, int]:
	aparser = ArgumentParser(prog = "udp_echo_initiate")

	aparser.add_argument('-c', type = int, metavar = "n_times"  , default = DEFAULT_N_TIMES        , help = "Number of times to echo.")
	aparser.add_argument('-p', type = int, metavar = "dest_port", default = DEFAULT_PORT           , help = "Port number to send to.")
	aparser.add_argument('-l', type = int, metavar = "own_port" , default = DEFAULT_LISTENING_PORT , help = "Port number to listen from.")

	aparser.add_argument('dest_ip_hstname', help = 'Destination IP/Hostname')
	aparser.add_argument('own_ip_hstname' , help = 'Assigned IP/Hostname')

	args = aparser.parse_args()

	return args.dest_ip_hstname, args.p, args.own_ip_hstname, args.p if args.l is None else args.l, args.c

def main() -> None:
	receiver_hostname, receiver_port, sender_hostname, sender_port, n_times = parse_opts()

	_logger.debug(f"receiver_hostname -> {receiver_hostname}")
	_logger.debug(f"receiver_port     -> {receiver_port}")
	_logger.debug(f"sender_hostname   -> {sender_hostname}")
	_logger.debug(f"sender_port       -> {sender_port}")
	_logger.debug(f"n_times           -> {n_times}")

	echo_results = []

	try_col_header       = "Try"
	msg_col_header       = "Exchanged"
	success_col_header   = "Success"
	time_col_header      = "Time taken (s)"

	longest_try          = len(try_col_header)
	longest_msg          = len(msg_col_header)
	longest_success_fail = len(success_col_header)
	longest_time_taken   = len(time_col_header)



	while True:
		try:
			echo_results, time_taken_establish, total_time_taken = tcp_echo_time_sender(receiver_hostname, receiver_port, sender_hostname, sender_port, n_times)

			for try_no, msg_xchanged, success, time_taken in echo_results:
				longest_try        = max(longest_try, len(str(try_no)))
				longest_msg        = max(longest_msg, len(msg_xchanged))
				longest_time_taken = max(longest_time_taken, len(str(time_taken)))
	
			print(
				try_col_header    .ljust(longest_try),
				msg_col_header    .ljust(longest_msg),
				success_col_header.ljust(longest_success_fail),
				time_col_header   .ljust(longest_time_taken),
				sep = "  "
			)
			for n, m, s, t in echo_results:
				print(
					str(n)                          .rjust(longest_try),
					m                               .rjust(longest_msg),
					("yes" if s         else "no"  ).rjust(longest_success_fail),
					("N/A" if t is None else str(t)).rjust(longest_time_taken),
					sep = "  "
				)
	
			print("", file = stderr)
			print("Establishment time:           ", time_taken_establish, "seconds")
			print("Average echo time:            ", mean(i[3] for i in echo_results if i[2]), "seconds")
			print("Success rate:                  ", round(sum(1 for i in echo_results if i[2]) * 100 / len(echo_results), 1), "%", sep = "")
			print("Total time:                   ", total_time_taken, "seconds")
			break
		except OSError as e:
			_logger.info(f"{e}")
			_logger.info(f"Waiting for port {sender_port} to be available again...")
			sleep(1)

if __name__ == '__main__':
	main()
