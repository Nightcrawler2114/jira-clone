import sqlalchemy

from app.db import metadata

from app.enums import RoleEnum


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("role", sqlalchemy.Enum(RoleEnum)),
)