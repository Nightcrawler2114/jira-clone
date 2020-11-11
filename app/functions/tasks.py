from typing import List

from sqlalchemy.sql.expression import join
from sqlalchemy.sql import select

from app.models.tasks import tasks, attachments
from app.schemas.tasks import Task, Attachment, CreateUpdateTask

from app.exceptions import TaskTitleDuplicateException, TaskDoesNotExistsException

from app.db import database


class TasksListHandler:

    async def handle(self) -> List[Task]:

        return await self._get_tasks()

    async def _get_tasks(self) -> List[Task]:

        query = tasks.select()

        return await database.fetch_all(query)


class CreateTaskHandler:

    async def handle(self, model: CreateUpdateTask) -> Task:

        await self._validate(model)

        return await self._create(model)

    async def _validate(self, model: CreateUpdateTask) -> None:

        async for row in database.iterate(query=tasks.select()):

            if row['title'] == model.title:
                raise TaskTitleDuplicateException('Title is already taken')

    async def _create(self, model: CreateUpdateTask) -> Task:

        query = tasks.insert().values(model.dict())

        task_id = await database.execute(query)

        response_model = Task(**model.dict(), id=task_id)

        return response_model


class UpdateTaskHandler:

    async def handle(self, task_id: int, model: CreateUpdateTask) -> Task:

        query = tasks.select().where(tasks.c.id == task_id)

        task = await database.fetch_one(query=query)

        await self._validate(task, model)

        return await self._update(task, model)

    async def _validate(self, task: Task, model: CreateUpdateTask) -> None:

        if not task:

            raise TaskDoesNotExistsException('Task does not exists')

        async for row in database.iterate(query=tasks.select()):

            if row['title'] == model.title:
                raise TaskTitleDuplicateException('Title is already taken')

    async def _update(self, task: Task, model: CreateUpdateTask) -> Task:

        query = tasks.update().where(tasks.c.id == task['id']).values(model.dict())

        await database.fetch_one(query=query)

        response_model = Task(**model.dict(), id=task['id'])

        return response_model


class DeleteTaskHandler:

    async def handle(self, task_id: int) -> None:

        query = tasks.select().where(tasks.c.id == task_id)

        task = await database.fetch_one(query=query)

        await self._validate(task)

        return await self._delete(task)

    async def _validate(self, task: Task) -> None:

        if not task:

            raise TaskDoesNotExistsException('Task does not exists')

    async def _delete(self, task: Task) -> None:

        query = tasks.delete().where(tasks.c.id == task['id'])

        await database.fetch_one(query=query)
