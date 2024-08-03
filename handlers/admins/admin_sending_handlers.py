import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.adminkeys import adm_adm
from keyboards.default.start_dk import main_keyboard
from keyboards.inline.elon_keys import yes_no

from data.config import SUPER_ADMIN
from loader import dp, bot, db


@dp.message_handler(text="Cancel sending messages", state="*", user_id=SUPER_ADMIN)
async def cancel_send_state(message: types.Message, state: FSMContext):
    await message.answer(
        text="<b>E'LON JO'NATISH STATE</b> o'chirildi!"
    )
    await state.finish()


@dp.message_handler(text=['/admin'], user_id=SUPER_ADMIN, state="*")
async def buttons(message: types.Message):
    admin = await db.select_user(
        telegram_id=message.from_user.id
    )
    if admin[3] is True:
        await message.answer(
            text="Jarayon tugatilmadi!",
            reply_markup=main_keyboard
        )
    else:
        await message.answer(
            text='Admin bosh menyusi',
            reply_markup=adm_adm
        )


@dp.message_handler(text='Sending messages', user_id=SUPER_ADMIN)
async def admin_sendmes_state(message: types.Message, state: FSMContext):
    await message.answer(
        text=f"<b>E'LON JO'NATISH STATE</b> yoqildi!"
    )
    await state.set_state(
        state="elon"
    )


@dp.message_handler(content_types=['text'], state="elon", user_id=SUPER_ADMIN)
async def elonj(message: types.Message, state: FSMContext):
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
        await call.message.answer(
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


@dp.message_handler(text="Delete blocked users", user_id=SUPER_ADMIN)
async def deleteblockedusers(message: types.Message):
    blocked_users = await db.select_all_users()

    c = 0
    for user in blocked_users:
        if user[2]:
            c += 1
            await db.delete_user_tgid(
                tgid=user[1]
            )
    await message.answer(
        text=f"Jami {c} ta foydalanuvchi ma'lumotlar omboridan o'chirildi!"
    )


@dp.message_handler(text="Count_all_users", user_id=SUPER_ADMIN, state="*")
async def count_users_handler(message: types.Message):
    count = await db.count_users()
    await message.answer(
        text=f"Umumiy foydalanuvchilar soni: {count} ta"
    )
