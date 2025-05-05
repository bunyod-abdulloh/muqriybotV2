from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.ilm_suhbati_main_buttons import ilm_suhbats_main_ikb
from loader import dp, ilmdb
from states.admin_states import AdminStates


@dp.message_handler(F.text == "📚 Ilmiy suhbatlar", state="*")
async def handle_ilm_suh_main(message: types.Message, state: FSMContext):
    await state.finish()
    data = await ilmdb.get_titles()
    text = str()

    for index, title in enumerate(data, start=1):
        text += f"{index}. {title['title']}\n"
    await message.answer(text=text, reply_markup=ilm_suhbats_main_ikb(data=data))


@dp.message_handler(F.text == "on_id", state="*")
async def handle_add_id(message: types.Message):
    await message.answer(text="Jonli suhbatlar uchun videolarni yuboring\n\n"
                              "Namuna: title,title_id,message_id")
    await AdminStates.ADD_ID.set()


@dp.message_handler(state=AdminStates.ADD_ID, content_types=types.ContentType.TEXT)
async def handle_video_id(message: types.Message):
    title, title_id, message_id = message.text.split(",")
    await ilmdb.add_ilm_suhbati_video(title=title, title_id=title_id, video=message_id)
    await message.answer(text="Video bazaga joylandi")


@dp.callback_query_handler(F.data.startswith("ilmsuhbati:"), state="*")
async def handle_ilm_suh_ft(call: types.CallbackQuery):
    chapter_id = int(call.data.split(":")[1])
    print(chapter_id)

