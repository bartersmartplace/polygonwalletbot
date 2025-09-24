from aiogram import Router
from tg_bot.middlewares import SwapMiddleware
from tg_bot.bot_instance import bot


swap_router = Router(name="swap_router")
swap_router.message.middleware(SwapMiddleware(bot, bot.id))
swap_router.callback_query.middleware(SwapMiddleware(bot, bot.id))