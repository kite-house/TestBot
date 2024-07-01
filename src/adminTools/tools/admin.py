from db.database import session
from db.models import User
from aiogram import types
from src.adminTools.tools.admValidation import Validation
from aiogram.enums import ParseMode

@Validation.args
async def make(message: types.Message, username: str = None):
    user = session.query(User).filter(User.username == username)
    
    if not user.first():
        raise SystemError('Такой пользователь не найден!')
    if user.first().is_superuser == True:
        raise SystemError('Этот пользователь уже имеет права администратора!')

    user.update({User.is_superuser : 1})
    session.commit()

    await message.reply(f'Вы успешно выдали <b>{username}</b> права администратора!', parse_mode= ParseMode.HTML)


@Validation.args
async def remove(message: types.Message, username: str = None): 
    user = session.query(User).filter(User.username == username)

    if not user.first():
        raise SystemError('Такой пользователь не найден!')
    if user.first().is_superuser == False:
        raise SystemError('Этот пользователь и так не имеет прав администратора!')
    if user.first().username == message.from_user.username:
        raise SystemError('Вы не можете забрать права администратора у самого себя')
    
    user.update({User.is_superuser : 0})
    session.commit()

    await message.reply(f'Вы успешно забрали у <b>{username}</b> права администратора!', parse_mode= ParseMode.HTML)