import datetime

from tortoise import fields, models
from tortoise.fields.relational import _NoneAwaitable
from tortoise.queryset import QuerySet


class PersonModel(models.Model):
    """Tortoise-based log model."""

    # Fields
    person_id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=True)
    gender = fields.IntField(null=True)
    dob = fields.DatetimeField(null=True)
    phone = fields.CharField(max_length=15, null=True)
    avatar_url = fields.CharField(max_length=255, null=True)
    position = fields.CharField(max_length=255, null=True)
    # auto zone
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "Person"

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
