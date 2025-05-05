from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminSqlButtons(StatesGroup):
    main = State()


class AdminStates(StatesGroup):
    ADD_ID = State()
