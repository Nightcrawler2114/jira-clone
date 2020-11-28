from typing import List

from app.models.users import users
from app.schemas.users import CreateUpdateUser, User

from app.exceptions import UserDoesNotExistsException, UnauthorizedAccessException

from app.enums import RoleEnum

from app.db import database


class UsersListHandler:

    async def handle(self) -> List[User]:

        return await self._get_users()

    async def _get_users(self) -> List[User]:

        query = users.select()

        return await database.fetch_all(query)


class CreateUserHandler:

    async def handle(self, model: CreateUpdateUser, user: User) -> User:

        await self._validate(user)

        return await self._create(model)

    async def _validate(self, user: User):

        if user['role'] == RoleEnum.user or user['role'] == RoleEnum.product_owner:

            raise UnauthorizedAccessException('You do not have enough rights')

    async def _create(self, model: CreateUpdateUser) -> User:

        query = users.insert().values(model.dict())

        user_id = await database.execute(query)

        response_model = User(**model.dict(), id=user_id)

        return response_model


class UpdateUserHandler:

    async def handle(self, user_id: int, model: CreateUpdateUser, user: User) -> User:

        query = users.select().where(users.c.id == user_id)

        db_user = await database.fetch_one(query=query)

        await self._validate(db_user, user)

        return await self._update(db_user, model)

    async def _validate(self, model: User, user: User) -> None:

        if user['role'] == RoleEnum.user or user['role'] == RoleEnum.product_owner:

            raise UnauthorizedAccessException('You do not have enough rights')

        if not model:

            raise UserDoesNotExistsException('User does not exists')

    async def _update(self, user: User, model: CreateUpdateUser) -> User:

        query = users.update().where(users.c.id == user['id']).values(model.dict())

        await database.fetch_one(query=query)

        response_model = User(**model.dict(), id=user['id'])

        return response_model


class DeleteUserHandler:

    async def handle(self, user_id: int, user: User) -> None:

        query = users.select().where(users.c.id == user_id)

        db_user = await database.fetch_one(query=query)

        await self._validate(db_user, user)

        return await self._delete(user)

    async def _validate(self, model: User, user: User) -> None:

        if user['role'] == RoleEnum.user or user['role'] == RoleEnum.product_owner:

            raise UnauthorizedAccessException('You do not have enough rights')

        if not model:

            raise UserDoesNotExistsException('User does not exists')

    async def _delete(self, user: User) -> None:

        query = users.delete().where(users.c.id == user['id'])

        await database.fetch_one(query=query)
