from tg_bot.bot_instance import dp, bot
from tg_bot.routers import ROUTERS  


async def run_bot():
    for router in ROUTERS:
        dp.include_router(router)
    await dp.start_polling(bot)