import json
from typing import List, Union

from tortoise.exceptions import DoesNotExist

from database.models.event import EventModel


class EventDAO:
    @staticmethod
    async def get(event_id: int) -> Union[EventModel, None]:
        """
        Retrieve a specific Event by its ID.

        Args:
            event_id (int): Event ID

        Returns:
            Union[EventModel, None]: Event model or None if not found
        """
        try:
            return await EventModel.get(id=event_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_all() -> List[EventModel]:
        """
        Retrieve all Events.

        Returns:
            List[EventModel]: List of event models
        """
        return await EventModel.all()

    @staticmethod
    async def filter(**kwargs) -> List[EventModel]:
        """
        Filter Events based on provided keyword arguments.

        Returns:
            List[EventModel]: List of event models
        """
        return await EventModel.filter(**kwargs)

    @staticmethod
    async def create(**kwargs) -> EventModel:
        """
        Create a new Event using provided keyword arguments.

        Returns:
            EventModel: Event model
        """
        return await EventModel.create(**kwargs)

    @staticmethod
    async def update(event_id: int, **kwargs) -> None:
        """
        Update a specific Event using provided keyword arguments.

        Args:
            event_id (int): Event ID
        """
        event = await EventDAO.get(event_id)
        if event:
            await event.update_from_dict(kwargs).save()

    @staticmethod
    async def delete(event_id: int) -> None:
        """
        Delete a specific Event by its ID.

        Args:
            event_id (int): Event ID
        """
        event = await EventDAO.get(event_id)
        if event:
            await event.delete()

    @staticmethod
    def model_to_json(event: EventModel) -> dict:
        """
        Convert EventModel instance to JSON string.

        Args:
            event (EventModel): Event model

        Returns:
            dict: Model data as JSON key-value datatype
        """
        return event.to_json()
