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

def time_echo_udp(hostname_ip:str, port:int) -> None:
	unix_time_str = str(floor(time()))
	sock = socket(AF_INET, SOCK_DGRAM)
	_logger.info(f"Sending the unix_timestamp to {hostname_ip}:{port}")
	_logger.debug(f"UNIX timestamp str -> {unix_time_str}")
	sock.sendto(unix_time_str.encode(encoding = "utf-8"), (hostname_ip, port))

	sock.bind((hostname_ip, port))

	sock.setblocking(True)
	_logger.info(f"Awaiting response via {hostname_ip}:{port}...")
	received_msg, sending_addr = sock.recvfrom(1024)

	_logger.info(f"Received message: '{received_msg}' from {sending_addr}")

def echo_back_time_udp(hostname_ip:str, port:int) -> None:
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind((hostname_ip, port))

	sock.setblocking(True)
	_logger.info(f"Awaiting message via {hostname_ip}:{port}...")
	received_msg, sender_addr = sock.recvfrom(1024)

	_logger.info(f"Received message: '{received_msg}' from {sender_addr}")

	_logger.info(f"Echoing '{received_msg}' back to {hostname_ip}")
	sock.sendto(received_msg, (hostname_ip, port))
