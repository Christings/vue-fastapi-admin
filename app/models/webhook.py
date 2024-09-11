from tortoise import fields

from .base import BaseModel, TimestampMixin


class Webhook(BaseModel, TimestampMixin):
    project = fields.CharField(max_length=64, description="项目名称", index=True)
    name = fields.CharField(max_length=64, description="webhook名称", index=True)
    webhook = fields.CharField(
        max_length=500, null=True, description="webhook url")
    switch = fields.BooleanField(default=False, description="是否开启")

    class Meta:
        table = "webhook"
        unique_together = (('project', 'name'),)


class WebhookTest(BaseModel, TimestampMixin):
    webhook_id = fields.BigIntField(description="部门ID", index=True)
    project = fields.CharField(max_length=64, description="项目名称", index=True)
    name = fields.CharField(max_length=64, description="webhook名称", index=True)
    ret = fields.TextField(description="结果")

    class Meta:
        table = "webhook_test"
