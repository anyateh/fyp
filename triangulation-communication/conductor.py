#!/usr/bin/env python3

import asyncio

from signal import signal, SIGINT, SIGTERM

from scripts.logger import logger
from scripts.server import TrianServer

import scripts.conductor.manage_antes as antes

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
	
	keep_server_alive = True
	ctrl_c_handled    = False

	async def handle_ctrl_c() -> None:
		nonlocal ctrl_c_handled
		if ctrl_c_handled:
			return
		ctrl_c_handled = True
		nonlocal keep_server_alive
		keep_server_alive = False
		await antes.stop_ante_updates()
		await server.close()

	asyncio.get_event_loop().add_signal_handler(SIGINT,  lambda: asyncio.ensure_future(handle_ctrl_c()))
	asyncio.get_event_loop().add_signal_handler(SIGTERM, lambda: asyncio.ensure_future(handle_ctrl_c()))

	await server.start_accepting_clients()

	loop_update_task = None

	def probe_exception(tsk:asyncio.Task) -> None:
		nonlocal loop_update_task
		loop_update_task = None
		tsk.result()

	while keep_server_alive:
		if not loop_update_task:
			loop_update_task = asyncio.create_task(antes.loop_ante_updates(server))
			loop_update_task.add_done_callback(probe_exception)

		await asyncio.sleep(1)
	
	if loop_update_task:
		await asyncio.wait_for(loop_update_task, timeout = None)

if __name__ == '__main__':
	asyncio.run(main_loop())