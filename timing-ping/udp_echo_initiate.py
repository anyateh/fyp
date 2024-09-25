#!/usr/bin/env python3

import json

from udp_echo.udp_echo_time import udp_echo_time_sender

def main() -> None:
	echo_results = []

	n_times = 4

	sender_hostname   = "192.168.1.117"
	sender_port       = 2310
	receiver_hostname = "emma.local"
	receiver_port     = 2310

	msg_xchanged, time_taken = udp_echo_time_sender(receiver_hostname, receiver_port, sender_hostname, sender_port)

	print(time_taken)
	# for i in range(4):
	#     try:
	#         msg_xchanged, time_taken = udp_echo_time_sender(receiver_hostname, receiver_port, sender_hostname, sender_port)
	#         echo_results.append((msg_xchanged, True, time_taken))
	#     except TimeoutError:


if __name__ == '__main__':
	main()
