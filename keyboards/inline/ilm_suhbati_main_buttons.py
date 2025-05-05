from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ilm_suhbats_main_list = ["Jonli suhbatlar", "Surxondaryo safari", "Toshkent viloyati", "Toshkent shahri",
                         "Haj va qurbonlik", "Ilmiy suhbatlar (fevral 2020 - iyun 2021)", "Suhbat va uchrashuvlar"]

ilm_suhbats_main_ikb = InlineKeyboardMarkup(row_width=5)

for index, suhbat in enumerate(ilm_suhbats_main_list, start=1):
    ilm_suhbats_main_ikb.insert(
        InlineKeyboardButton(text=suhbat, callback_data=f"ilmsuhbati:{index}"
        )
    )
