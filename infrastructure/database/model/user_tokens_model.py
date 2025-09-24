from sqlalchemy import (
    Column, Integer, ForeignKey
)
from sqlalchemy.orm import relationship
from .base import Base


class UserTokens(Base):
    __tablename__ = 'user_tokens'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    token_id = Column(Integer, ForeignKey('token.id', ondelete='CASCADE'), nullable=False)
    
    user = relationship("User", back_populates="tokens")
    token = relationship("Token", back_populates="users")