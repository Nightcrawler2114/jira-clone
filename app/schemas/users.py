from pydantic import BaseModel, Field


from app.enums import RoleEnum


class User(BaseModel):

    id: int
    name: str = Field('name', max_length=300, description='User\'s name')
    role: RoleEnum = Field(RoleEnum.user, description='User\'s role. Choices are admin, user')
    username: str = Field('username', max_length=300, description='User\'s username')
    password: str = Field('password', max_length=300, description='User\'s password')


class CreateUpdateUser(BaseModel):

    name: str = Field('name', max_length=300, description='User\'s name')
    role: RoleEnum = Field(RoleEnum.user, description='User\'s role. Choices are admin, user')
    username: str = Field('username', max_length=300, description='User\'s username')
    password: str = Field('password', max_length=300, description='User\'s password')