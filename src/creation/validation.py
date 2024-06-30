from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from db.database import session
from db.models import Tests
from src.creation.states import StatesCreatingTest


class Validation:
    async def title(message: types.Message, state: FSMContext):
        search_title = session.query(Tests.title).filter(Tests.title == message.text.lower()).first()
        if search_title:
            await state.clear()
            raise ValueError('Тест с таким названием уже существует!')
        
    async def question(message: types.Message, state: FSMContext):
        data = await state.get_data()
        question_values = ([item['question'] for item in data['questions']])
        duplicates = [x for x in question_values if question_values.count(message.text.lower()) > 0]
        if duplicates:
            await state.set_state(StatesCreatingTest.guestion)
            raise ValueError('Такой вопрос уже зарегистрирован в данном тесте!')
        
    async def answerOptions(message: types.Message, state: FSMContext):
        data = await state.get_data()
        duplicates = [x for x in data['answerOptions'] if message.text.lower().split(',').count(x) > 0]
        if duplicates:
            await state.set_state(StatesCreatingTest.answerOptions)
            raise ValueError('Варианты ответа повторяются!')
        
    async def correctAnswer(message: types.Message, state: FSMContext):
        data = await state.get_data()
        if message.text.lower() not in data['answerOptions']:
            await state.set_state(StatesCreatingTest.correctAnswer)
            raise ValueError('Необходимо чтобы правильный ответ совпадал с одним из вариантов ответа!')