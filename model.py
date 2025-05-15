from sqlalchemy import Table, Column, Integer, String
from database import Base


class Transact(Base):
    __tablename__='transactions'
    id = Column('id',Integer,primary_key=True)
    value =Column('value',Integer)
    type = Column('type', String)