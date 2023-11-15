import datetime

from tortoise import fields, models
from tortoise.fields.relational import _NoneAwaitable
from tortoise.queryset import QuerySet


class ZoneSettingModel(models.Model):
    """Model for demo purpose."""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)  # noqa: WPS432
    description = fields.CharField(max_length=255, null=True)
    config = fields.CharField(max_length=255)

    # relationship
    zone = fields.ForeignKeyField("models.ZoneModel", related_name="zone_setting_zone", null=True)

    class Meta:
        table = "ZoneSetting"

    def to_json(self):
        model_data = {}
        for field_name, field_object in self._meta.fields_map.items():
            value = getattr(self, field_name)
            if isinstance(
                field_object,
                (fields.ForeignKeyField.__class__, fields.OneToOneField.__class__),
            ):
                value = value.id if value else None
            elif isinstance(value, datetime.datetime):
                value = int(round(value.timestamp())) if value else None
            elif isinstance(value, (fields.ReverseRelation, _NoneAwaitable)):
                continue
            model_data[field_name] = value
        return {key: value for key, value in model_data.items() if not isinstance(value, QuerySet)}
