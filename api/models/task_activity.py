
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List


class Task(BaseModel):
    update_by: str
    date: datetime = Field(description="Field for knowing the date the update occurred")
    update: dict
    event: str

class Activity(BaseModel):
    task_id: str = Field(False, description="Relating to the current task id", unique=True)
    last_updated: datetime = Field(description="Field for knowing the expiration of a prompt")
    activities: List[TaskActivity]
    current: dict
