from sqlalchemy import (
    Column, Integer, String
)
from .base import Base
from app.application.dto import AddressDTO


class Address(Base):
    __tablename__ = 'address'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    address = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Address(id={self.id}, address='{self.address}', user_id={self.user_id})>"
    

    @property
    def dto(self) -> AddressDTO:
        return AddressDTO(id=self.id, user_id=self.user_id, address=self.address)