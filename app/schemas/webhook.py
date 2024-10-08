from pydantic import BaseModel, Field


class BaseWebhook(BaseModel):
    project: str = Field(..., description="项目名称", example="Teamhub")
    name: str = Field(..., description="webhook名称", example="apifox")
    webhook: str = Field("", description="webhook", example="webhook url")
    switch: bool = Field(default=1, description="webhook",
                         example="webhook url")


class WebhookCreate(BaseWebhook):
    ...


class WebhookUpdate(BaseWebhook):
    id: int

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})


class BaseWebhookTest(BaseModel):
    webhook_id: int = Field(..., description="webhook id")
    project: str = Field(..., description="项目名称", example="Teamhub")
    name: str = Field(..., description="webhook名称", example="apifox")
    ret: str = Field(..., description="结果")


class WebhookTestCreate(BaseWebhookTest):
    pass


class WebhookTestUpdate(BaseWebhookTest):
    id: int

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})
