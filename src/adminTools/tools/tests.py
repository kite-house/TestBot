from db.database import session
from db.models import Tests
from aiogram import types
from src.adminTools.tools.admValidation import Validation
from aiogram.enums import ParseMode

@Validation.args
async def remove(message: types.Message, title: str = None): 
    user = session.query(Tests).filter(Tests.title == title)

    if not user.first():
        raise SystemError('Такой тест не существует!')
    
    user.delete()
    session.commit()

    await message.reply(f'Вы успешно удалил тест <b>{title}</b>!', parse_mode= ParseMode.HTML)

