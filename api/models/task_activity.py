from datetime import datetime
from pydantic import BaseModel, Field
from typing import List


class TaskActivity(BaseModel):
    update_by: str
    date: datetime = Field(description="Field for knowing the date the update occurred")
    update: dict
    event: str

class TaskHistory(BaseModel):
    task_id: str = Field(False, description="Relating to the current task id", unique=True)
    last_updated: datetime = Field(description="Field for knowing the expiration of a prompt")
    activities: List[TaskActivity]
    current: dict
