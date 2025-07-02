from aiogram.types import ReplyKeyboardMarkup

adm_adm = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
)

adm_adm.row("E'lon yuborish")
adm_adm.row("Foydalanuvchilar soni")
adm_adm.row("Barcha statistika", "Sana bo'yicha")
adm_adm.add("🏡 Бош саҳифа")
