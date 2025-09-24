from sqlalchemy import (
    Column, Integer, String, BigInteger
)
from sqlalchemy.orm import relationship
from .base import Base


class Network(Base):
    __tablename__ = 'network'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    network_id = Column(Integer, unique=True, nullable=False)
    rpc_url = Column(String, nullable=False)
    last_checked_block = Column(BigInteger, default=0, nullable=False)
    
    tokens = relationship("Token", back_populates="network")