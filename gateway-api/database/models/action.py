import datetime

from tortoise import fields, models
from tortoise.fields.relational import _NoneAwaitable
from tortoise.queryset import QuerySet


class ActionModel(models.Model):
    """Tortoise-based log model."""

    # Fields
    id = fields.IntField(
        pk=True,
    )
    percentage = fields.FloatField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Relationship
    camera = fields.OneToOneField("models.ZoneModel", related_name="camera_attendance", null=True)
    face = fields.ForeignKeyField("models.FaceModel", related_name="face_tracking", null=True)
    # event = fields.ForeignKeyField("models.EventModel", related_name="action_event")
    log = fields.ForeignKeyField("models.EventLogModel", "action_log")

    class Meta:
        table = "Action"

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
