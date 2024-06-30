from db.database import session
from db.models import Tests
from aiogram.fsm.context import FSMContext
from aiogram import types
class SaveTest:
    async def save(state: FSMContext):
        data = await state.get_data()
        session.add(Tests(title = data['title'], questions = data['questions']))
        session.commit()
        await state.clear()

    async def add_quest(state: FSMContext):
        data = await state.get_data()
        data['questions'].append({
                "question" : data['question'],
                "answerOptions" : data['answerOptions'],
                "correctAnswer" : data['correctAnswer']  
        })
        await state.update_data(questions = data['questions'])
        await state.update_data(answerOptions = [])

    async def add_answerOptions(message: types.Message, state: FSMContext):
        data = await state.get_data()
        data['answerOptions'].append(message.text.lower())
        await state.update_data(answerOptions = data['answerOptions'])