from aiogram import types

from handlers.users.quran_duolar_dict import duo_dict
from keyboards.default.users_custom_buttons import quran_prayers_custom_buttons
from loader import dp, statdb
from states.users_state import Quran_Prayers

quran_duolar_buttons = types.InlineKeyboardMarkup(row_width=5)
for key in duo_dict.keys():
    quran_duolar_buttons.insert(types.InlineKeyboardButton(text=f"{key}",
                                                           callback_data=f"quranduolar_{key}"))


@dp.message_handler(text="🤲 Қуръоний дуолар", state="*")
async def qd_title_page(message: types.Message):
    await statdb.upsert_statistics(chapter_name="Qur'oniy duolar")
    await message.answer(text=message.text,
                         reply_markup=quran_prayers_custom_buttons)
    await message.answer(text="Қуръоний дуоларни бирга ўрганамиз!"
                              "\n\nУстоз: Хасанҳон Яҳё Абдулмажид",
                         reply_markup=quran_duolar_buttons)
    await Quran_Prayers.first_page.set()


@dp.callback_query_handler(text_contains="quranduolar_", state=Quran_Prayers.first_page)
async def qd_first_page(call: types.CallbackQuery):
    await call.message.delete()
    album = types.MediaGroup()

    callback_data = call.data.split("_")[-1]
    media_keys = str(duo_dict.keys())

    if callback_data in media_keys:
        call_data = int(callback_data)
        if call_data == 19:
            await call.message.answer_photo(photo=duo_dict[call_data]['photo'],
                                            caption=duo_dict[call_data]['caption'])
        else:
            album.attach_photo(photo=duo_dict[call_data]['photo'],
                               caption=duo_dict[call_data]['caption'])
            album.attach_video(video=duo_dict[call_data]['video'])

            await call.message.answer_media_group(media=album)


@dp.message_handler(state=Quran_Prayers.first_page, text="⬅️ Ортга")
async def qd_back_function(message: types.Message):
    await message.answer(text="Қуръоний дуоларни бирга ўрганамиз!"
                              "\n\nУстоз: Хасанҳон Яҳё Абдулмажид",
                         reply_markup=quran_duolar_buttons)
    await Quran_Prayers.first_page.set()
