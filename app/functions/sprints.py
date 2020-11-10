from typing import List

from app.models.sprints import sprints
from app.schemas.sprints import Sprint, CreateUpdateSprint

from app.exceptions import SprintTitleDuplicateException, SprintDoesNotExistsException

from app.db import database


class SprintsListHandler:

    async def handle(self) -> List[Sprint]:

        return await self._get_sprints()

    async def _get_sprints(self) -> List[Sprint]:

        query = sprints.select()

        return await database.fetch_all(query)


class CreateSprintHandler:

    async def handle(self, model: CreateUpdateSprint) -> Sprint:

        await self._validate(model)

        return await self._create(model)

    async def _validate(self, model: CreateUpdateSprint) -> None:

        async for row in database.iterate(query=sprints.select()):

            if row['title'] == model.title:
                raise SprintTitleDuplicateException('Title is already taken')

    async def _create(self, model: CreateUpdateSprint) -> Sprint:

        query = sprints.insert().values(model.dict())

        sprint_id = await database.execute(query)

        response_model = Sprint(**model.dict(), id=sprint_id)

        return response_model


class UpdateSprintHandler:

    async def handle(self, sprint_id: int, model: CreateUpdateSprint) -> Sprint:

        query = sprints.select().where(sprints.c.id == sprint_id)

        sprint = await database.fetch_one(query=query)

        await self._validate(sprint, model)

        return await self._update(sprint, model)

    async def _validate(self, sprint: Sprint, model: CreateUpdateSprint) -> None:

        if not sprint:

            raise SprintDoesNotExistsException('Sprint does not exists')

        async for row in database.iterate(query=sprints.select()):

            if row['title'] == model.title:
                raise SprintTitleDuplicateException('Title is already taken')

    async def _update(self, sprint: Sprint, model: CreateUpdateSprint) -> Sprint:

        query = sprints.update().where(sprints.c.id == sprint['id']).values(model.dict())

        await database.fetch_one(query=query)

        response_model = Sprint(**model.dict(), id=sprint['id'])

        return response_model


class DeleteSprintHandler:

    async def handle(self, sprint_id: int) -> None:

        query = sprints.select().where(sprints.c.id == sprint_id)

        sprint = await database.fetch_one(query=query)

        await self._validate(sprint)

        return await self._delete(sprint)

    async def _validate(self, sprint: Sprint) -> None:

        if not sprint:

            raise SprintDoesNotExistsException('Sprint does not exists')

    async def _delete(self, sprint: Sprint) -> None:

        query = sprints.delete().where(sprints.c.id == sprint['id'])

        await database.fetch_one(query=query)
