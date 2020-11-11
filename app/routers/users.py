from fastapi import APIRouter
from fastapi.responses import JSONResponse

from typing import List, Union

from app.schemas.users import User, CreateUpdateUser

from app.functions.users import UsersListHandler, CreateUserHandler, UpdateUserHandler, DeleteUserHandler

from app.exceptions import UserDoesNotExistsException

router = APIRouter()


@router.get("/users", tags=["users"])
async def users_list() -> List[User]:

    return await UsersListHandler().handle()


@router.post("/users", tags=["users"])
async def create_user(model: CreateUpdateUser) -> User:

    return await CreateUserHandler().handle(model)


@router.put("/users/{user_id}", tags=["users"])
async def update_user(user_id: int, model: CreateUpdateUser) -> Union[User, JSONResponse]:

    try:

        return await UpdateUserHandler().handle(user_id, model)

    except UserDoesNotExistsException:

        return JSONResponse(status_code=404, content={"message": "User does not exist"})


@router.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: int) -> Union[None, JSONResponse]:

    try:

        return await DeleteUserHandler().handle(user_id)

    except UserDoesNotExistsException:

        return JSONResponse(status_code=404, content={"message": "User does not exist"})
