from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ilm_suhbats_main_list = ["Jonli suhbatlar", "Surxondaryo safari", "Toshkent viloyati", "Toshkent shahri",
                         "Haj va qurbonlik", "Ilmiy suhbatlar (fevral 2020 - iyun 2021)", "Suhbat va uchrashuvlar"]


def ilm_suhbats_main_ikb(data):
    btn = InlineKeyboardMarkup(row_width=1)

    for index, n in enumerate(data, start=1):
        btn.insert(
            InlineKeyboardButton(text=str(index), callback_data=f"ilmsuhbati:{n['id']}"
                                 ))
    return btn
