from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    Form_addAdmin1 = State()
    Form_addAdmin2 = State()
    Form_addAdmin3 = State()

    Form_removeAdmin1 = State()
    Form_removeAdmin2 = State()

    Form_unmute = State()