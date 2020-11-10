from fastapi import APIRouter

from typing import List

from app.schemas.sprints import Sprint, CreateUpdateSprint

from app.functions.sprints import SprintsListHandler, CreateSprintHandler, UpdateSprintHandler, DeleteSprintHandler

router = APIRouter()


@router.get("/sprints", tags=["sprints"])
async def sprints_list() -> List[Sprint]:

    return await SprintsListHandler().handle()


@router.post("/sprints", tags=["sprints"])
async def create_sprint(model: CreateUpdateSprint) -> Sprint:

    return await CreateSprintHandler().handle(model)


@router.put("/sprints/{sprint_id}", tags=["sprints"])
async def update_sprint(sprint_id: int, model: CreateUpdateSprint) -> Sprint:

    return await UpdateSprintHandler().handle(sprint_id, model)


@router.delete("/sprints/{sprint_id}", tags=["sprints"])
async def delete_sprint(sprint_id: int) -> None:

    return await DeleteSprintHandler().handle(sprint_id)
