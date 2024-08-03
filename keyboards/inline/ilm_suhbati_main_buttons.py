from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ilmiy_suhbatlar_home_list = ["Jonli suhbatlar", "Surxondaryo safari", "Toshkent viloyati", "Toshkent shahri",
                             "Haj va qurbonlik", "Ilmiy suhbatlar (fevral 2020 - iyun 2021)", "Suhbat va uchrashuvlar"]

ilm_suhbati_home_page = InlineKeyboardMarkup(row_width=5)

index_number = 0
for suhbat in ilmiy_suhbatlar_home_list:
    ilm_suhbati_home_page.insert(
        InlineKeyboardButton(
            text=suhbat,
            callback_data=f"ilmsuhbati_{index_number}"
        )
    )
    index_number += 1
index_number = 0
