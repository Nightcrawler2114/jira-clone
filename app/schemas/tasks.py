from pydantic import BaseModel

from datetime import datetime


class Task(BaseModel):

    id: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    status: str
    priority: str
    project_id: int
    sprint_id: int
    creator_id: int
    assignee_id: int


class Attachment(BaseModel):

    id: int
    filename: str
    filepath: str
    task_id: int
