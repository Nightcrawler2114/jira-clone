import sqlalchemy

from app.db import metadata

from app.enums import StatusEnum, PriorityEnum


tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("start_date", sqlalchemy.DateTime),
    sqlalchemy.Column("end_date", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.Enum(StatusEnum)),
    sqlalchemy.Column("priority", sqlalchemy.Enum(PriorityEnum)),
    sqlalchemy.Column("project_id", sqlalchemy.ForeignKey('projects.id')),
    sqlalchemy.Column("sprint_id", sqlalchemy.ForeignKey('sprints.id')),
    sqlalchemy.Column("creator_id", sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column("assignee_id", sqlalchemy.ForeignKey('users.id')),
)

attachments = sqlalchemy.Table(
    "attachments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("filename", sqlalchemy.String),
    sqlalchemy.Column("filepath", sqlalchemy.String),
    sqlalchemy.Column("task_id", sqlalchemy.ForeignKey('tasks.id')),
)