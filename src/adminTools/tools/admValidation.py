from aiogram import types

class Validation:
    def args(func):
        async def wrapper(message: types.Message):
            try:
                return await func(message, ' '.join(message.text.lower().split(' ')[1:]))
            except IndexError:
                await message.reply('Укажите обьект, после команды через пробел!')
            except SystemError as error:
                await message.reply(str(error))
            except Exception as error:
                await message.reply(f"Неизвестная ошибка: {str(error)}")
        return wrapper 
