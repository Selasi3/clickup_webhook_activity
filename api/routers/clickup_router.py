from fastapi import APIRouter, Depends, HTTPException, Request

router = APIRouter(
    prefix="/clickup",
    responses={404: {"description": "Not found"}},
    tags=["clickup"],
)


# Endpoint to receive webhook events from ClickUp
@router.post("/webhook")
async def clickup_webhook(request: Request):
    print("Received webhook event from ClickUp")

    # Handle the ClickUp task event

    # Log the event to a file
    payload = await request.json()

    with open("webhook.log", "a") as f:
        f.write(str(payload) + "\n")

    return {"status": "ok"}
