import json
from typing import List, Union

from database.models.attendance import AttendaceTrackingModel
from tortoise.exceptions import DoesNotExist


class AttendanceTrackingDAO:
    @staticmethod
    async def get(tracking_id: int) -> Union[AttendaceTrackingModel, None]:
        """
        Retrieve a specific AttendanceTracking entry by its ID.

        Args:
            tracking_id (int): Attendance Tracking ID

        Returns:
            Union[AttendaceTrackingModel, None]: AttendanceTracking model or None if not found
        """
        try:
            return await AttendaceTrackingModel.get(tracking_id=tracking_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_all() -> List[AttendaceTrackingModel]:
        """
        Retrieve all AttendanceTracking entries.

        Returns:
            List[AttendaceTrackingModel]: List of attendance tracking models
        """
        return await AttendaceTrackingModel.all()

    @staticmethod
    async def filter(**kwargs) -> List[AttendaceTrackingModel]:
        """
        Filter AttendanceTracking entries based on provided keyword arguments.

        Returns:
            List[AttendaceTrackingModel]: List of attendance tracking models
        """
        return await AttendaceTrackingModel.filter(**kwargs)

    @staticmethod
    async def create(**kwargs) -> AttendaceTrackingModel:
        """
        Create a new AttendanceTracking entry using provided keyword arguments.

        Returns:
            AttendaceTrackingModel: AttendanceTracking model
        """
        return await AttendaceTrackingModel.create(**kwargs)

    @staticmethod
    async def update(tracking_id: int, **kwargs) -> None:
        """
        Update a specific AttendanceTracking entry using provided keyword arguments.

        Args:
            tracking_id (int): Attendance Tracking ID
        """
        attendance_tracking = await AttendanceTrackingDAO.get(tracking_id)
        if attendance_tracking:
            await attendance_tracking.update_from_dict(kwargs).save()

    @staticmethod
    async def delete(tracking_id: int) -> None:
        """
        Delete a specific AttendanceTracking entry by its ID.

        Args:
            tracking_id (int): Attendance Tracking ID
        """
        attendance_tracking = await AttendanceTrackingDAO.get(tracking_id)
        if attendance_tracking:
            await attendance_tracking.delete()

    @staticmethod
    def model_to_json(attendance_tracking: AttendaceTrackingModel) -> dict:
        """
        Convert AttendaceTrackingModel instance to JSON string.

        Args:
            attendance_tracking (AttendaceTrackingModel): AttendanceTracking model

        Returns:
            dict: Model data as JSON key-value datatype
        """
        return attendance_tracking.to_json()
