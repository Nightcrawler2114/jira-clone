import sqlalchemy
import databases

# from app.models.projects import projects
# from app.models.sprints import sprints
# from app.models.tasks import tasks, attachments
# from app.models.users import users


DATABASE_URL = "postgres://superuser:superuser@localhost:5433/jira-clone"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)
