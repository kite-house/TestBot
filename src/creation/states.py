
from aiogram.fsm.state import State, StatesGroup

class StatesCreatingTest(StatesGroup): 
    title = State()
    question = State()
    questions = State()
    answerOptions = State()
    correctAnswer = State()
    next = State()
    confirmation = State()
    creation = State()