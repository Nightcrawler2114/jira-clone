from fastapi import APIRouter

from typing import List

from app.schemas.projects import Project, CreateUpdateProject

from app.functions.projects import ProjectsListHandler, CreateProjectHandler, DeleteProjectHandler, UpdateProjectHandler

router = APIRouter()


@router.get("/projects", tags=["projects"])
async def projects_list() -> List[Project]:

    return await ProjectsListHandler().handle()


@router.post("/projects", tags=["projects"])
async def create_project(model: CreateUpdateProject) -> Project:

    return await CreateProjectHandler().handle(model)


@router.put("/projects/{project_id}", tags=["projects"])
async def update_project(project_id: int, model: CreateUpdateProject) -> Project:

    return await UpdateProjectHandler().handle(project_id, model)


@router.delete("/projects/{project_id}", tags=["projects"])
async def delete_project(project_id: int) -> None:

    return await DeleteProjectHandler().handle(project_id)





