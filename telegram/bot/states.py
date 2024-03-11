from aiogram.filters.state import State, StatesGroup


class AddGroup(StatesGroup):
    title = State()
    description = State()

class EditChat(StatesGroup):
    photo = State()
    username = State()
    reddit = State()