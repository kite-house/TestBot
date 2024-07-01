from db.database import session
from db.models import User
from typing import Union, Dict, Any
from aiogram.filters import BaseFilter
from aiogram.types import Message

# Проверка на наличие админки в БД
class administration(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, dict[str, Any]]:
        try:
            permission = session.query(User.is_superuser).filter(User.username == message.from_user.username).first()[0] # Возвращает True. False в зависимости от is_superuser
        except Exception:
            session.add(User(username = message.from_user.username))
            session.commit()
            permission = False
        if permission:
            return True
        await message.reply('У вас нету прав администратора!') 
        return False