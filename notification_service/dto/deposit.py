from decimal import Decimal
from dataclasses import dataclass


@dataclass
class Deposit:
    language: str
    telegram_id: int
    address: str
    currency_symbol: str
    amount: Decimal 
    hash: str