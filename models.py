from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base, engine


class Order_ORM(Base):
    __tablename__ = "Orders"

    id = Column(Integer, primary_key=True, index=True)
    txid = Column(String)
    coinName = Column(String)
    state = Column(String)
    bizType = Column(String)
    type = Column(String)
    coinType = Column(String)
    to = Column(String)
    value = Column(String)
    sequence = Column(Integer, unique=True)
    confirmations = Column(Integer)
    create_at = Column(Integer)
    update_at = Column(Integer)
    hash = Column(String)
    memo = Column(String)
    
def create_tables():
    Base.metadata.create_all(engine)