from typing import Protocol


class IWeb3Provider(Protocol):
    async def check_connection(self):
        """Connect to the blockchain node"""
        pass