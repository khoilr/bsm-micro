import json
from typing import List, Optional, Union

from tortoise.exceptions import DoesNotExist

from database.models.user import UserModel


class UserDAO:
    """Class for accessing user table."""

    @staticmethod
    async def get(user_id: IndentationError) -> Union[UserModel, None]:
        """
        Add single user to session.

        Args:
            user_id (int): user id

        Returns:
            Union[UserModel, None]: User model
        """
        try:
            return await UserModel.get(user_id=user_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_all() -> List[UserModel]:
        """
        Get all user models.

        Returns:
            List[UserModel]: List of user models
        """
        return await UserModel.all()

    @staticmethod
    async def filter(**kwargs) -> List[UserModel]:
        """
        Filter the user models.

        Returns:
            List[UserModel]: List of user models
        """
        return await UserModel.filter(**kwargs)

    @staticmethod
    async def create(**kwargs) -> UserModel:
        """
        Create user model.

        Returns:
            UserModel: user model
        """
        return await UserModel.create(**kwargs)

    @staticmethod
    async def delete(user_id: int) -> None:
        """
        Delete user model.

        Args:
            user_id (int): user id to delete
        """
        user = await UserDAO.get(user_id)
        if user:
            await user.delete()

    @staticmethod
    def model_to_json(user: UserModel) -> dict:
        """
        Convert model to json data type.

        Args:
            user (UserModel): user model

        Returns:
            dict: Model data as JSON key-value datatype
        """
        return user.to_json()
