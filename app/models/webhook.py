from tortoise import fields

from .base import BaseModel, TimestampMixin


class Webhook(BaseModel, TimestampMixin):
    project = fields.CharField(max_length=64, description="项目名称")
    name = fields.CharField(max_length=64, description="webhook名称")
    webhook = fields.CharField(max_length=500, null=True, description="webhook url")
    switch = fields.BooleanField(default=False, description="是否开启", index=True)

    class Meta:
        table = "webhook"