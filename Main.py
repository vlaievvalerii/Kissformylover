import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from Routes import morning_messages_loop, router


load_dotenv()

TOKEN = getenv("kissformylover")


async def main():
    if not TOKEN:
        raise ValueError("Не знайдено токен kissformylover у файлі .env")

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    asyncio.create_task(morning_messages_loop(bot))

    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
