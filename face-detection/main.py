import asyncio

from src.app import app
from src.logger import logger

if __name__ == "__main__":
    logger.info("Starting application")
    asyncio.run(app())
