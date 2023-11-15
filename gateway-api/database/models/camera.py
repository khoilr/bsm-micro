import datetime

from tortoise import fields, models
from tortoise.fields.relational import _NoneAwaitable
from tortoise.queryset import QuerySet


class CameraModel(models.Model):
    """Tortoise-based camera model."""

    # Fields
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=True)
    description = fields.CharField(max_length=256, null=True)
    connect_uri = fields.CharField(max_length=256, null=True)
    placeholder_url = fields.CharField(max_length=255, null=True)

    # type like socket, stream, ezviz,...
    type = fields.IntField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Relationship
    zone = fields.ForeignKeyField("models.ZoneModel", null=True)

    # user = fields.ReverseRelation["models.UserModel"]

    class Meta:
        table = "Camera"

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
