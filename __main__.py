import asyncio
from tg_bot import run_bot
from notification_service import run_parsing
import multiprocessing


if __name__ == '__main__':
    parsing_process = multiprocessing.Process(target=run_parsing)
    parsing_process.start()
    asyncio.run(run_bot())