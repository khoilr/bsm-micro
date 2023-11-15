import json
from typing import List, Union

from tortoise.exceptions import DoesNotExist

from database.models.event_log import EventLogModel


class EventLogDAO:
    @staticmethod
    async def get(event_log_id: int) -> Union[EventLogModel, None]:
        """
        Retrieve a specific EventLog by its ID.

        Args:
            event_log_id (int): EventLog ID

        Returns:
            Union[EventLogModel, None]: EventLog model or None if not found
        """
        try:
            return await EventLogModel.get(id=event_log_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_all() -> List[EventLogModel]:
        """
        Retrieve all EventLogs.

        Returns:
            List[EventLogModel]: List of event log models
        """
        return await EventLogModel.all()

    @staticmethod
    async def filter(**kwargs) -> List[EventLogModel]:
        """
        Filter EventLogs based on provided keyword arguments.

        Returns:
            List[EventLogModel]: List of event log models
        """
        return await EventLogModel.filter(**kwargs)

    @staticmethod
    async def create(**kwargs) -> EventLogModel:
        """
        Create a new EventLog using provided keyword arguments.

        Returns:
            EventLogModel: EventLog model
        """
        return await EventLogModel.create(**kwargs)

    @staticmethod
    async def update(event_log_id: int, **kwargs) -> None:
        """
        Update a specific EventLog using provided keyword arguments.

        Args:
            event_log_id (int): EventLog ID
        """
        event_log = await EventLogDAO.get(event_log_id)
        if event_log:
            await event_log.update_from_dict(kwargs).save()

    @staticmethod
    async def delete(event_log_id: int) -> None:
        """
        Delete a specific EventLog by its ID.

        Args:
            event_log_id (int): EventLog ID
        """
        event_log = await EventLogDAO.get(event_log_id)
        if event_log:
            await event_log.delete()

    @staticmethod
    def model_to_json(event_log: EventLogModel) -> dict:
        """
        Convert EventLogModel instance to JSON string.

        Args:
            event_log (EventLogModel): EventLog model

        Returns:
            dict: Model data as JSON key-value datatype
        """
        return event_log.to_json()
