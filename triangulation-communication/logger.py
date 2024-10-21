import logging

logger = logging.getLogger("rtst_logger")
logger_console_handler = logging.StreamHandler()

logger.addHandler(logger_console_handler)
logger_console_handler.setFormatter(logging.Formatter(
	"[%(levelname)s] %(message)s"
))
logger.setLevel(logging.DEBUG)
