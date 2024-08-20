from tortoise.expressions import Q
from tortoise.transactions import atomic

from app.core.crud import CRUDBase
from app.models.webhook import Webhook
from app.schemas.webhook import WebhookCreate, WebhookUpdate


class WebhookController(CRUDBase[Webhook, WebhookCreate, WebhookUpdate]):
    def __init__(self):
        super().__init__(model=Webhook)

    # async def get_by_username(self, username: str) -> Optional[User]:
    #     return await self.model.filter(username=username).first()


    # async def get_webhook_tree(self, project:str):
    #     return await self.model.filter(project=project).all()

    async def get_webhook_info(self):
        pass

    # async def update_webhook_closure(self, obj: Webhook):
    #     parent_webhooks = await WebhookClosure.filter(descendant=obj.parent_id)
    #     for i in parent_webhooks:
    #         print(i.ancestor, i.descendant)
    #     webhook_closure_objs: list[WebhookClosure] = []
    #     # 插入父级关系
    #     for item in parent_webhooks:
    #         webhook_closure_objs.append(WebhookClosure(ancestor=item.ancestor, descendant=obj.id, level=item.level + 1))
    #     # 插入自身x
    #     webhook_closure_objs.append(WebhookClosure(ancestor=obj.id, descendant=obj.id, level=0))
    #     # 创建关系
    #     await WebhookClosure.bulk_create(webhook_closure_objs)

    @atomic()
    async def create_webhook(self, obj_in: WebhookCreate):
        # 创建
        # if obj_in.parent_id != 0:
        #     await self.get(id=obj_in.parent_id)
        # await self.create(obj_in=obj_in)
        obj = await self.create(obj_in=obj_in)
        return obj
        # new_obj = await self.create(obj_in=obj_in)
        # await self.update_webhook_closure(new_obj)

    @atomic()
    async def update_webhook(self, obj_in: WebhookUpdate):
        webhook_obj = await self.get(id=obj_in.id)
        # 更新部门关系
        # if webhook_obj.parent_id != obj_in.parent_id:
        #     await WebhookClosure.filter(ancestor=webhook_obj.id).delete()
        #     await WebhookClosure.filter(descendant=webhook_obj.id).delete()
        #     await self.update_webhook_closure(webhook_obj)
        # 更新部门信息
        webhook_obj.update_from_dict(obj_in.model_dump(exclude_unset=True))
        await webhook_obj.save()

    @atomic()
    async def delete_webhook(self, webhook_id: int):
        # 删除部门
        obj = await self.get(id=webhook_id)
        # obj.is_deleted = True
        # await obj.save()
        # # 删除关系
        # await WebhookClosure.filter(descendant=webhook_id).delete()
        await Webhook.filter(id=obj.id).delete()


webhook_controller = WebhookController()
