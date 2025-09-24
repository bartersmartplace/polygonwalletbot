from .address import address_router
from .base import base_router
from .user import user_router
from .token import token_router
from .swap import swap_router
from .admin import admin_router


ROUTERS = [
    address_router,
    base_router,
    user_router,
    token_router,
    swap_router,
    admin_router,
]

__all__ = [
    "ROUTERS",
]