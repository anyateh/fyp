import logging

NOTE = 25

logger = logging.getLogger("rtst_logger")
logger_console_handler = logging.StreamHandler()

logger.addHandler(logger_console_handler)
logger_console_handler.setFormatter(logging.Formatter(
	"[%(levelname)s] %(message)s"
))
logger.setLevel(logging.INFO)

logging.addLevelName(NOTE, "NOTE")

def set_colour_formatting() -> None:
	logging.addLevelName(logging.DEBUG, "\x1b[1;32mDEBUG\x1b[0m")
	logging.addLevelName(logging.INFO, "\x1b[1;34mINFO\x1b[0m")
	logging.addLevelName(NOTE, "\x1b[1;36mNOTE\x1b[0m")
	logging.addLevelName(logging.WARNING, "\x1b[1;33mWARNING\x1b[0m")
	logging.addLevelName(logging.ERROR, "\x1b[1;31mERROR\x1b[0m")
	logging.addLevelName(logging.CRITICAL, "\x1b[1;31mCRITICAL\x1b[0m")
