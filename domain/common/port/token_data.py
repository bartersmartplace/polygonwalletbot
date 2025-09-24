from dataclasses import dataclass
from typing import Protocol


@dataclass
class TokenData(Protocol):
    address: str