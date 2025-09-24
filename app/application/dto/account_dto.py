from typing import Optional
from pydantic.dataclasses import dataclass


@dataclass
class AccountDTO:
    private_key: Optional[str]
    address: str