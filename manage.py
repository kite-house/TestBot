import asyncio
from aiogram import Bot
from os import getenv
from src.main import dp
from aiogram import types
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

bot = Bot(token = getenv('TELEGRAM_TOKEN'))

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))