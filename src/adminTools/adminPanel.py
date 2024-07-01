from aiogram import Router
from src.adminTools import permission
from aiogram.filters import Command
from aiogram import types
from src.adminTools.tools import admin

# Роутер
router = Router()
router.message.filter(permission.administration()) # Фильтр (Только администраторы)


@router.message(Command('delete'))
async def delete_test():
    pass

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