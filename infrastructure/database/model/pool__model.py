from sqlalchemy import (
    Column, Integer, ForeignKey
)
from sqlalchemy.orm import relationship
from .base import Base


class Pool(Base):
    __tablename__ = 'pool'
    
    id = Column(Integer, primary_key=True)
    fee = Column(Integer, nullable=False)
    first_token_id = Column(Integer, ForeignKey('token.id'), nullable=False)
    second_token_id = Column(Integer, ForeignKey('token.id'), nullable=False)
    
    first_token = relationship("Token", foreign_keys=[first_token_id], back_populates="pools_first")
    second_token = relationship("Token", foreign_keys=[second_token_id], back_populates="pools_second")