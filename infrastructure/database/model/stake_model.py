from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Stake(Base):
    __tablename__ = 'stake'
    
    id = Column(Integer, primary_key=True)
    stake_token_id = Column(Integer, ForeignKey('token.id'), nullable=False)
    reward_token_id = Column(Integer, ForeignKey('token.id'), nullable=False)

    stake_token = relationship("Token", foreign_keys=[stake_token_id], backref="staking_as_stake")
    reward_token = relationship("Token", foreign_keys=[reward_token_id], backref="staking_as_reward")