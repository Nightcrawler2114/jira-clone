from fastapi import APIRouter

from typing import List

from app.schemas.sprints import Sprint

router = APIRouter()


@router.get("/sprints", tags=["sprints"])
async def sprints_list() -> List[Sprint]:
    return


@router.post("/sprints", tags=["sprints"])
async def create_sprint() -> Sprint:
    return


@router.put("/sprints/{sprint_id}", tags=["sprints"])
async def update_sprint() -> Sprint:
    return


@router.delete("/sprints/{sprint_id}", tags=["sprints"])
async def delete_sprint() -> None:
    return
