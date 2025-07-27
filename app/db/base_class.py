from sqlalchemy import Column, Integer
from app.database import Base

class CustomBase(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
