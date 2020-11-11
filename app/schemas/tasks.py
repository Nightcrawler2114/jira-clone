from pydantic import BaseModel, Field, validator

from typing import List

from datetime import datetime

from app.enums import StatusEnum, PriorityEnum


class Attachment(BaseModel):

    id: int
    filename: str
    filepath: str
    task_id: int


class Task(BaseModel):

    id: int
    title: str = Field('task title', max_length=300, description='Task\'s title')
    description: str = Field('', max_length=1000, description='Task\'s description')
    start_date: datetime = Field(
        datetime.now(),
        description='Task start date'
    )
    end_date: datetime = Field(
        datetime.now(),
        description='Task end date'
    )
    status: StatusEnum = Field(
        StatusEnum.todo,
        description='Task\'s status. Choices are todo, progress, review, testing, done'
    )
    priority: PriorityEnum = Field(
        PriorityEnum.medium,
        description='Task\'s priority. Choices are low, lowest, medium, high, highest'
    )
    project_id: int
    sprint_id: int
    creator_id: int
    assignee_id: int
    attachments: List[Attachment] = []

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


class CreateUpdateTask(BaseModel):

    title: str = Field('task title', max_length=300, description='Task\'s title')
    description: str = Field('', max_length=1000, description='Task\'s description')
    start_date: datetime = Field(
        datetime.now(),
        description='Task start date'
    )
    end_date: datetime = Field(
        datetime.now(),
        description='Task end date'
    )
    status: StatusEnum = Field(
        StatusEnum.todo,
        description='Task\'s status. Choices are todo, progress, review, testing, done'
    )
    priority: PriorityEnum = Field(
        PriorityEnum.medium,
        description='Task\'s priority. Choices are low, lowest, medium, high, highest'
    )
    project_id: int
    sprint_id: int
    creator_id: int
    assignee_id: int

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

