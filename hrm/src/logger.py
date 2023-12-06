from loguru import logger
from datetime import datetime

logger.add(f"logs/{datetime.now().astimezone().isoformat()}.log", rotation="500 MB")
