import sqlalchemy
import databases


DATABASE_URL = "postgres://superuser:superuser@localhost:5433/jira-clone"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)

# metadata.create_all(engine)
