from aiogram import Router
from tg_bot.middlewares import TokenMiddleware
from tg_bot.bot_instance import bot


token_router = Router(name="token_router")
token_router.message.middleware(TokenMiddleware(bot, bot.id))
token_router.callback_query.middleware(TokenMiddleware(bot, bot.id))