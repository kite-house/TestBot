from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram import Dispatcher, types
from src.creation.insertData import router as instertRouter

dp = Dispatcher()
dp.include_router(instertRouter) # Добавляем команды из instertData

# Start
@dp.message(Command('start'))
async def start(message: types.Message):
    await message.reply("Привет! Я бот для создание и прохождение тестов!")

@dp.message(Command('cancel'))
async def cancelCreation(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Вы успешно отменили текущее действие!")