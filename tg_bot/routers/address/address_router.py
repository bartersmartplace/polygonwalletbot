from aiogram import Router
from tg_bot.middlewares import AddressMiddleware
from tg_bot.bot_instance import bot


address_router = Router(name="address_router")
address_router.message.middleware(AddressMiddleware(bot, bot.id))
address_router.callback_query.middleware(AddressMiddleware(bot, bot.id))