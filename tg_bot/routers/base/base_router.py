from aiogram import Router
from tg_bot.middlewares import BaseMiddleware
from tg_bot.bot_instance import bot


base_router = Router(name="base_router")
base_router.message.middleware(BaseMiddleware(bot, bot.id))
base_router.callback_query.middleware(BaseMiddleware(bot, bot.id))