from tortoise.expressions import Q
from tortoise.transactions import atomic

from app.core.crud import CRUDBase
from app.models.webhook import Webhook, WebhookTest
from app.schemas.webhook import WebhookCreate, WebhookUpdate, WebhookTestCreate, WebhookTestUpdate


class WebhookController(CRUDBase[Webhook, WebhookCreate, WebhookUpdate]):
    def __init__(self):
        super().__init__(model=Webhook)

    async def get_webhook_info(self):
        pass

    @atomic()
    async def create_webhook(self, obj_in: WebhookCreate):
        # 创建webhook
        obj = await self.create(obj_in=obj_in)
        return obj

    @atomic()
    async def update_webhook(self, obj_in: WebhookUpdate):
        webhook_obj = await self.get(id=obj_in.id)
        # 更新webhook
        webhook_obj.update_from_dict(obj_in.model_dump(exclude_unset=True))
        await webhook_obj.save()

    @atomic()
    async def delete_webhook(self, webhook_id: int):
        # 删除webhook
        obj = await self.get(id=webhook_id)
        await Webhook.filter(id=obj.id).delete()


class WebhookTestController(CRUDBase[WebhookTest, WebhookTestCreate, WebhookTestUpdate]):
    def __init__(self):
        super().__init__(model=WebhookTest)

    async def get_webhook_info(self):
        pass

    @atomic()
    async def create_webhook_test(self, obj_in: WebhookTestCreate):
        # 创建webhook_test
        obj = await self.create(obj_in=obj_in)
        return obj


webhook_controller = WebhookController()
webhook_test_controller = WebhookTestController()
