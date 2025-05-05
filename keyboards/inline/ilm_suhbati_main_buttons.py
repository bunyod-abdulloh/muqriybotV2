from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ilm_suhbats_main_ikb(data):
    btn = InlineKeyboardMarkup(row_width=4)

    for index, n in enumerate(data, start=1):
        btn.insert(
            InlineKeyboardButton(text=str(index), callback_data=f"ilmsuhbati:{n['title_id']}"
                                 ))
    return btn


def ilm_suhbati_audio_video_ikb(title_id):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(InlineKeyboardButton(text="Audio", callback_data=f"ilmsuhaudio:{title_id}"),
            InlineKeyboardButton(text="Video", callback_data=f"ilmsuhvideo:{title_id}"))
    btn.add(InlineKeyboardButton(text="Ortga", callback_data=f"ilmback:1"))
    return btn
