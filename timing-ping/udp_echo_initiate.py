#!/usr/bin/env python3

import json
from statistics import mean

from udp_echo.udp_echo_time import udp_echo_time_sender

def main() -> None:
	echo_results = []

	try_col_header       = "Try"
	msg_col_header       = "Exchanged"
	success_col_header   = "Success"
	time_col_header      = "Time taken (s)"

	longest_try          = len(try_col_header)
	longest_msg          = len(msg_col_header)
	longest_success_fail = len(success_col_header)
	longest_time_taken   = len(time_col_header)

	n_times = 4

	sender_hostname   = "192.168.1.117"
	sender_port       = 2310
	receiver_hostname = "emma.local"
	receiver_port     = 2310

	for i in range(n_times):
		msg_xchanged, success, time_taken = udp_echo_time_sender(receiver_hostname, receiver_port, sender_hostname, sender_port)

		echo_results.append((str(i + 1), msg_xchanged, success, time_taken))

		longest_try        = max(longest_try, len(str(i + 1)))
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
			n                       .rjust(longest_try),
			m                       .rjust(longest_msg),
			("yes"  if s else "no" ).rjust(longest_success_fail),
			(str(t) if s else "N/A").rjust(longest_time_taken),
			sep = "  "
		)
	
	# print("Average:", mean(map(lambda a: a[3], filter(lambda a: a[2], echo_results))), "seconds")
	# print("Success Rate: ", round([i[2] for i in echo_results].count(True) * 100 / len(echo_results), 1), "%", sep = "")
	print("Average:", mean(i[3] for i in echo_results if i[2]), "seconds")
	print("Success Rate: ", round(sum(1 for i in echo_results if i[2]) * 100 / len(echo_results), 1), "%", sep = "")

if __name__ == '__main__':
	main()
