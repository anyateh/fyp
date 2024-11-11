#!/usr/bin/env python3

import asyncio

from signal import signal, SIGINT

from scripts.logger import logger
from scripts.server import TrianServer

import scripts.leader_node.manage_antes as antes

async def main_loop() -> None:
	server = TrianServer("0.0.0.0", 32310)

	while True:
		try:
			server.start()
			break
		except OSError as e:
			logger.info(f"{e}")
			logger.info("Waiting for port to be available again...")
			await asyncio.sleep(1)
	
	def handle_ctrl_c(sig, frame) -> None:
		server.stop_accepting_clients()
		server.close()
		exit(0)

	signal(SIGINT, handle_ctrl_c)

	await server.start_accepting_clients()

	loop_update_task = None

	def probe_exception(tsk:asyncio.Task) -> None:
		nonlocal loop_update_task
		loop_update_task = None
		tsk.result()

	while True:
		if not loop_update_task:
			loop_update_task = asyncio.create_task(antes.loop_ante_updates(server))
			loop_update_task.add_done_callback(probe_exception)

		await asyncio.sleep(1)

if __name__ == '__main__':
	asyncio.run(main_loop())