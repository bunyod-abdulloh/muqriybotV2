import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from typing import List

from keyboards.default.adminkeys import adm_adm
from keyboards.default.start_dk import main_keyboard
from keyboards.inline.elon_keys import yes_no

from data.config import SUPER_ADMIN
from loader import dp, bot, db


@dp.message_handler(text=['/admin'], user_id=SUPER_ADMIN, state="*")
async def buttons(message: types.Message):
    admin = await db.select_user(
        telegram_id=message.from_user.id
    )
    if admin[2] is True:
        await message.answer(
            text="Jarayon tugatilmadi!",
            reply_markup=main_keyboard
        )
    else:
        await message.answer(
            text='Admin bosh menyusi',
            reply_markup=adm_adm
        )


@dp.message_handler(text='Forward ON', user_id=SUPER_ADMIN)
async def admin_forward_state(message: types.Message, state: FSMContext):
    await message.answer(
        text=f"<b>FORWARD STATE</b> yoqildi!"
    )
    await state.set_state(
        state="forw"
    )


@dp.message_handler(text='MediaGroup ON', user_id=SUPER_ADMIN)
async def admin_mediagr_state(message: types.Message, state: FSMContext):
    await message.answer(
        text=f"<b>MEDIA GROUP STATE</b> yoqildi!"
    )
    await state.set_state(
        state="mediagroup"
    )


@dp.message_handler(text='ID ON', user_id=SUPER_ADMIN)
async def admin_id_state(message: types.Message, state: FSMContext):
    await message.answer(
        text=f"<b>ID OLISH STATE</b> yoqildi!"
    )
    await state.set_state(
        state="idolish"
    )


@dp.message_handler(text='Sending messages', user_id=SUPER_ADMIN)
async def admin_sendmes_state(message: types.Message, state: FSMContext):
    await message.answer(
        text=f"<b>E'LON JO'NATISH STATE</b> yoqildi!"
    )
    await state.set_state(
        state="elon"
    )


@dp.message_handler(content_types=['any'], user_id=SUPER_ADMIN, state="forw")
async def contumum(message: types.Message, state: FSMContext):
    content_type = ["audio", "video", "voice", "document", "photo", "text"]

    if message.text == 'Forward OFF':
        await message.answer(
            text="Forward ON state o'chirildi!"
        )
        await state.finish()
    else:
        if message.content_type in content_type:
            await db.update_admin(
                telegram_id=message.from_user.id,
                bool_value=True
            )
            await message.answer(
                text=f"Habar yuborilganligi haqidagi to'liq ma'lumot tez orada yuboriladi!",
                reply_markup=main_keyboard
            )
            await state.finish()

            users = await db.select_all_users()
            count_baza = await db.count_users()
            active = 0
            block = 0
            count_one = 0
            count_two = 0

            for user in users:
                try:
                    await message.forward(
                        chat_id=user[1]
                    )
                    active += 1

                except Exception:
                    block += 1
                    await db.update_blocked_user(
                        telegram_id=user[1],
                        blocked_id=user[1]
                    )
                    continue

                count_one += 1
                count_two += 1

                if count_one == 25:
                    count_one = 0
                    await asyncio.sleep(0.5)

                if count_two == 1500:
                    await asyncio.sleep(180)
                    count_two = 0

            await state.finish()
            await message.answer(f"SENT: {active}"
                                 f"\nBLOCK: {block}"
                                 f"\nALL_USERS: {count_baza}")
            await db.update_admin(
                telegram_id=message.from_user.id,
                bool_value=False
            )


@dp.message_handler(is_media_group=True, content_types=['any'], state="mediagroup")
async def mediagr(message: types.Message, album: List[types.Message], state: FSMContext):
    media_group = types.MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id
        try:
            media_group.attach({"media": file_id,
                                "type": obj.content_type,
                                "caption": obj.caption})
        except Exception as err:
            logging.exception(err)
            return await message.answer("Бу альбомни aiogram қўлламайди!")

    users = await db.select_all_users()
    count_baza = await db.count_users()
    active = 0
    block = 0
    count_one = 0
    count_two = 0
    await db.update_admin(
        telegram_id=message.from_user.id,
        bool_value=True
    )
    await message.answer(
        text=f"Habar yuborilganligi haqidagi to'liq ma'lumot tez orada yuboriladi!",
        reply_markup=main_keyboard
    )

    for user in users:
        try:
            await bot.send_media_group(
                chat_id=user[1],
                media=media_group
            )
            active += 1

        except Exception:
            block += 1
            await db.update_blocked_user(
                telegram_id=user[1],
                blocked_id=user[1]
            )
            continue

        count_one += 1
        count_two += 1

        if count_one == 25:
            count_one = 0
            await asyncio.sleep(0.5)

        if count_two == 1500:
            await asyncio.sleep(180)
            count_two = 0

    await state.finish()
    await message.answer(
        text=f"SENT: {active}"
             f"\nBLOCK: {block}"
             f"\nALL_USERS: {count_baza}")
    await db.update_admin(
        telegram_id=message.from_user.id,
        bool_value=False
    )


