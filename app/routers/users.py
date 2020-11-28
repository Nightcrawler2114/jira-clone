from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from typing import List, Union

from app.schemas.users import User, CreateUpdateUser

from app.functions.users import UsersListHandler, CreateUserHandler, UpdateUserHandler, DeleteUserHandler

from app.exceptions import UserDoesNotExistsException, UnauthorizedAccessException

from app.auth import get_current_user

router = APIRouter()


@router.get("/users", tags=["users"], status_code=200)
async def users_list() -> List[User]:

    return await UsersListHandler().handle()


@router.post("/users", tags=["users"], status_code=201)
async def create_user(model: CreateUpdateUser, user: User = Depends(get_current_user)) -> Union[User, JSONResponse]:

    try:

        return await CreateUserHandler().handle(model, user)

    except UnauthorizedAccessException as e:

        return JSONResponse(status_code=403, content={"message": str(e)})


@router.put("/users/{user_id}", tags=["users"], status_code=200)
async def update_user(
        user_id: int,
        model: CreateUpdateUser,
        user: User = Depends(get_current_user)
) -> Union[User, JSONResponse]:

    try:

        return await UpdateUserHandler().handle(user_id, model, user)

    except UserDoesNotExistsException:

        return JSONResponse(status_code=404, content={"message": "User does not exist"})

    except UnauthorizedAccessException as e:

        return JSONResponse(status_code=403, content={"message": str(e)})


@router.delete("/users/{user_id}", tags=["users"], status_code=200)
async def delete_user(user_id: int, user: User = Depends(get_current_user)) -> Union[None, JSONResponse]:

    try:

        return await DeleteUserHandler().handle(user_id, user)

    except UserDoesNotExistsException:

        return JSONResponse(status_code=404, content={"message": "User does not exist"})

    except UnauthorizedAccessException as e:

        return JSONResponse(status_code=403, content={"message": str(e)})
