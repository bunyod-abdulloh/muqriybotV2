from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

audio_video_page = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⏮ Олдинги"),
            KeyboardButton(text="🏡 Бош саҳифа"),
        ],
        [
            KeyboardButton(text="🎧 Ayдиo"),
            KeyboardButton(text="🎬 Видео"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

alldk = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🏡 Бош саҳифа"),
        ],
        [
            KeyboardButton(text="🎧 Ayдиo"),
            KeyboardButton(text="🎬 Видео"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# else:
#     await msg.answer("Қуйидаги тугмалардан бирини киритинг:")
