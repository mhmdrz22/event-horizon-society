from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer

@as_declarative()
class Base:
    """Base class which provides automated table name
    and surrogate primary key column.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s" #  e.g. User -> users

    id = Column(Integer, primary_key=True, index=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

# This file will also be used to ensure all models are imported before Base is used.
# For now, it's just the Base class definition. We'll add model imports here later.
