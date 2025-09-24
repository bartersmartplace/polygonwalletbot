from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, BigInteger
)
from sqlalchemy.orm import relationship
from .base import Base
from app.application.dto import UserDTO


class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=True)
    tg_name = Column(String, nullable=True)
    tg_username = Column(String, nullable=True)
    active_address_id = Column(Integer, ForeignKey('address.id'))
    address_limit = Column(Integer, default=1)
    language = Column(String, default="en")
    is_admin = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    referrer_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    ref_income = Column(Integer, default=0)
    tokens_limit = Column(Integer, default=1)
    
    active_address = relationship("Address", foreign_keys=[active_address_id])
    tokens = relationship("UserTokens", back_populates="user") 
    referrer = relationship("User", remote_side=[id], backref="referrals", cascade="all, delete")


    @property
    def dto(self) -> UserDTO:
        """Return a UserDTO representation of the User model."""
        return UserDTO(
            id=self.id,
            tg_id=self.tg_id,
            tg_name=self.tg_name,
            tg_username=self.tg_username,
            active_address_id=self.active_address_id,
            address_limit=self.address_limit,
            language=self.language,
            is_admin=self.is_admin,
            is_banned=self.is_banned,
            referrer_id=self.referrer_id,
            ref_income=self.ref_income,
            tokens_limit = self.tokens_limit
        )