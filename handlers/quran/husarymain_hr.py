from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.file_ids import husary_dict
from handlers.quran.muqriyrecitation_hr import quran_hasanxon_husaynxon_alert
from keyboards.inline.quran_ibuttons import key_returner_muqriy_husary
from loader import dp, db
from utils.functions.all import extracter


@dp.message_handler(F.text == "husary")
async def husary_handler(message):
    """
    Husary Ta'lim uslubida bo'limi bilan bog'liq sura va oyatlar ro'yxatini qo'shish uchun handler.
    """

    c = 0
    for key, value in husary_dict.items():
        c += 1
        await db.add_husary(
            sura_name=value[0],
            total_verses=value[1],
            zip_=value[2],
            audio=value[3]
        )

    await message.answer(f"{c} ta ma'lumot qo'shildi!")


@dp.message_handler(F.text == "Qur'oni Karim tilovati (ta'lim uslubida)", state="*")
async def husary_first_rtr(message: types.Message, state: FSMContext):
    await state.finish()

    husary = await db.select_all_husary()

    extract = extracter(
        all_medias=husary, delimiter=16
    )

    current_page = 1
    all_pages = len(extract)

    items = extract[current_page - 1]
    markup = key_returner_muqriy_husary(
        items=items, callback_data="husary", current_page=current_page, all_pages=all_pages
    )
    await message.answer(
        text="Sura tartib raqamini tanlang", reply_markup=markup
    )


@dp.callback_query_handler(F.data.startswith('prev_husary:'))
async def husary_main_prev_rtr(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    current_page = int(call.data.split(':')[2])

    husary = await db.select_all_husary()

    extract = extracter(
        all_medias=husary, delimiter=16
    )

    all_pages = len(extract)

    if current_page == 1:
        current_page = all_pages
    else:
        current_page -= 1

    items = extract[current_page - 1]
    markup = key_returner_muqriy_husary(
        items=items, callback_data="husary", current_page=current_page, all_pages=len(extract)

    )
    await call.message.edit_reply_markup(
        reply_markup=markup
    )


@dp.callback_query_handler(F.data.startswith("next_husary:"))
async def husary_main_next_rtr(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    current_page = int(call.data.split(':')[2])
    husary = await db.select_all_husary()

    extract = extracter(
        all_medias=husary, delimiter=16
    )

    all_pages = len(extract)

    if current_page == all_pages:
        current_page = 1
    else:
        current_page += 1

    items = extract[current_page - 1]

    markup = key_returner_muqriy_husary(
        items=items, callback_data="husary", current_page=current_page, all_pages=len(extract)

    )
    await call.message.edit_reply_markup(
        reply_markup=markup
    )


@dp.callback_query_handler(F.data.startswith("alert_husary"))
async def husary_main_alert(call: types.CallbackQuery):
    await quran_hasanxon_husaynxon_alert(
        call=call
    )
