#!/usr/bin/env python3

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

def send_msg(hostname_ip:str, port:int, msg:bytes) -> None:
	sock = socket(AF_INET, SOCK_DGRAM)
	_logger.info(f"Sending message to {hostname_ip}:{port}")
	sock.sendto(msg, (hostname_ip, port))

def udp_echo_time_sender(sender_hostname_ip:str, sender_port:int, receiver_hostname_ip:str, receiver_port:int) -> None:
	unix_time_str = str(floor(time()))
	sock = socket(AF_INET, SOCK_DGRAM)
	_logger.info(f"Sending the unix_timestamp to {receiver_hostname_ip}:{receiver_port}")
	_logger.debug(f"UNIX timestamp str -> {unix_time_str}")
	t0 = time()
	sock.sendto(unix_time_str.encode(encoding = "utf-8"), (receiver_hostname_ip, receiver_port))

	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind((sender_hostname_ip, sender_port))

	sock.setblocking(True)
	_logger.info(f"Awaiting response via {sender_hostname_ip}:{sender_port}...")
	received_msg, sending_addr = sock.recvfrom(1024)
	t1 = time()
	time_taken = t1 - t0

	_logger.info(f"Received message: '{received_msg}' from {sending_addr}")
	_logger.info(f"Time measured: {time_taken} seconds")

def udp_echo_time_receiver(sender_hostname_ip:str, sender_port:int, receiver_hostname_ip:str, receiver_port:int) -> None:
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind((receiver_hostname_ip, receiver_port))

	sock.setblocking(True)
	_logger.info(f"Awaiting message via {receiver_hostname_ip}:{receiver_port}...")
	received_msg, sender_addr = sock.recvfrom(1024)

	_logger.info(f"Received message: '{received_msg}' from {sender_addr}")

	_logger.info(f"Echoing '{received_msg}' back to {sender_hostname_ip}:{sender_port}")
	sock.sendto(received_msg, (sender_hostname_ip, sender_port))
