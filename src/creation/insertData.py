from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram import Dispatcher, types
from aiogram import Router

router = Router()

class CreateTest(StatesGroup):
    title = State()
    # Корретикровки вопроса
    guest = State()
    variants = State()
    corect = State()
    next = State()

questions = []




@router.message(Command('create'))
async def create(message: types.Message, state: FSMContext):
    await message.answer('Приступаем к созданию теста, как хотите назвать тест?')
    await state.set_state(CreateTest.title)


@router.message(CreateTest.title)
async def set_name(message: types.Message, state: FSMContext):
    if message.text.lower() == 'Отмена':
        await state.clear()
        await message.reply('Ну как скажите')

    await state.update_data(title = message.text.lower())
    await message.answer("Введите название вопроса")
    await state.set_state(CreateTest.guest)

@router.message(CreateTest.guest)
async def add_quest(message: types.Message, state: FSMContext):
    await state.update_data(quest = message.text.lower())
    await message.answer('Введите варианты ответа через запятую: ')
    await state.set_state(CreateTest.variants)

@router.message(CreateTest.variants)
async def add_quest(message: types.Message, state: FSMContext):
    await state.update_data(variants = message.text.lower())
    await message.answer('Введите правильный ответ: ')
    await state.set_state(CreateTest.corect)

@router.message(CreateTest.corect)
async def add_quest(message: types.Message, state: FSMContext):
    await state.update_data(corect = message.text.lower())
    get_state = await state.get_data()
    questions.append({
        get_state['quest'] : {
            "Варианты ответа" : get_state['variants'],
            "Правильный ответ" : get_state['corect']
            }
        }
    )

    await message.answer(f'Создан вопрос: NONE \nВведите название следующего вопроса или же завершить если хотите закончить.')
    await state.set_state(CreateTest.next)

@router.message(CreateTest.next)
async def next(message: types.Message, state: FSMContext):
    if message.text.lower() == "завершить":
        await message.reply(f'Как скажите! \nВаш тест\n{questions}')

    else:
        await state.set_state(CreateTest.guest)

# state['questions'] -- ТО что там хранится!


# Имя - вопросы
