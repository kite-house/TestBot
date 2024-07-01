from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import types, Router, F
from src import keyMarkup
from aiogram.utils.formatting import Bold, as_list, as_marked_section, as_key_value
from datetime import datetime

# Роутер
router = Router()
router.message.filter()



@router.message(F.text.lower() == 'пройти тест')
async def start(message: types.Message):
    await message.reply('ку ку)')    
