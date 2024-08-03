from aiogram.types import ReplyKeyboardMarkup

adm_adm = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
)

adm_adm.row("Sending messages", "Cancel sending messages")
adm_adm.row("Count_all_users", "Delete blocked users")
adm_adm.add("Sql buttons", "🏡 Бош саҳифа")
