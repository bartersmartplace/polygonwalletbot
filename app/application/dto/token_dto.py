from typing import Optional
from pydantic.dataclasses import dataclass


@dataclass
class TokenStandardsDTO:
    erc20 = "erc20"
    erc721 = "erc721"


@dataclass
class TokenDTO:
    id: int
    name: str
    symbol: str
    address: Optional[str]
    standard: Optional[str]
    decimal: int
    network_id: int
    is_base: bool
    last_checked_block: int