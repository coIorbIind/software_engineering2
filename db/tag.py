from sqlalchemy import Column, Integer, String

from db.base import Base


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, name='id', primary_key=True, autoincrement=True, index=True)
    name = Column(String, name='name', nullable=False, index=True, unique=True)
    code = Column(String, name='code', nullable=False, index=True, unique=True)
