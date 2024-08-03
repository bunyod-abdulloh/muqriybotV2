from aiogram.dispatcher.filters.state import StatesGroup, State


class Quran_Prayers(StatesGroup):
    first_page = State()


class MuqriyVideoStates(StatesGroup):
    qadamjolar_menu = State()
    qadamjolar_videos = State()
