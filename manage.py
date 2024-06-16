import asyncio
from aiogram import Bot, Dispatcher, types
from os import getenv
from aiogram.filters.command import Command
bot = Bot(token = getenv('TELEGRAM_TOKEN'))
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.reply("Привет! Я бот для создание и прохождение тестов!")


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))