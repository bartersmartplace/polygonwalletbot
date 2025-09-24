from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, BigInteger
)
from sqlalchemy.orm import relationship
from .base import Base
from app.application.dto import TokenDTO


class Token(Base):
    __tablename__ = 'token'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    address = Column(String, unique=True, nullable=True)
    standard = Column(String, nullable=True, default="Root")
    decimal = Column(Integer, nullable=False, default=1)
    network_id = Column(Integer, ForeignKey('network.id'), nullable=False)
    is_base = Column(Boolean, default=False)
    last_checked_block = Column(BigInteger, default=0)
    
    network = relationship("Network", back_populates="tokens")
    pools_first = relationship("Pool", foreign_keys="[Pool.first_token_id]", back_populates="first_token")
    pools_second = relationship("Pool", foreign_keys="[Pool.second_token_id]", back_populates="second_token")
    users = relationship("UserTokens", back_populates="token")


    @property
    def dto(self):
        return TokenDTO(
            id=self.id,
            name=self.name,
            symbol=self.symbol,
            address=self.address,
            standard=self.standard,
            decimal=self.decimal,
            network_id=self.network_id,
            is_base=self.is_base,
            last_checked_block=self.last_checked_block
        )