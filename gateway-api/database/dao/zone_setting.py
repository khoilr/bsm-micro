from typing import List, Union

from tortoise.exceptions import DoesNotExist

from database.models.zone_setting import ZoneSettingModel


class ZoneSettingDAO:
    @staticmethod
    async def get(zone_setting_id: int) -> Union[ZoneSettingModel, None]:
        """
        Retrieve a specific ZoneSetting by its ID.

        Args:
            zone_setting_id (int): ZoneSetting id

        Returns:
            Union[ZoneSettingModel, None]: ZoneSetting model or None if not found
        """
        try:
            return await ZoneSettingModel.get(id=zone_setting_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_all() -> List[ZoneSettingModel]:
        """
        Retrieve all ZoneSettings.

        Returns:
            List[ZoneSettingModel]: list of zone setting models
        """
        return await ZoneSettingModel.all()

    @staticmethod
    async def filter(**kwargs) -> List[ZoneSettingModel]:
        """
        Filter ZoneSettings based on provided keyword arguments.

        Returns:
            List[ZoneSettingModel]: List of zone setting models
        """
        return await ZoneSettingModel.filter(**kwargs)

    @staticmethod
    async def create(**kwargs) -> ZoneSettingModel:
        """
        Create a new ZoneSetting.

        Args:
            name (str): Name of the setting.
            description (str): Description of the setting.
            config (str): Configuration string.
            zone_id (int, optional): Zone ID. Defaults to None.

        Returns:
            ZoneSettingModel: The created ZoneSetting model.
        """
        zone_setting = await ZoneSettingModel.create(**kwargs)
        return zone_setting

    @staticmethod
    async def update(zone_setting_id: int, **kwargs) -> None:
        """
        Update a specific ZoneSetting using provided keyword arguments.

        Args:
            zone_setting_id (int): ZoneSetting id.
            **kwargs: Arbitrary keyword arguments.
        """
        zone_setting = await ZoneSettingDAO.get(zone_setting_id)
        if zone_setting:
            await zone_setting.update_from_dict(kwargs).save()

    @staticmethod
    async def delete(zone_setting_id: int) -> None:
        """
        Delete a specific ZoneSetting by its ID.

        Args:
            zone_setting_id (int): ZoneSetting id.
        """
        zone_setting = await ZoneSettingDAO.get(zone_setting_id)
        if zone_setting:
            await zone_setting.delete()

    @staticmethod
    def model_to_json(zone_setting: ZoneSettingModel) -> dict:
        """
        Convert ZoneSettingModel instance to JSON string.

        Args:
            zone_setting (ZoneSettingModel): zone setting model

        Returns:
            dict: Model data as JSON key-value datatype
        """
        return zone_setting.to_json()
