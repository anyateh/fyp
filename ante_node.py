#!/usr/bin/env python3
import asyncio

from signal import signal, SIGINT
from sys import argv, stderr

from scripts.ante_terminal.client import AnteClient
from scripts.ante_terminal.obtain_signal import measure_dbm
from scripts.logger import logger, set_colour_formatting

def print_usage(arg0:str) -> None:
	print('usage:', arg0, 'id', 'x', 'y', 'ip_hostname', 'port', file = stderr)

def main() -> None:
	set_colour_formatting()

	if len(argv) < 6:
		print_usage(argv[0])
		return

	antenna_client = AnteClient(int(argv[1]), float(argv[2]), float(argv[3]), argv[4], int(argv[5]))

	antenna_client.start()
	def handle_ctrl_c(sig, frame) -> None:
		antenna_client.close()
		exit(0)

	signal(SIGINT, handle_ctrl_c)

	login_accept_pkt = antenna_client.request_login()

	if not login_accept_pkt:
		logger.error("Login request denied!")
		antenna_client.close()
		exit(1)

	keep_alive = True

	def ctrl_c_handler(sig, frame) -> None:
		nonlocal keep_alive
		keep_alive = False

	signal(SIGINT, ctrl_c_handler)

	while keep_alive:
		data_request_pkt = antenna_client.receive_packet_request()
		if not data_request_pkt:
			continue

		if data_request_pkt.is_kick_request():
			logger.debug("Received Kick request")
			if data_request_pkt.is_server_closing_noti():
				antenna_client.send_server_close_ack()
			else:
				antenna_client.send_kick_out_ack()
			logger.debug("Acknowledgement sent")
			antenna_client.close()
			return

		if data_request_pkt.is_coord_update_request():
			x, y = data_request_pkt.unpack_coord_update()
			if x:
				antenna_client.x = x
			if y:
				antenna_client.y = y
			continue

		if not data_request_pkt.is_dbm_data_request():
			continue

		fid = data_request_pkt.get_frame_id()

		dbm_measurement = asyncio.run(measure_dbm(antenna_client))

		antenna_client.send_requested_data(fid, dbm_measurement)

	logout_ack_pkt = antenna_client.request_logout()

	while not logout_ack_pkt:
		logout_ack_pkt = antenna_client.request_logout()

	antenna_client.close()

if __name__ == '__main__':
	main()
