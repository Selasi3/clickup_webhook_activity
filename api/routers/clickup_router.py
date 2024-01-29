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

@router.get("/project_activities")
async def get_project_activities(project_name: str = "Levr"):
    try:
        activities = await task_activity_service.get_activities_by_project(project_name)
        return {"success": True, "activities": activities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

