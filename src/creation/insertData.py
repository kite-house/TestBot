from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import types, Router
from src.adminTools import permission
from src.creation.states import StatesCreatingTest
from src.creation.saveData import SaveTest
from src.creation.validation import Validation
from src import keyMarkup
from aiogram.utils.formatting import Bold, as_list, as_marked_section, as_key_value
from datetime import datetime

# Роутер
router = Router()
router.message.filter(permission.administration()) # Фильтр (Только администраторы)



@router.message(Command('create'))
async def create(message: types.Message, state: FSMContext):
    await state.update_data(questions = [], answerOptions = [], creater = message.from_user.username)
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
        content = as_list( 
            Bold(f'Успешно добавлен вопрос {data['questions'][-1]['question'].capitalize()}'),
            as_marked_section(
                Bold('Варианты ответов'),
                f'{'\n ➤ '.join(map(str.capitalize, data['questions'][-1]['answerOptions']))}',
                marker = " ➤ "
            ),
            as_marked_section(
                Bold("Правильный вариант ответа"),
                f'{data['questions'][-1]['correctAnswer'].capitalize()}',
                marker = " ➤ "
            ),
            Bold(f'Выберите продолжить чтобы добавить ещё один вопрос или завершить ввод вопросов'),
            sep = '\n\n'
            
        )
        await message.answer(**content.as_kwargs(), reply_markup=keyMarkup.confirmationQuestion)

@router.message(StatesCreatingTest.next)
async def next(message: types.Message, state: FSMContext):
    if message.text.lower() == "завершить":
        await state.set_state(StatesCreatingTest.confirmation)
        data = await state.get_data()
        content = as_list(
            Bold(f'Успешно создан тест {data['title'].capitalize()}'),
            as_marked_section(
                Bold('Список вопросов в данном тесте'),
                f'{"\n".join([(f" ➤ Вопрос: {data['question'].capitalize()}\n"
                               f"     ➤ Варианты ответа \n        ➤ {'\n        ➤ '.join(map(str.capitalize, data['answerOptions']))}\n"
                               f"     ➤ Правильный ответ: {data['correctAnswer'].capitalize()}\n") 
                               for data in data['questions']])}',
                marker=''
            ),
            as_marked_section(
                Bold('Информация'),
                as_key_value("Создатель", data['creater']),
                as_key_value("Дата создание теста", datetime.now().date().strftime('%d-%m-%Y')),
                as_key_value("Кол-во вопросов", len(data['questions'])),
                marker=' '
            ),
            Bold('Выберите сохранить или удалить данный тест'),
            sep="\n\n"
        )

        await message.reply(**content.as_kwargs(),reply_markup=keyMarkup.confirmationSaveTest)

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