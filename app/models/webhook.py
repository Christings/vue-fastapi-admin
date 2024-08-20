from tortoise import fields

from app.schemas.menus import MenuType

from .base import BaseModel, TimestampMixin
from .enums import MethodType


class Webhook(BaseModel, TimestampMixin):
    project = fields.CharField(max_length=64, unique=True, description="项目名称")
    name = fields.CharField(max_length=64, unique=True, description="webhook名称")
    webhook = fields.CharField(max_length=500, null=True, description="webhook url")
    switch = fields.BooleanField(default=False, description="是否开启", index=True)

    class Meta:
        table = "webhook"