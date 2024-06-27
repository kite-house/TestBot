
from aiogram.fsm.state import State, StatesGroup

class StatesCreatingTest(StatesGroup): 
    title = State()
    guestion = State()
    answerOptions = State()
    correctAnswer = State()
    next = State()
    confirmation = State()