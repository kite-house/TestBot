from aiogram import types

class Validation:
    def user(func):
        async def wrapper(message: types.Message):
            try:
                return await func(message, username = message.text.lower().split(' ')[1])
            except IndexError:
                await message.reply('Укажите пользователя!')
            except SystemError as error:
                await message.reply(str(error))
            except Exception as error:
                await message.reply(f"Неизвестная ошибка: {str(error)}")
        return wrapper 
