from aiogram.fsm.state import StatesGroup, State


class GuestName(StatesGroup):
    Name = State()
    del_Name = State()
