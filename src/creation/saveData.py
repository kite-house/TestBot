from db.database import session
from db.models import Tests


class SaveTest:
    def __init__(self):
        self.questions = list()
    
    async def save(self, state):
        data = await state.get_data()
        session.add(Tests(title = data['title'], questions = self.questions))
        session.commit()
        self.questions.clear()

    async def add_quest(self, state):
        data = await state.get_data()
        self.questions.append({
                "question" : data['question'],
                "answerOptions" : data['answerOptions'].replace(" ", '').split(','),
                "correctAnswer" : data['correctAnswer']
            
        })

saveTest = SaveTest()