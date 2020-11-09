from fastapi import APIRouter

from typing import List

from app.schemas.projects import Project

router = APIRouter()


@router.get("/projects", tags=["projects"])
async def projects_list() -> List[Project]:
    return


@router.post("/projects", tags=["projects"])
async def create_project(model: Project) -> Project:
    return


@router.put("/projects/{project_id}", tags=["projects"])
async def update_project(model: Project) -> Project:
    return


@router.delete("/projects/{project_id}", tags=["projects"])
async def delete_project(project_id: int) -> None:
    return





