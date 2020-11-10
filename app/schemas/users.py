from pydantic import BaseModel


from app.enums import RoleEnum


class User(BaseModel):

    id: int
    name: str
    role: RoleEnum = RoleEnum.user


class CreateUpdateUser(BaseModel):

    name: str
    role: RoleEnum = RoleEnum.user
