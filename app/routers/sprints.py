from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from typing import List, Union, Optional

from app.schemas.sprints import Sprint, CreateUpdateSprint
from app.schemas.users import User

from app.functions.sprints import SprintsListHandler, CreateSprintHandler, UpdateSprintHandler, DeleteSprintHandler

from app.exceptions import (
    SprintTitleDuplicateException,
    SprintDoesNotExistsException,
    ReferenceProjectDoesNotExistException,
    UnauthorizedAccessException
)

from app.auth import get_current_user

router = APIRouter()


@router.get("/sprints", tags=["sprints"], status_code=200)
async def sprints_list(project_id: Optional[int]) -> List[Sprint]:

    return await SprintsListHandler().handle(project_id)


@router.post("/sprints", tags=["sprints"], status_code=201)
async def create_sprint(model: CreateUpdateSprint, user: User = Depends(get_current_user)) -> Union[Sprint, JSONResponse]:

    try:

        return await CreateSprintHandler().handle(model, user)

    except SprintTitleDuplicateException as e:

        return JSONResponse(status_code=400, content={"message": str(e)})

    except ReferenceProjectDoesNotExistException as e:

        return JSONResponse(status_code=404, content={"message": str(e)})

    except UnauthorizedAccessException as e:

        return JSONResponse(status_code=403, content={"message": str(e)})


@router.put("/sprints/{sprint_id}", tags=["sprints"], status_code=200)
async def update_sprint(
        sprint_id: int,
        model: CreateUpdateSprint,
        user: User = Depends(get_current_user)
) -> Union[Sprint, JSONResponse]:

    try:

        return await UpdateSprintHandler().handle(sprint_id, model, user)

    except SprintTitleDuplicateException as e:

        return JSONResponse(status_code=400, content={"message": str(e)})

    except (SprintDoesNotExistsException, ReferenceProjectDoesNotExistException) as e:

        return JSONResponse(status_code=404, content={"message": str(e)})

    except UnauthorizedAccessException as e:

        return JSONResponse(status_code=403, content={"message": str(e)})


@router.delete("/sprints/{sprint_id}", tags=["sprints"], status_code=200)
async def delete_sprint(sprint_id: int, user: User = Depends(get_current_user)) -> Union[None, JSONResponse]:

    try:

        return await DeleteSprintHandler().handle(sprint_id, user)

    except SprintDoesNotExistsException as e:

        return JSONResponse(status_code=404, content={"message": str(e)})

    except UnauthorizedAccessException as e:

        return JSONResponse(status_code=403, content={"message": str(e)})
