import datetime
import io
import os
import uuid
from io import IOBase

from tortoise import fields, models
from tortoise.fields import TextField
from tortoise.fields.relational import _NoneAwaitable
from tortoise.queryset import QuerySet


class FaceModel(models.Model):
    """Tortoise-based log model."""

    # Fields
    face_id = fields.IntField(pk=True)
    FrameFilePath = fields.TextField(null=True)
    X = fields.FloatField(null=True)
    Y = fields.FloatField(null=True)
    Width = fields.IntField(null=True)
    Height = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # relationship
    person = fields.ForeignKeyField("models.PersonModel", related_name="person_model", null=True)

    class Meta:
        table = "Face"

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
