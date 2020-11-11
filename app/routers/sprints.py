from fastapi import APIRouter
from fastapi.responses import JSONResponse

from typing import List, Union

from app.schemas.sprints import Sprint, CreateUpdateSprint

from app.functions.sprints import SprintsListHandler, CreateSprintHandler, UpdateSprintHandler, DeleteSprintHandler

from app.exceptions import SprintDoesNotExistsException, SprintTitleDuplicateException

router = APIRouter()


@router.get("/sprints", tags=["sprints"])
async def sprints_list() -> List[Sprint]:

    return await SprintsListHandler().handle()


@router.post("/sprints", tags=["sprints"])
async def create_sprint(model: CreateUpdateSprint) -> Union[Sprint, JSONResponse]:

    try:

        return await CreateSprintHandler().handle(model)

    except SprintTitleDuplicateException:

        return JSONResponse(status_code=400, content={"message": "Title is already taken"})


@router.put("/sprints/{sprint_id}", tags=["sprints"])
async def update_sprint(sprint_id: int, model: CreateUpdateSprint) -> Union[Sprint, JSONResponse]:

    try:

        return await UpdateSprintHandler().handle(sprint_id, model)

    except (SprintTitleDuplicateException, SprintDoesNotExistsException) as e:

        if e == SprintTitleDuplicateException:

            return JSONResponse(status_code=400, content={"message": "Title is already taken"})

        elif e == SprintDoesNotExistsException:

            return JSONResponse(status_code=404, content={"message": "Sprint does not exist"})


@router.delete("/sprints/{sprint_id}", tags=["sprints"])
async def delete_sprint(sprint_id: int) -> Union[None, JSONResponse]:

    try:

        return await DeleteSprintHandler().handle(sprint_id)

    except SprintDoesNotExistsException:

        return JSONResponse(status_code=404, content={"message": "Sprint does not exist"})
