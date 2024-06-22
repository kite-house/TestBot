from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Column, Date, Integer, String, Boolean



class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(150), default= False, nullable=False)
    is_superuser = Column(Boolean, default=False)
