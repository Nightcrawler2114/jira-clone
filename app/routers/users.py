from fastapi import APIRouter

from typing import List

from app.schemas.users import User, CreateUpdateUser

from app.functions.users import UsersListHandler, CreateUserHandler, UpdateUserHandler, DeleteUserHandler

router = APIRouter()


@router.get("/users", tags=["users"])
async def users_list() -> List[User]:

    return await UsersListHandler().handle()


@router.post("/users", tags=["users"])
async def create_user(model: CreateUpdateUser) -> User:

    return await CreateUserHandler().handle(model)


@router.put("/users/{user_id}", tags=["users"])
async def update_user(user_id: int, model: CreateUpdateUser) -> User:

    return await UpdateUserHandler().handle(user_id, model)


@router.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: int) -> None:

    return await DeleteUserHandler().handle(user_id)
