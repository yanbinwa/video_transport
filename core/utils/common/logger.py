import sys
import logging

# ignore asyncio warning message
logging.getLogger("asyncio").setLevel(logging.INFO)

LOG_FORMAT = "%(asctime)s %(levelname)-8s [%(process)d][%(thread)d] %(filename)s:%(lineno)-4d: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(stream=sys.stdout, format=LOG_FORMAT, level=logging.INFO, datefmt=DATE_FORMAT)
log = logging.getLogger("pyparser")

# 增加 gunicorn logger handler
gunicorn_logger = logging.getLogger('gunicorn.error')
log.handlers.extend(gunicorn_logger.handlers)
log.setLevel(gunicorn_logger.level)
