from pydantic import BaseModel, Field, validator

from datetime import datetime


class Sprint(BaseModel):

    id: int
    title: str = Field('sprint title', max_length=300, description='Sprint\'s title')
    description: str = Field('', max_length=1000, description='Sprint\'s description')
    start_date: datetime = Field(
        datetime.now(),
        description='Sprint start date'
    )
    end_date: datetime = Field(
        datetime.now(),
        description='Sprint end date'
    )
    active: bool = Field(True, description='Is task active?')
    project_id: int


class CreateUpdateSprint(BaseModel):

    title: str = Field('sprint title', max_length=300, description='Sprint\'s title')
    description: str = Field('', max_length=1000, description='Sprint\'s description')
    start_date: datetime = Field(
        datetime.now(),
        description='Sprint start date'
    )
    end_date: datetime = Field(
        datetime.now(),
        description='Sprint end date'
    )
    active: bool = Field(True, description='Is task active?')
    project_id: int

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
