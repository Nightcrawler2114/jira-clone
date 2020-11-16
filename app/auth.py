import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.db import database
from app.models.users import users

from app.schemas.users import User

security = HTTPBasic()


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:

    async for row in database.iterate(query=users.select()):

        if row['username'] == credentials.username:

            user = row
        else:

            user = None

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with such name does not exists",
            headers={"WWW-Authenticate": "Basic"},
        )

    correct_password = secrets.compare_digest(credentials.password, user['password'])

    if not correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user
