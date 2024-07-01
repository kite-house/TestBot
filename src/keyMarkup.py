from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


confirmationAnswerOptions = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text = 'завершить')
    ]
    ], resize_keyboard=True, one_time_keyboard= True
)

confirmationQuestion = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text = 'продолжить'),
        KeyboardButton(text = 'завершить')
    ]
    ], resize_keyboard=True, one_time_keyboard= True
)

confirmationSaveTest = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text = 'сохранить'),
        KeyboardButton(text = 'удалить')
    ]
    ], resize_keyboard=True, one_time_keyboard= True
)

startTest = ReplyKeyboardMarkup(keyboard= [
    [
        KeyboardButton(text = 'пройти тест')
    ]
    ], resize_keyboard=True, one_time_keyboard= True
)