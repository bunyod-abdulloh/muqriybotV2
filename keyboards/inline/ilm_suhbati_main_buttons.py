from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ilm_suhbats_main_ikb(data):
    btn = InlineKeyboardMarkup(row_width=4)

    for index, n in enumerate(data, start=1):
        btn.insert(
            InlineKeyboardButton(text=str(index), callback_data=f"ilmsuhbati:{n['id']}"
                                 ))
    return btn
