from typing import List, Optional

from app.models.sprints import sprints
from app.models.projects import projects

from app.schemas.sprints import Sprint, CreateUpdateSprint
from app.schemas.users import User

from app.exceptions import (
    SprintTitleDuplicateException,
    SprintDoesNotExistsException,
    ReferenceProjectDoesNotExistException,
    UnauthorizedAccessException
)

from app.enums import RoleEnum

from app.db import database


class SprintsListHandler:

    async def handle(self, project_id: Optional[int]) -> List[Sprint]:

        return await self._get_sprints(project_id)

    async def _get_sprints(self, project_id: Optional[int]) -> List[Sprint]:

        if project_id:

            query = sprints.select().where(sprints.c.id == project_id)

        else:

            query = sprints.select()

        return await database.fetch_all(query)


class CreateSprintHandler:

    async def handle(self, model: CreateUpdateSprint, user: User) -> Sprint:

        await self._validate(model, user)

        return await self._create(model)

    async def _validate(self, model: CreateUpdateSprint, user: User) -> None:

        if user['role'] == RoleEnum.user:

            raise UnauthorizedAccessException('You do not have enough rights')

        async for row in database.iterate(query=sprints.select()):

            if row['title'] == model.title:
                raise SprintTitleDuplicateException('Title is already taken')

        if not await database.fetch_one(projects.select().where(projects.c.id == model.project_id)):

            raise ReferenceProjectDoesNotExistException('Reference project does not exist')

    async def _create(self, model: CreateUpdateSprint) -> Sprint:

        query = sprints.insert().values(model.dict())

        sprint_id = await database.execute(query)

        response_model = Sprint(**model.dict(), id=sprint_id)

        return response_model


class UpdateSprintHandler:

    async def handle(self, sprint_id: int, model: CreateUpdateSprint, user: User) -> Sprint:

        query = sprints.select().where(sprints.c.id == sprint_id)

        sprint = await database.fetch_one(query=query)

        await self._validate(sprint, model, user)

        return await self._update(sprint, model)

    async def _validate(self, sprint: Sprint, model: CreateUpdateSprint, user: User) -> None:

        if not sprint:

            raise SprintDoesNotExistsException('Sprint does not exists')

        if user['role'] == RoleEnum.user:

            raise UnauthorizedAccessException('You do not have enough rights')

        async for row in database.iterate(query=sprints.select()):

            if row['title'] == model.title:
                raise SprintTitleDuplicateException('Title is already taken')

        if not await database.fetch_one(projects.select().where(projects.c.id == model.project_id)):

            raise ReferenceProjectDoesNotExistException('Reference project does not exist')

    async def _update(self, sprint: Sprint, model: CreateUpdateSprint) -> Sprint:

        query = sprints.update().where(sprints.c.id == sprint['id']).values(model.dict())

        await database.fetch_one(query=query)

        response_model = Sprint(**model.dict(), id=sprint['id'])

        return response_model


class DeleteSprintHandler:

    async def handle(self, sprint_id: int, user: User) -> None:

        query = sprints.select().where(sprints.c.id == sprint_id)

        sprint = await database.fetch_one(query=query)

        await self._validate(sprint, user)

        return await self._delete(sprint)

    async def _validate(self, sprint: Sprint, user: User) -> None:

        if not sprint:

            raise SprintDoesNotExistsException('Sprint does not exists')

        if user['role'] == RoleEnum.user:

            raise UnauthorizedAccessException('You do not have enough rights')

    async def _delete(self, sprint: Sprint) -> None:

        query = sprints.delete().where(sprints.c.id == sprint['id'])

        await database.fetch_one(query=query)
