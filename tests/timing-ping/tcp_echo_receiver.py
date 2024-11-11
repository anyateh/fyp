#!/usr/bin/env python3

from argparse import ArgumentParser
from os import write as os_write
from sys import stderr
from time import sleep

from tcp_echo.tcp_echo import tcp_echo_time_receiver

DEFAULT_PORT           = 2311

# Return own_ip, own_port
def parse_opts() -> tuple[str, int]:
	aparser = ArgumentParser(prog = "udp_echo_initiate")

	aparser.add_argument('-p', type = int, metavar = "listening_port", default = DEFAULT_PORT          , help = "Port number to listen.")

	aparser.add_argument('own_ip_hstname' , help = 'Assigned IP/Hostname')

	args = aparser.parse_args()

	return args.own_ip_hstname, args.p

def main() -> None:
	listening_hostname, listening_port = parse_opts()

	while True:
		try:
			tcp_echo_time_receiver(listening_hostname, listening_port)
		except OSError as e:
			os_write(stderr, f"[INFO] {e}\n[INFO] Waiting for port {listening_port} to be available again...")
			sleep(1)

if __name__ == '__main__':
	main()
