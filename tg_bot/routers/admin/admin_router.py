from aiogram import Router
from tg_bot.middlewares import AdminMiddleware
from tg_bot.bot_instance import bot


admin_router = Router(name="admin_router")
admin_router.message.middleware(AdminMiddleware(bot, bot.id))
admin_router.callback_query.middleware(AdminMiddleware(bot, bot.id))