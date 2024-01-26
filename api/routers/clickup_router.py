from fastapi import APIRouter, Depends, HTTPException, Request
from api.services.task_activity import TaskActivityService

router = APIRouter(
    prefix="/clickup",
    responses={404: {"description": "Not found"}},
    tags=["clickup"],
)

task_activity_service = TaskActivityService()

# Endpoint to receive webhook events from ClickUp
@router.post("/webhook")
async def clickup_webhook(request: Request):
    print("Received webhook event from ClickUp")

    # Handle the ClickUp task event

    # Log the event to a file
    payload = await request.json()

    await task_activity_service.create_task_activity(payload)

    with open("webhook.log", "a") as f:
        f.write(str(payload) + "\n")

    return {"status": "ok"}
