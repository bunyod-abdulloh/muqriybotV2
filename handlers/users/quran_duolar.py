from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.quran_duolar_dict import duo_dict
from keyboards.default.users_custom_buttons import quran_prayers_custom_buttons
from loader import dp
from states.users_state import Quran_Prayers


quran_duolar_buttons = types.InlineKeyboardMarkup(row_width=5)
for key in duo_dict.keys():
    quran_duolar_buttons.insert(types.InlineKeyboardButton(text=f"{key}",
                                                           callback_data=f"quranduolar_{key}"))


# @dp.message_handler(text="🤲 Қуръоний дуолар", state="*")
# async def qd_sample(message: types.Message):
#
#     await message.answer(text="Техник хатолар тўғриланиб қайта жойланади!")


@dp.message_handler(text="photo_video", state="*")
async def photo_id_function(message: types.Message, state: FSMContext):
    await message.answer(text="Photo yoki video yuboring")
    await state.set_state("photo_video_state")


@dp.message_handler(state="photo_video_state", content_types=["photo", "video"])
async def photo_state_function(message: types.Message):
    if message.content_type == "photo":
        await message.answer(text=f"PHOTO ID\n\n<code>{message.photo[-1].file_id}</code>")

    elif message.content_type == "video":
        await message.answer(text=f"VIDEO ID \n\n<code>{message.video.file_id}</code>")


@dp.message_handler(text="🤲 Қуръоний дуолар", state="*")
async def qd_title_page(message: types.Message):
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
