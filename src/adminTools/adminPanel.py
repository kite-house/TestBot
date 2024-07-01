from src.adminTools import permission
from aiogram.filters import Command
from aiogram import types, Router
from src.adminTools.tools import admin, tests

# Роутер
router = Router()
router.message.filter(permission.administration()) # Фильтр (Только администраторы)


@router.message(Command('delete'))
async def delete_test(message: types.Message):
    try:
        await tests.remove(message)
    except Exception as error:
        await message.reply(str(error))

@router.message(Command('makeadmin'))
async def make_admin(message: types.Message):
    try:
        await admin.make(message)
    except Exception as error:
        await message.reply(str(error))
        
@router.message(Command('removeadmin'))
async def remove_admin(message: types.Message):
    try:
        await admin.remove(message)
    except Exception as error:
        await message.reply(str(error))

@router.message(Command('help'))
async def help(message: types.Message):
    await message.reply(
        '/create - Создать тест'
        '/delete - Удалить тест'
        '/makeadmin {user} - Выдать права администратора пользователю'
        '/removeadmin {user} - Забрать права администратора у пользователя'
        )