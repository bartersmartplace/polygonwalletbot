from pydantic.dataclasses import dataclass
from typing import List, Tuple
from app.application.dto import TokenDTO 


@dataclass
class BalanceDTO:
    address: str
    tokens: List[Tuple[TokenDTO, int]]