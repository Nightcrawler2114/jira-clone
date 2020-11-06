import sqlalchemy

from app.db import metadata


sprints = sqlalchemy.Table(
    "sprints",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("start_date", sqlalchemy.DateTime),
    sqlalchemy.Column("end_date", sqlalchemy.DateTime),
    sqlalchemy.Column("active", sqlalchemy.Boolean),
    sqlalchemy.Column("project_id", sqlalchemy.ForeignKey('projects.id')),
)