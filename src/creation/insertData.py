from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Dispatcher, types
from magic_filter import F
from aiogram import Router
from src.creation import permission
from src.creation.states import StatesCreatingTest
from src.creation.saveData import saveTest


# Роутер
router = Router()
router.message.filter(permission.administration()) # Фильтр (Только администраторы)

@router.message(Command('create'))
async def create(message: types.Message, state: FSMContext):
    await state.set_state(StatesCreatingTest.title)
    await message.answer('Приступаем к созданию теста, как хотите назвать тест?')


@router.message(StatesCreatingTest.title)
async def set_name(message: types.Message, state: FSMContext):
    await state.update_data(title = message.text.lower())
    await state.set_state(StatesCreatingTest.guestion)
    await message.answer("Введите название вопроса")

@router.message(StatesCreatingTest.guestion)
async def add_quest(message: types.Message, state: FSMContext):
    await state.update_data(question = message.text.lower())
    await state.set_state(StatesCreatingTest.answerOptions)
    await message.answer('Введите варианты ответа через запятую')

@router.message(StatesCreatingTest.answerOptions)
async def add_quest(message: types.Message, state: FSMContext):
    await state.update_data(answerOptions = message.text.lower())
    await state.set_state(StatesCreatingTest.correctAnswer)
    await message.answer('Введите правильный ответ: ')

@router.message(StatesCreatingTest.correctAnswer)
async def add_quest(message: types.Message, state: FSMContext):
    await state.update_data(correctAnswer = message.text.lower())
    await saveTest.add_quest(state)
    await state.set_state(StatesCreatingTest.next)
    await message.answer(f'Успешно добавлен вопрос: **{saveTest.questions[-1]['question']}**\n'
                          'Варианты ответов\n' 
                         f'{'\n'.join(map(str, saveTest.questions[-1]['answerOptions']))}\n' 
                          'Правильный ответ\n'
                         f'{saveTest.questions[-1]['correctAnswer']}')

@router.message(StatesCreatingTest.next)
async def next(message: types.Message, state: FSMContext):
    if message.text.lower() == "завершить":
        await state.set_state(StatesCreatingTest.confirmation)
        await message.reply(f'Как скажите! \nВаш тест\nNone')
    else:
        await state.set_state(StatesCreatingTest.guestion)

@router.message(StatesCreatingTest.confirmation)
async def confirmation(message: types.Message, state: FSMContext):
    if message.text.lower() == 'сохранить':
        await saveTest.save(state)

    else:
        await state.clear()
        await message.reply('Тест был удалён!')