@dp.message_handler(state="mediagroup")
async def mediagryopish(message: types.Message, state: FSMContext):
    if message.text == "MediaGroup OFF":
        await message.answer(
            text="<b>MEDIA GROUP STATE</b> o'chirildi!"
        )
        await state.finish()


@dp.message_handler(content_types=['any'], user_id=SUPER_ADMIN, state="idolish")
async def idvideo(message: types.Message, state: FSMContext):
    if message.video:
        await message.answer(
            text=f"<b>VIDEO/CAPTION:</b> \n\n{message.caption}"
                 f"<b>\n\nVIDEO/ID:</b> \n\n{message.video.file_id}"
        )
    if message.audio:
        await message.answer(
            text=f"<b>AUDIO/CAPTION:</b> \n\n{message.caption}"
                 f"\n\n<b>AUDIO/ID:</b>\n\n{message.audio.file_id}"
        )
    if message.voice:
        await message.answer(
            text=f"<b>AUDIO/CAPTION:</b> \n\n{message.caption}"
                 f"\n\n<b>AUDIO/ID:</b>\n\n{message.voice.file_id}"
        )
    if message.photo:
        await message.answer(
            text=f"<b>PHOTO/CAPTION:</b>\n\n{message.caption}"
                 f"\n\n<b>PHOTO/ID:</b>\n\n{message.photo[-1].file_id}"
        )
    if message.document:
        await message.answer(
            text=f"<b>DOCUMENT/CAPTION:</b>\n\n{message.caption}"
                 f"\n\n<b>DOCUMENT/ID:</b>\n\n{message.document.file_id}"
        )

    if message.text == "ID OFF":
        await message.answer(
            text="<b>ID OLISH STATE</b> o'chirildi!"
        )
        await state.finish()

    elif message.text:
        await message.answer(
            text="Siz <b>ID OLISH STATE</b>dasiz."
                 "\n\nChiqish uchun <b>ID o'chirish</b> tugmasinig bosing!"
        )


@dp.message_handler(content_types=['text'], state="elon", user_id=SUPER_ADMIN)
async def elonj(message: types.Message, state: FSMContext):
    if message.text == "Cancel sending messages":
        await message.answer(
            text="<b>E'LON JO'NATISH STATE</b> o'chirildi!"
        )
        await state.finish()

    elif message.text:
        matn = message.text
        await message.answer(
            text="Yuboradigan habaringizni tekshirdingizmi?"
                 "\n\nOgoh bo'ling, habaringiz ko'pchilikka boradi!"
                 "\n\nHabarni yuborasizmi?",
            reply_markup=yes_no
        )
        await state.update_data(
            text=matn
        )
        await state.set_state(
            state="yes_no"
        )


@dp.callback_query_handler(state="yes_no")
async def checkyes_no(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    users = await db.select_all_users()
    count_baza = await db.count_users()
    active = 0
    block = 0
    count_one = 0
    count_two = 0
    if call.data == "yes":
        await db.update_admin(
            telegram_id=call.from_user.id,
            bool_value=True
        )
        await call.message.edit_text(
            text=f"Habar yuborilganligi haqidagi to'liq ma'lumot tez orada yuboriladi!",
            reply_markup=main_keyboard
        )
        await state.finish()

        for user in users:
            try:
                await bot.send_message(
                    chat_id=user[1],
                    text=data['text']
                )
                active += 1

            except Exception:
                block += 1
                await db.update_blocked_user(
                    telegram_id=user[1],
                    blocked_id=user[1]
                )
                continue

            count_one += 1
            count_two += 1

            if count_one == 25:
                count_one = 0
                await asyncio.sleep(0.5)

            if count_two == 1500:
                await asyncio.sleep(120)
                count_two = 0

        await call.message.answer(f"SENT: {active}"
                                  f"\nBLOCK: {block}"
                                  f"\nALL_USERS: {count_baza}")
        await db.update_admin(
            telegram_id=call.from_user.id,
            bool_value=False
        )

    elif call.data == "no_again":
        await call.message.answer(
            text="Habaringizni qayta yuborishingiz mumkin!"
        )
        await state.set_state("elon")
