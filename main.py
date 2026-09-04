import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.engine import init_db
from handlers import common, auth, clients, orders, tasks, search
from scheduler.jobs import scheduler

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    await init_db()
    print("✅ База данных инициализирована")
    
    dp.include_router(common.router)
    dp.include_router(auth.router)
    dp.include_router(clients.router)
    dp.include_router(orders.router)
    dp.include_router(tasks.router)
    dp.include_router(search.router)
    
    scheduler.start()
    print("⏰ Планировщик запущен")
    
    print("🚀 Бот запущен и ждет сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())