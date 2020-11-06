from pydantic import BaseModel

from datetime import datetime


class Project(BaseModel):

    id: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
