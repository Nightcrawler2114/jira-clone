from typing import List

from app.models.users import users
from app.schemas.users import CreateUpdateUser, User

from app.exceptions import UserDoesNotExistsException

from app.db import database


class UsersListHandler:

    async def handle(self) -> List[User]:

        return await self._get_users()

    async def _get_users(self) -> List[User]:

        query = users.select()

        return await database.fetch_all(query)


class CreateUserHandler:

    async def handle(self, model: CreateUpdateUser) -> User:

        return await self._create(model)

    async def _create(self, model: CreateUpdateUser) -> User:

        query = users.insert().values(model.dict())

        user_id = await database.execute(query)

        response_model = User(**model.dict(), id=user_id)

        return response_model


class UpdateUserHandler:

    async def handle(self, user_id: int, model: CreateUpdateUser) -> User:

        query = users.select().where(users.c.id == user_id)

        user = await database.fetch_one(query=query)

        await self._validate(user)

        return await self._update(user, model)

    async def _validate(self, user: User) -> None:

        if not user:

            raise UserDoesNotExistsException('User does not exists')

    async def _update(self, user: User, model: CreateUpdateUser) -> User:

        query = users.update().where(users.c.id == user['id']).values(model.dict())

        await database.fetch_one(query=query)

        response_model = User(**model.dict(), id=user['id'])

        return response_model


class DeleteUserHandler:

    async def handle(self, user_id: int) -> None:

        query = users.select().where(users.c.id == user_id)

        user = await database.fetch_one(query=query)

        await self._validate(user)

        return await self._delete(user)

    async def _validate(self, user: User) -> None:

        if not user:

            raise UserDoesNotExistsException('User does not exists')

    async def _delete(self, user: User) -> None:

        query = users.delete().where(users.c.id == user['id'])

        await database.fetch_one(query=query)
