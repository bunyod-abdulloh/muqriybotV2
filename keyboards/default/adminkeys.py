from aiogram.types import ReplyKeyboardMarkup

adm_adm = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
)

adm_adm.row("Sending messages")
adm_adm.row("Count_all_users")
adm_adm.add("🏡 Бош саҳифа")
