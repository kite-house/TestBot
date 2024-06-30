from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Column, Date, Integer, String, Boolean, JSON



class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(150), default= False, nullable=False)
    is_superuser = Column(Boolean, default=False)

class Tests(Base):
    __tablename__ = 'Tests'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), default= False, nullable= False)
    questions = Column(JSON)
    creation = Column(String(150), default= False, nullable= False)
    date_created = Column(Date, default= False, nullable= False)