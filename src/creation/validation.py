from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from db.database import session
from db.models import Tests
from src.creation.saveData import saveTest
from src.creation.states import StatesCreatingTest


class Validation:
    async def title(message: types.Message, state: FSMContext):
        search_title = session.query(Tests.title).filter(Tests.title == message.text.lower()).first()
        if search_title:
            await state.clear()
            raise ValueError('Тест с таким названием уже существует!')
        
    async def guestion(message: types.Message, state: FSMContext):
        question_values = ([item['question'] for item in saveTest.questions])
        duplicates = [x for x in question_values if question_values.count(message.text.lower()) > 0]
        if duplicates:
            await state.set_state(StatesCreatingTest.guestion)
            raise ValueError('Такой вопрос уже зарегистрирован в данном тесте!')
        
    async def answerOptions(message: types.Message, state: FSMContext):
        duplicates = [x for x in message.text.lower().split(',') if message.text.lower().split(',').count(x) > 1]
        if duplicates:
            await state.set_state(StatesCreatingTest.answerOptions)
            raise ValueError('Варианты ответа повторяются!')