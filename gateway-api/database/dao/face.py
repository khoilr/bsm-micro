import json
from typing import List, Union

from tortoise.exceptions import DoesNotExist

from database.models.face import FaceModel


class FaceDAO:
    @staticmethod
    async def get(face_id: int) -> Union[FaceModel, None]:
        """
        Retrieve a specific Face by its ID.

        Args:
            face_id (int): Face ID

        Returns:
            Union[FaceModel, None]: Face model or None if not found
        """
        try:
            return await FaceModel.get(face_id=face_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_all() -> List[FaceModel]:
        """
        Retrieve all Faces.

        Returns:
            List[FaceModel]: List of face models
        """
        return await FaceModel.all()

    @staticmethod
    async def filter(**kwargs) -> List[FaceModel]:
        """
        Filter Faces based on provided keyword arguments.

        Returns:
            List[FaceModel]: List of face models
        """
        return await FaceModel.filter(**kwargs)

    @staticmethod
    async def create(**kwargs) -> FaceModel:
        """
        Create a new Face using provided keyword arguments.

        Returns:
            FaceModel: Face model
        """
        return await FaceModel.create(**kwargs)

    @staticmethod
    async def update(face_id: int, **kwargs) -> None:
        """
        Update a specific Face using provided keyword arguments.

        Args:
            face_id (int): Face ID
        """
        face = await FaceDAO.get(face_id)
        if face:
            await face.update_from_dict(kwargs).save()

    @staticmethod
    async def delete(face_id: int) -> None:
        """
        Delete a specific Face by its ID.

        Args:
            face_id (int): Face ID
        """
        face = await FaceDAO.get(face_id)
        if face:
            await face.delete()

    @staticmethod
    def model_to_json(face: FaceModel) -> dict:
        """
        Convert FaceModel instance to JSON string.

        Args:
            face (FaceModel): Face model

        Returns:
            dict: Model data as JSON key-value datatype
        """
        return face.to_json()
