from tortoise.exceptions import DoesNotExist
from typing import List, Union
import json
from database.models.zone import ZoneModel


class ZoneDAO:
    @staticmethod
    async def get(zone_id: int) -> Union[ZoneModel, None]:
        """
        Retrieve a specific Zone by its ID.

        Args:
            zone_id (int): Zone id

        Returns:
            Union[ZoneModel, None]: Zone model or None if not found
        """
        try:
            return await ZoneModel.get(zone_id=zone_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_all() -> List[ZoneModel]:
        """
        Retrieve all Zones.

        Returns:
            List[ZoneModel]: list of zone models
        """
        return await ZoneModel.all()

    @staticmethod
    async def filter(**kwargs) -> List[ZoneModel]:
        """
        Filter Zones based on provided keyword arguments.

        Returns:
            List[ZoneModel]: List of zone models
        """
        return await ZoneModel.filter(**kwargs)

    @staticmethod
    async def create(**kwargs) -> ZoneModel:
        """
        Create a new Zone using provided keyword arguments.

        Returns:
            ZoneModel: Zone model
        """
        return await ZoneModel.create(**kwargs)

    @staticmethod
    async def update(zone_id: int, **kwargs):
        """
        Update a specific Zone using provided keyword arguments.

        Args:
            zone_id (int): Zone id
        """
        zone = await ZoneDAO.get(zone_id)
        if zone:
            updatedZone = await zone.update_from_dict(kwargs)
            await updatedZone.save()
            return updatedZone

    @staticmethod
    async def delete(zone_id: int):
        """
        Delete a specific Zone by its ID.

        Args:
            zone_id (int): Zone id
        """
        zone = await ZoneDAO.get(zone_id)
        if zone:
            await zone.delete()
            return zone

    @staticmethod
    def model_to_json(zone: ZoneModel) -> dict:
        """
        Convert ZoneModel instance to JSON string.

        Args:
            zone (ZoneModel): Zone model

        Returns:
            dict: Model data as JSON key-value datatype
        """
        return zone.to_json()
