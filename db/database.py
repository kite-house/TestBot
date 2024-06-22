from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.models import Base
from os import getenv

engine = create_engine(
    url = f'mysql+mysqlconnector://{getenv("DB_USER")}:{getenv("DB_PASSWORD")}@{getenv("DB_HOST")}:{getenv("DB_PORT")}/{getenv("DB_NAME")}',
    echo = False
)

session = sessionmaker(engine)()

Base.metadata.create_all(engine)

def clear_db():
    Base.metadata.drop_all(engine)