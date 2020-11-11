from fastapi import APIRouter
from fastapi.responses import JSONResponse

from typing import List, Union

from app.schemas.projects import Project, CreateUpdateProject

from app.functions.projects import ProjectsListHandler, CreateProjectHandler, DeleteProjectHandler, UpdateProjectHandler

from app.exceptions import ProjectTitleDuplicateException, ProjectDoesNotExistsException

router = APIRouter()


@router.get("/projects", tags=["projects"], response_model=List[Project])
async def projects_list() -> List[Project]:

    return await ProjectsListHandler().handle()


@router.post("/projects", tags=["projects"], response_model=Project)
async def create_project(model: CreateUpdateProject) -> Union[Project, JSONResponse]:

    try:

        return await CreateProjectHandler().handle(model)
    except ProjectTitleDuplicateException:

        return JSONResponse(status_code=400, content={"message": "Title is already taken"})


@router.put("/projects/{project_id}", tags=["projects"], response_model=Project)
async def update_project(project_id: int, model: CreateUpdateProject) -> Union[Project, JSONResponse]:

    try:

        return await UpdateProjectHandler().handle(project_id, model)

    except (ProjectTitleDuplicateException, ProjectDoesNotExistsException) as e:

        if e == ProjectTitleDuplicateException:

            return JSONResponse(status_code=400, content={"message": "Title is already taken"})

        elif e == ProjectDoesNotExistsException:

            return JSONResponse(status_code=404, content={"message": "Project does not exist"})


@router.delete("/projects/{project_id}", tags=["projects"])
async def delete_project(project_id: int) -> Union[None, JSONResponse]:

    try:

        return await DeleteProjectHandler().handle(project_id)

    except ProjectDoesNotExistsException:

        return JSONResponse(status_code=404, content={"message": "Project does not exist"})





