from typing import List

from app.models.projects import projects
from app.schemas.projects import CreateUpdateProject, Project

from app.exceptions import ProjectTitleDuplicateException, ProjectDoesNotExistsException

from app.db import database


class ProjectsListHandler:

    async def handle(self) -> List[Project]:

        return await self._get_projects()

    async def _get_projects(self) -> List[Project]:

        query = projects.select()

        return await database.fetch_all(query)


class CreateProjectHandler:

    async def handle(self, model: CreateUpdateProject) -> Project:

        await self._validate(model)

        return await self._create(model)

    async def _validate(self, model: CreateUpdateProject) -> None:

        async for row in database.iterate(query=projects.select()):

            if row['title'] == model.title:
                raise ProjectTitleDuplicateException('Title is already taken')

    async def _create(self, model: CreateUpdateProject) -> Project:

        query = projects.insert().values(model.dict())

        project_id = await database.execute(query)

        response_model = Project(**model.dict(), id=project_id)

        return response_model


class UpdateProjectHandler:

    async def handle(self, project_id: int, model: CreateUpdateProject) -> Project:

        query = projects.select().where(projects.c.id == project_id)

        project = await database.fetch_one(query=query)

        await self._validate(project, model)

        return await self._update(project, model)

    async def _validate(self, project: Project, model: CreateUpdateProject) -> None:

        if not project:

            raise ProjectDoesNotExistsException('Project does not exist')

        async for row in database.iterate(query=projects.select()):

            if row['title'] == model.title:
                raise ProjectTitleDuplicateException('Title is already taken')

    async def _update(self, project: Project, model: CreateUpdateProject) -> Project:

        query = projects.update().where(projects.c.id == project['id']).values(model.dict())

        await database.fetch_one(query=query)

        response_model = Project(**model.dict(), id=project['id'])

        return response_model


class DeleteProjectHandler:

    async def handle(self, project_id: int) -> None:

        query = projects.select().where(projects.c.id == project_id)

        project = await database.fetch_one(query=query)

        await self._validate(project)

        return await self._delete(project)

    async def _validate(self, project: Project) -> None:

        if not project:

            raise ProjectDoesNotExistsException('Project does not exists')

    async def _delete(self, project: Project) -> None:

        query = projects.delete().where(projects.c.id == project['id'])

        await database.fetch_one(query=query)


