from aiogram import Bot, Dispatcher
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import router, send_message
from aiogram.fsm.storage.redis import RedisStorage
from redisdb import redis_fsm
from config import TOKEN

TOKEN = TOKEN

redis = redis_fsm()
storage = RedisStorage(redis=redis)
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_message, trigger='cron', day_of_week='mon,wed,sat,fri', hour=10, minute=0)
    scheduler.start()
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
