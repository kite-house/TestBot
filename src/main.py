from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Dispatcher, types
from src.creation.insertData import router as createRouter
from src.adminTools.adminPanel import router as adminRouter
from src.passing.insertData import router as passingRouter
from db.database import session
from db.models import User
from src import keyMarkup

dp = Dispatcher()
dp.include_routers(
    createRouter, 
    adminRouter,
    passingRouter
)


# Start
@dp.message(Command('start'))
async def start(message: types.Message):
    user = session.query(User.username).filter(User.username == message.from_user.username).first()
    if not user:
        session.add(User(username = message.from_user.username))
        session.commit()
    await message.reply("Привет! Я бот для создание и прохождение тестов!", reply_markup= keyMarkup.startTest)

@dp.message(Command('cancel'))
async def cancelCreation(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Вы успешно отменили текущее действие!")