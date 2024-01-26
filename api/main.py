from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.services.clickup import ClickUpServices

from api.db import (
    check_db_connection,
    close_database_connection,
)

from api.routers import clickup_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clickup_router.router)

app.add_event_handler("startup", check_db_connection)
app.add_event_handler("shutdown", close_database_connection)

WEBHOOK_ENDPOINT = "https://5f58-154-160-27-205.ngrok-free.app/clickup/webhook"

@app.on_event("startup")
async def initialize_webhook():
    clickup_accessor = ClickUpServices()
    response = clickup_accessor.get_webhooks()

    webhooks = response["webhooks"]

    webhook_endpoint = WEBHOOK_ENDPOINT
    jesse_webhooks = [item for item in webhooks if item['endpoint'] == webhook_endpoint and item['health']['status'] == 'active' ]
    webhooks_inactive = [item for item in webhooks if item['endpoint'] == webhook_endpoint and item['health']['status'] != 'active' ]

    for item in webhooks_inactive:
        clickup_accessor.delete_webhook(item['id'])

    if len(jesse_webhooks) == 0:
        clickup_accessor.create_webhook()
