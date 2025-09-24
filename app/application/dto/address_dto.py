from pydantic.dataclasses import dataclass

@dataclass
class AddressDTO:
    id: int
    user_id: int
    address: str