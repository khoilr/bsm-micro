from tortoise.exceptions import DoesNotExist
from typing import List, Union
import json
from database.models.camera import CameraModel


class CameraDAO:
    @staticmethod
    async def get(camera_id: int) -> Union[CameraModel, None]:
        """
        Retrieve a specific Camera by its ID.

        Args:
            camera_id (int): Camera ID

        Returns:
            Union[CameraModel, None]: Camera model or None if not found
        """
        try:
            return await CameraModel.get(id=camera_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_all() -> List[CameraModel]:
        """
        Retrieve all Cameras.

        Returns:
            List[CameraModel]: List of camera models
        """
        return await CameraModel.all()

    @staticmethod
    async def filter(**kwargs) -> List[CameraModel]:
        """
        Filter Cameras based on provided keyword arguments.

        Returns:
            List[CameraModel]: List of camera models
        """
        return await CameraModel.filter(**kwargs)

    @staticmethod
    async def create(**kwargs) -> CameraModel:
        """
        Create a new Camera using provided keyword arguments.

        Returns:
            CameraModel: Camera model
        """
        return await CameraModel.create(**kwargs)

    @staticmethod
    async def update(camera_id: int, **kwargs):
        """
        Update a specific Camera using provided keyword arguments.

        Args:
            camera_id (int): Camera ID
        """
        camera = await CameraDAO.get(camera_id)
        if camera:
            await camera.update_from_dict(kwargs).save()

    @staticmethod
    async def delete(camera_id: int) -> None:
        """
        Delete a specific Camera by its ID.

        Args:
            camera_id (int): Camera ID
        """
        camera = await CameraDAO.get(camera_id)
        if camera:
            await camera.delete()
            return camera

    @staticmethod
    def model_to_json(camera: CameraModel) -> dict:
        """
        Convert CameraModel instance to JSON string.

        Args:
            camera (CameraModel): Camera model

        Returns:
            dict: Model data as JSON key-value datatype
        """
        return camera.to_json()
