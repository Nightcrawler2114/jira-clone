import sqlalchemy
import databases

from app.settings import DATABASE_URL


database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)

