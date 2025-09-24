from typing import Optional
from pydantic.dataclasses import dataclass


@dataclass
class UserDTO:
    id: int
    tg_id: Optional[int]
    tg_name: Optional[str]
    tg_username: Optional[str]
    active_address_id: Optional[int]
    address_limit: int
    language: str
    is_admin: bool
    is_banned: bool
    referrer_id: Optional[int]
    ref_income: int
    tokens_limit: int