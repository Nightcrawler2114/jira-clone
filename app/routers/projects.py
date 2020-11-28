from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from typing import List, Union

from app.schemas.projects import Project, CreateUpdateProject
from app.schemas.users import User

from app.functions.projects import ProjectsListHandler, CreateProjectHandler, DeleteProjectHandler, UpdateProjectHandler

from app.exceptions import ProjectTitleDuplicateException, ProjectDoesNotExistsException, UnauthorizedAccessException

from app.auth import get_current_user

router = APIRouter()


@router.get("/projects", tags=["projects"], response_model=List[Project], status_code=200)
async def projects_list() -> List[Project]:

    return await ProjectsListHandler().handle()


@router.post("/projects", tags=["projects"], response_model=Project, status_code=201)
async def create_project(
        model: CreateUpdateProject,
        user: User = Depends(get_current_user)
) -> Union[Project, JSONResponse]:

    try:

        return await CreateProjectHandler().handle(model, user)

    except ProjectTitleDuplicateException as e:

        return JSONResponse(status_code=400, content={"message": str(e)})

    except UnauthorizedAccessException as e:

        return JSONResponse(status_code=403, content={"message": str(e)})


@router.put("/projects/{project_id}", tags=["projects"], response_model=Project, status_code=200)
async def update_project(
        project_id: int,
        model: CreateUpdateProject,
        user: User = Depends(get_current_user)
) -> Union[Project, JSONResponse]:

    try:

        return await UpdateProjectHandler().handle(project_id, model, user)

    except ProjectTitleDuplicateException as e:

        return JSONResponse(status_code=400, content={"message": str(e)})

    except ProjectDoesNotExistsException as e:

        return JSONResponse(status_code=404, content={"message": str(e)})

    except UnauthorizedAccessException as e:

        return JSONResponse(status_code=403, content={"message": str(e)})


@router.delete("/projects/{project_id}", tags=["projects"], status_code=200)
async def delete_project(project_id: int, user: User = Depends(get_current_user)) -> Union[None, JSONResponse]:

    try:

        return await DeleteProjectHandler().handle(project_id, user)

    except ProjectDoesNotExistsException as e:

        return JSONResponse(status_code=404, content={"message": str(e)})

    except UnauthorizedAccessException as e:

        return JSONResponse(status_code=403, content={"message": str(e)})





