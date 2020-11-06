from pydantic import BaseModel

from datetime import datetime


class Sprint(BaseModel):

    id: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    active: bool
    project_id: int
