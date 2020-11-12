from typing import List


from app.models.tasks import tasks, attachments
from app.models.projects import projects
from app.models.users import users

from app.schemas.tasks import Task, Attachment, CreateUpdateTask, CreateAttachment

from app.exceptions import (
    TaskTitleDuplicateException,
    TaskDoesNotExistsException,
    ReferenceProjectDoesNotExistException,
    ReferenceUserDoesNotExistException,
    AttachmentDoesNotExistException
)

from app.db import database


class TasksListHandler:

    async def handle(self) -> List[Task]:

        return await self._get_tasks()

    async def _get_tasks(self) -> List[Task]:

        tasks_list = []

        tasks_query = tasks.select()
        tasks_result = await database.fetch_all(tasks_query)

        for result in tasks_result:

            result = dict(result)

            attachments_list = []

            attachment_query = attachments.select().where(result['id'] == attachments.c.task_id)
            attachment_result = await database.fetch_all(attachment_query)

            for result_ in attachment_result:
                attachments_list.append(result_)

            result['attachments'] = attachments_list

            tasks_list.append(result)

        return tasks_list


class CreateTaskHandler:

    async def handle(self, model: CreateUpdateTask) -> Task:

        await self._validate(model)

        return await self._create(model)

    async def _validate(self, model: CreateUpdateTask) -> None:

        async for row in database.iterate(query=tasks.select()):

            if row['title'] == model.title:
                raise TaskTitleDuplicateException('Title is already taken')

        if not await database.fetch_one(projects.select().where(projects.c.id == model.project_id)):

            raise ReferenceProjectDoesNotExistException('Reference project does not exist')

        if (
                not await database.fetch_one(users.select().where(users.c.id == model.creator_id)) or
                not await database.fetch_one(users.select().where(users.c.id == model.assignee_id))
        ):

            raise ReferenceUserDoesNotExistException('Reference user does not exist')

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

        if not await database.fetch_one(projects.select().where(projects.c.id == model.project_id)):

            raise ReferenceProjectDoesNotExistException('Reference project does not exist')

        if (
                not await database.fetch_one(users.select().where(users.c.id == model.creator_id)) or
                not await database.fetch_one(users.select().where(users.c.id == model.assignee_id))
        ):

            raise ReferenceUserDoesNotExistException('Reference user does not exist')

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


class CreateAttachmentHandler:

    async def handle(self, model: CreateAttachment) -> Attachment:

        await self._validate(model)

        return await self._create(model)

    async def validate(self, model: CreateAttachment) -> None:

        if not database.fetch_one(tasks.select().where(tasks.c.id == model.task_id)):

            raise TaskDoesNotExistsException('Task does not exists')

    async def _create(self, model: CreateAttachment) -> Attachment:

        query = attachments.insert().values(model.dict())

        attachment_id = await database.execute(query)

        response_model = Attachment(**model.dict(), id=attachment_id)

        return response_model


class DeleteAttachmentHandler:

    async def handle(self, attachment_id: int) -> None:

        query = attachments.select().where(attachments.c.id == attachment_id)

        attachment = await database.fetch_one(query=query)

        await self._validate(attachment)

        return await self._delete(attachment)

    async def _validate(self, attachment: Attachment) -> None:

        if not attachment:

            raise AttachmentDoesNotExistException('Sprint does not exists')

    async def _delete(self, attachment: Attachment) -> None:

        query = attachments.delete().where(attachments.c.id == attachment['id'])

        await database.fetch_one(query=query)
