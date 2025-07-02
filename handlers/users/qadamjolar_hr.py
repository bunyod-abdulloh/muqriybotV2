from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import QADAMJOLAR
from keyboards.inline.qadamjolar_inline_buttons import MENU_POST, LATEST_RESULT, chunks, key_returner, \
    qadamjolar_back_button
from loader import dp, bot
from states.users_state import MuqriyVideoStates

ITEMS = list(range(1, 40))


@dp.callback_query_handler(text_contains="alertmessage_", state="*")
async def alert_message(call: types.CallbackQuery):
    current_page = call.data.split("_")[1]

    await call.answer(
        text=f"Siz {current_page} - sahifadasiz!",
        show_alert=True
    )


@dp.message_handler(text="📍 Расулуллоҳ ﷺ қадамжолари", state="*")
async def qadamjolar_first_handler(message: types.Message, state: FSMContext):
    c = 0
    datas = list(chunks(ITEMS, 15))

    keys = await key_returner(
        items=datas[c],
        current_page=1,
        all_pages=len(datas)
    )
    count_text = len(datas[c])
    text = str()
    for i in MENU_POST[:count_text]:
        text += f"{i}"
    await message.answer(
        text=text,
        reply_markup=keys
    )
    counter = c + 1
    await state.update_data(
        c=c,
        len_datas=len(datas),
        counter=counter
    )
    await MuqriyVideoStates.qadamjolar_menu.set()


@dp.callback_query_handler(state=MuqriyVideoStates.qadamjolar_menu)
async def callback_resp(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    if call.data in LATEST_RESULT.keys():
        await bot.copy_message(
            chat_id=call.from_user.id,
            from_chat_id=QADAMJOLAR,
            message_id=LATEST_RESULT[call.data],
            reply_markup=qadamjolar_back_button
        )
        await MuqriyVideoStates.qadamjolar_videos.set()

    else:
        data = await state.get_data()
        c = data['c']
        counter = data['counter']
        len_datas = data['len_datas']

        if call.data == "+1":
            c = int(c) + 1
            counter += 1
        elif call.data == "-1":
            c = int(c) - 1
            counter -= 1
        if c == len_datas or c == - len_datas:
            c = 0
            if c == 0 or c == 4:
                counter = 1

        datas = list(chunks(ITEMS, 15))[c]

        keys = await key_returner(
            items=datas,
            current_page=counter,
            all_pages=len_datas
        )

        text = str()
        for i in datas:
            text += f"{MENU_POST[i - 1]}"
        await call.message.answer(
            text=text,
            reply_markup=keys
        )
        await state.update_data(
            c=c,
            counter=counter
        )


@dp.callback_query_handler(state=MuqriyVideoStates.qadamjolar_videos)
async def qadamjolar_videos_state(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    c = data['c']
    counter = data['counter']

    datas = list(chunks(ITEMS, 15))

    keys = await key_returner(
        items=datas[c],
        current_page=counter,
        all_pages=len(datas)
    )
    first_index = datas[c][0] - 1
    last_index = datas[c][-1]
    text = str()
    for i in MENU_POST[first_index:last_index]:
        text += f"{i}"
    await call.message.answer(
        text=text,
        reply_markup=keys
    )
    await MuqriyVideoStates.qadamjolar_menu.set()
