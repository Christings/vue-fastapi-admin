import json

from fastapi import APIRouter, Query, Path, Request

from app.controllers.webhook import webhook_controller, webhook_test_controller
from app.log import logger
from app.schemas import Success, SuccessExtra, Fail
from app.schemas.webhook import *

from tortoise.expressions import Q

import httpx

router = APIRouter()


@router.get("/list", summary="查看Webhook列表")
async def list_webhook(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    project: str = Query(None, description="Webhook名称"),

):
    q = Q()
    if project:
        q &= Q(project__contains=project)

    total, webhook_objs = await webhook_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict(m2m=True) for obj in webhook_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看Webhook")
async def get_webhook(
    id: int = Query(..., description="WebhookID"),
):
    webhook_obj = await webhook_controller.get(id=id)
    data = await webhook_obj.to_dict()
    return Success(data=data)


@router.post("/create", summary="创建Webhook")
async def create_webhook(
    webhook_in: WebhookCreate,
):
    await webhook_controller.create_webhook(obj_in=webhook_in)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新Webhook")
async def update_webhook(
    webhook_in: WebhookUpdate,
):
    await webhook_controller.update_webhook(obj_in=webhook_in)
    return Success(msg="Update Successfully")


@router.delete("/delete", summary="删除Webhook")
async def delete_webhook(
    webhook_id: int = Query(..., description="WebhookID"),
):
    await webhook_controller.delete_webhook(webhook_id=webhook_id)
    return Success(msg="Deleted Success")


@router.post("/{project}/{name}", summary="监听Webhook")
async def listen_webhook(
    request: Request,
    project: str = Path(description="项目名称"),
    name: str = Path(description="webhook名称"),
):
    params = await request.body()
    logger.info(
        f"Listen Webhook: body={params}, project={project}, name={name}")
    q = Q()
    if project:
        q &= Q(project=project)
    if name:
        q &= Q(name=name)

    webhook_objs = await webhook_controller.get_by_uk(search=q)
    data = [await obj.to_dict(m2m=True) for obj in webhook_objs]

    message = {
        "attachments": [
            {
                "fallback": "test",
                "color": "#FF8000",
                # "pretext": "This is noma project.",
                # "author_name": "Mattermost",
                # "author_icon": "https://mattermost.com/wp-content/uploads/2022/02/icon_WS.png",
                # "author_link": "https://mattermost.org/",
                # "title": text["event"]+":"+text["title"],
            }
        ]
    }

    if name == "apifox":
        params = json.loads(params)
        content = params.get("content", None)
        if not content:
            return Fail(msg="The data passed by apifox is empty")

        content = content.split("\n")
        fields = []
        for i in content:
            fields.append({"short": False, "title": i, "value": ""})

        if fields:
            message["attachments"][0]["fields"] = fields

        event = params.get("event", None)
        title = params.get("title", None)
        if event and title:
            message["attachments"][0]["tile"] = event+":"+title
        elif event and not title:
            message["attachments"][0]["tile"] = event
        elif not event and title:
            message["attachments"][0]["tile"] = title

    elif name == "metersphere":
        if isinstance(params, bytes):
            params = params.decode("utf-8")
            message["attachments"][0]["title"] = params
        else:
            message["attachments"][0]["title"] = str(params)
    else:
        if params:
            if isinstance(params, bytes):
                params = params.decode("utf-8")
            message["attachments"][0]["title"] = str(params)

    logger.info(f"Listen Webhook: message={message}")
    for i in data:
        if i["project"] == project:
            webhook_test_obj = WebhookTestCreate(
                webhook_id=i["id"], project=i["project"], name=i["name"], ret=str(params))
            await webhook_test_controller.create_webhook_test(webhook_test_obj)

            url = i["webhook"]
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=message)
                return Success(msg="Listen Successfully", data=resp.text)

    return Success(msg="Listen Successfully", data=None)


@router.get("/test/list", summary="查看Webhook测试结果列表")
async def list_webhook_test(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    webhook_id: str = Query(None, description="Webhook id"),

):
    q = Q()
    if webhook_id:
        q &= Q(webhook_id__contains=webhook_id)

    total, webhook_test_objs = await webhook_test_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict(m2m=True) for obj in webhook_test_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)
