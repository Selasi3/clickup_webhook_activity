from fastapi import APIRouter, Depends, HTTPException, Request
from api.services.task_activity import TaskActivityService
from api.services.clickup import ClickUpServices

router = APIRouter(
    prefix="/clickup",
    responses={404: {"description": "Not found"}},
    tags=["clickup"],
)

task_activity_service = TaskActivityService()
clickup_accessor = ClickUpServices()

# Endpoint to receive webhook events from ClickUp
@router.post("/webhook")
async def clickup_webhook(request: Request):
    print("Received webhook event from ClickUp")

    # Log the event to a file
    payload = await request.json()

    await task_activity_service.create_task_activity(payload)


@router.get("/project_activities")
async def get_project_activities(project_name: str = "Levr"):
    try:
        activities = await task_activity_service.get_activities_by_project(project_name)
        return {"success": True, "activities": activities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create_webhook")
async def create_webhook():
    try:
        response = clickup_accessor.create_webhook()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/get_webhooks")
async def get_webhooks():
    try:
        webhooks = clickup_accessor.get_webhooks()
        return webhooks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
