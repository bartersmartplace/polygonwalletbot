from typing import Optional
from dataclasses import dataclass
from .token_dto import TokenDTO

@dataclass
class TradeDTO:
    sell_token: TokenDTO
    amount_to_sell: int
    buy_token: TokenDTO
    amount_to_buy: Optional[int]