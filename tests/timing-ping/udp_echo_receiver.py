#!/usr/bin/env python3

from argparse import ArgumentParser
from sys import stderr

from udp_echo.udp_echo_time import udp_echo_time_receiver

DEFAULT_PORT = 2310

# Return own_ip, own_port, echo_port
def parse_opts() -> tuple[str, int, int]:
	aparser = ArgumentParser(prog = "udp_echo_initiate")

	aparser.add_argument('-p', type = int, metavar = "listening_port", default = DEFAULT_PORT   , help = "Port number to listen.")
	aparser.add_argument('-b', type = int, metavar = "echo_back_port", default = None           , help = "Port number to echo back.")

	aparser.add_argument('own_ip_hstname' , help = 'Assigned IP/Hostname')

	args = aparser.parse_args()

	return args.own_ip_hstname, args.p, args.p if args.b is None else args.b

def main() -> None:
	# listening_hostname = "emma.local"
	# listening_port     = 2310
	# echo_back_port     = 2310

	listening_hostname, listening_port, echo_back_port = parse_opts()

	while True:
		print("\n[REMINDER] Press ctrl-c to terminate\n", file = stderr)
		udp_echo_time_receiver(listening_hostname, listening_port, echo_back_port)

if __name__ == '__main__':
	main()
