from pydantic import BaseModel, Field, validator

from datetime import datetime


class Project(BaseModel):

    id: int
    title: str = Field('project title', max_length=300, description='Project\'s title')
    description: str = Field('', max_length=1000, description='Project\'s description')
    creator_id: int
    start_date: datetime = Field(
        datetime.now(),
        description='Project start date'
    )
    end_date: datetime = Field(
        datetime.now(),
        description='Project end date'
    )


class CreateUpdateProject(BaseModel):

    title: str = Field('project title', max_length=300, description='Project\'s title')
    description: str = Field('', max_length=1000, description='Project\'s description')
    start_date: datetime = Field(
        datetime.now(),
        description='Project start date'
    )
    end_date: datetime = Field(
        datetime.now(),
        description='Project end date'
    )

    @validator('start_date')
    def start_date_must_be_a_future_date(cls, v):
        if v < datetime.now():
            raise ValueError('Start date must be a future date')
        return v

    @validator('end_date')
    def end_date_must_be_a_future_date(cls, v):
        if v < datetime.now():
            raise ValueError('End date must be a future date')
        return v
