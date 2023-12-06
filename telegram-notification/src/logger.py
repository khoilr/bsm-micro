from datetime import datetime

from loguru import logger

logger.add(f"logs/{datetime.now().astimezone().isoformat()}.log", rotation="500 MB")
