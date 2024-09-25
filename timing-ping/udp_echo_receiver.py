#!/usr/bin/env python3

from udp_echo.udp_echo_time import udp_echo_time_receiver

def main() -> None:
	listening_hostname = "emma.local"
	listening_port     = 2310
	echo_back_port     = 2310

	while True:
		udp_echo_time_receiver(listening_hostname, listening_port, echo_back_port)

if __name__ == '__main__':
	main()
