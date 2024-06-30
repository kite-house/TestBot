from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram import Dispatcher, types
from magic_filter import F
from aiogram import Router
from src.creation import permission
from src.creation.states import StatesCreatingTest
from src.creation.saveData import SaveTest
from src.creation.validation import Validation
from src.creation import keyMarkup
from aiogram.enums import ParseMode
# Роутер
router = Router()
router.message.filter(permission.administration()) # Фильтр (Только администраторы)



@router.message(Command('create'))
async def create(message: types.Message, state: FSMContext):
    await state.update_data(questions = [], answerOptions = [])
    await state.set_state(StatesCreatingTest.title)
    await message.answer('Приступаем к созданию теста, как хотите назвать тест?')


@router.message(StatesCreatingTest.title)
async def set_title(message: types.Message, state: FSMContext):
    try: 
        await Validation.title(message, state)
    except Exception as error:
        await message.reply(str(error))
    else:
        await state.update_data(title = message.text.lower())
        await state.set_state(StatesCreatingTest.question)
        await message.answer("Введите название вопроса")

@router.message(StatesCreatingTest.question)
async def set_question(message: types.Message, state: FSMContext):
    try:
        await Validation.question(message, state)
    except Exception as error:
        await message.reply(str(error))
    else: 
        await state.update_data(question = message.text.lower())
        await state.set_state(StatesCreatingTest.answerOptions)
        await message.answer('Введите первый вариант ответа')

@router.message(StatesCreatingTest.answerOptions)
async def set_answerOptions(message: types.Message, state: FSMContext):
    try:
        await Validation.answerOptions(message, state)
    except Exception as error:
        await message.reply(str(error))
    else:
        if message.text.lower() == 'завершить':
            await state.set_state(StatesCreatingTest.correctAnswer)
            await message.answer('Введите правильный ответ')
        else:
            await SaveTest.add_answerOptions(message, state)
            await message.answer("Введите следующий вариант ответа или завершить", reply_markup=keyMarkup.confirmationAnswerOptions)
            await state.set_state(StatesCreatingTest.answerOptions)

@router.message(StatesCreatingTest.correctAnswer)
async def set_correctAnswer(message: types.Message, state: FSMContext):
    try:
        await Validation.correctAnswer(message, state)
    except Exception as error:
        await message.reply(str(error))
    else:
        await state.update_data(correctAnswer = message.text.lower())
        await SaveTest.add_quest(state)
        await state.set_state(StatesCreatingTest.next)
        data = await state.get_data()
        await message.answer(f'Успешно добавлен вопрос: <b>{data['questions'][-1]['question']}<b>\n'
                            'Варианты ответов\n' 
                            f'{'\n'.join(map(str, data['questions'][-1]['answerOptions']))}\n' 
                            'Правильный ответ\n'
                            f'{data['questions'][-1]['correctAnswer']}\n'
                            '\n'
                            'Введите продолжить дабы добавить ещё вопрос или же завершить', 
                            reply_markup=keyMarkup.confirmationQuestion, parse_mode=ParseMode.HTML)

@router.message(StatesCreatingTest.next)
async def next(message: types.Message, state: FSMContext):
    if message.text.lower() == "завершить":
        await state.set_state(StatesCreatingTest.confirmation)
        data = await state.get_data()
        await message.reply(f'Вы создали тест {data['title']}\n'
                    f'Список вопросов\n'
                    f'------------------\n'
                    f'{"-------------------\n".join([f"Вопрос: {data['question']}\nВарианты ответа: {', '.join(data['answerOptions'])}\nПравильный ответ: {data['correctAnswer']}\n" for data in data['questions']])}'
                    f'--------------------\n'
                    f'Если вам понравился тест введите сохранить для отправки на сервер, или же удалить', reply_markup=keyMarkup.confirmationSaveTest)
    
    elif message.text.lower() == 'продолжить':
        await state.set_state(StatesCreatingTest.question)
        await message.reply('Введите название вопроса')

    else:
        await message.reply("Введите продолжить дабы добавить ещё вопрос или же завершить", reply_markup=keyMarkup.confirmationQuestion)
        await state.set_state(StatesCreatingTest.next)

@router.message(StatesCreatingTest.confirmation)
async def confirmation(message: types.Message, state: FSMContext):
    if message.text.lower() == 'сохранить':
        await SaveTest.save(state)
        await message.reply("Тест успешно был сохранен")

    elif message.text.lower() == 'удалить':
        await state.clear()
        await message.reply('Тест был удалён!')

    else:
        await state.set_state(StatesCreatingTest.confirmation)
        await message.reply('Введите продолжить или удалить!', reply_markup=keyMarkup.confirmationSaveTest)