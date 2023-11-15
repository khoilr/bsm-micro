import json
from typing import List, Union

from database.models.action import ActionModel
from tortoise.exceptions import DoesNotExist


class ActionDAO:
    @staticmethod
    async def get(action_id: int) -> Union[ActionModel, None]:
        """
        Retrieve a specific Action entry by its ID.

        Args:
            action_id (int): Action ID

        Returns:
            Union[ActionModel, None]: Action model or None if not found
        """
        try:
            return await ActionModel.get(id=action_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_all() -> List[ActionModel]:
        """
        Retrieve all Action entries.

        Returns:
            List[ActionModel]: List of action models
        """
        return await ActionModel.all()

    @staticmethod
    async def filter(**kwargs) -> List[ActionModel]:
        """
        Filter Action entries based on provided keyword arguments.

        Returns:
            List[ActionModel]: List of action models
        """
        return await ActionModel.filter(**kwargs)

    @staticmethod
    async def create(**kwargs) -> ActionModel:
        """
        Create a new Action entry using provided keyword arguments.

        Returns:
            ActionModel: Action model
        """
        return await ActionModel.create(**kwargs)

    @staticmethod
    async def update(action_id: int, **kwargs) -> None:
        """
        Update a specific Action entry using provided keyword arguments.

        Args:
            action_id (int): Action ID
        """
        action = await ActionDAO.get(action_id)
        if action:
            await action.update_from_dict(kwargs).save()

    @staticmethod
    async def delete(action_id: int) -> None:
        """
        Delete a specific Action entry by its ID.

        Args:
            action_id (int): Action ID
        """
        action = await ActionDAO.get(action_id)
        if action:
            await action.delete()

    @staticmethod
    def model_to_json(action: ActionModel) -> dict:
        """
        Convert ActionModel instance to JSON string.

        Args:
            action (ActionModel): Action model

        Returns:
            dict: Model data as JSON key-value datatype
        """
        return action.to_json()
