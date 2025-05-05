from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.ilm_suhbati_main_buttons import ilm_suhbats_main_ikb, ilm_suhbats_main_list
from loader import dp, ilmdb


@dp.message_handler(F.text == "📚 Ilmiy suhbatlar", state="*")
async def handle_ilm_suh_main(message: types.Message, state: FSMContext):
    await state.finish()
    data = await ilmdb.get_titles()
    text = str()

    for index, title in enumerate(data, start=1):
        text += f"{index}. {title['title']}\n"
    await message.answer(text=text, reply_markup=ilm_suhbats_main_ikb(data=data))


@dp.callback_query_handler(F.data.startswith("ilmsuhbati:"), state="*")
async def handle_ilm_suh_ft(call: types.CallbackQuery):
    chapter_id = int(call.data.split(":")[1])
    print(chapter_id)


@dp.message_handler(F.text == "add_ilm", state="*")
async def handle_add_ilm(message: types.Message):
    c = 0
    for suhbat in ilm_suhbats_main_list:
        c += 1
        await ilmdb.add_ilm_suhbati(title=suhbat)
    await message.answer(text=f"{c} ta ma'lumot qo'shildi")
