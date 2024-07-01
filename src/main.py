from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram import Dispatcher, types
from src.creation.insertData import router as instertRouter
from src.adminTools.adminPanel import router as adminRouter
from db.database import session
from db.models import User

dp = Dispatcher()
dp.include_routers(
    instertRouter, 
    adminRouter
)

# Start
@dp.message(Command('start'))
async def start(message: types.Message):
    user = session.query(User.username).filter(User.username == message.from_user.username).first()
    if not user:
        session.add(User(username = message.from_user.username))
        session.commit()
    await message.reply("Привет! Я бот для создание и прохождение тестов!")

@dp.message(Command('cancel'))
async def cancelCreation(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Вы успешно отменили текущее действие!")