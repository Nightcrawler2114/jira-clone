from fastapi import APIRouter

from typing import List

from app.schemas.users import User

router = APIRouter()


@router.get("/users", tags=["users"])
async def users_list() -> List[User]:
    return


@router.post("/users", tags=["users"])
async def create_user() -> User:
    return


@router.put("/users/{user_id}", tags=["users"])
async def update_user(user_id: int) -> User:
    return


@router.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: int) -> None:
    return
