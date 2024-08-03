from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def new_party(media_text):
    button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for n in range(len(media_text)):
        button.row(n)
    return button
