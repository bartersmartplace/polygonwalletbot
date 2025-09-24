from dataclasses import dataclass


@dataclass
class ContractsDTO:
    QUOTER = "quoter"
    ROUTER = "router"
    ERC20 = "erc20"
    STAKED_BRTR = "staked_brtr"