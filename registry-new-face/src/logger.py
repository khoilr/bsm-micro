from datetime import datetime

from loguru import logger

# config file name as current time in isoformat with .log extension, store in logs dir
logger.add(
    f"logs/{datetime.now().isoformat(timespec='seconds')}.log",
    rotation="1 day",
    level="INFO",
)
