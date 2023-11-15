import json
from typing import List, Union

from database.models.intruderlog import (
    LogModel,  # Assuming this is the import path for LogModel
)
from tortoise.exceptions import DoesNotExist


class LogDAO:
    @staticmethod
    async def get(log_id: int) -> Union[LogModel, None]:
        """
        Retrieve a specific Log by its ID.

        Args:
            log_id (int): Log ID

        Returns:
            Union[LogModel, None]: Log model or None if not found
        """
        try:
            return await LogModel.get(log_id=log_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_all() -> List[LogModel]:
        """
        Retrieve all Logs.

        Returns:
            List[LogModel]: List of log models
        """
        return await LogModel.all()

    @staticmethod
    async def filter(**kwargs) -> List[LogModel]:
        """
        Filter Logs based on provided keyword arguments.

        Returns:
            List[LogModel]: List of log models
        """
        return await LogModel.filter(**kwargs)

    @staticmethod
    async def create(**kwargs) -> LogModel:
        """
        Create a new Log using provided keyword arguments.

        Returns:
            LogModel: Log model
        """
        return await LogModel.create(**kwargs)

    @staticmethod
    async def update(log_id: int, **kwargs) -> None:
        """
        Update a specific Log using provided keyword arguments.

        Args:
            log_id (int): Log ID
        """
        log = await LogDAO.get(log_id)
        if log:
            await log.update_from_dict(kwargs).save()

    @staticmethod
    async def delete(log_id: int) -> None:
        """
        Delete a specific Log by its ID.

        Args:
            log_id (int): Log ID
        """
        log = await LogDAO.get(log_id)
        if log:
            await log.delete()

    @staticmethod
    def model_to_json(log: LogModel) -> dict:
        """
        Convert LogModel instance to JSON string.

        Args:
            log (LogModel): Log model

        Returns:
            dict: Model data as JSON key-value datatype
        """
        return log.to_json()
