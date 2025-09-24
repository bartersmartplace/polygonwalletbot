from aiogram import Router
from tg_bot.middlewares import UserMiddleware
from tg_bot.bot_instance import bot


user_router = Router(name="user_router")
user_router.message.middleware(UserMiddleware(bot, bot.id))
user_router.callback_query.middleware(UserMiddleware(bot, bot.id))