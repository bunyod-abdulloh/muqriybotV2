import asyncio

import aiogram
import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from magic_filter import F

from handlers.admins.sample import users_list
from keyboards.default.adminkeys import adm_adm
from keyboards.default.start_dk import main_keyboard

from data.config import SUPER_ADMIN
from loader import dp, db


@dp.message_handler(Command('admins'), user_id=SUPER_ADMIN, state="*")
async def admin_main_handler(message: types.Message):
    await message.answer(
        text='Admin bosh menyusi',
        reply_markup=adm_adm
    )


@dp.message_handler(F.text == 'Sending messages', user_id=SUPER_ADMIN)
async def admin_sendmes_state(message: types.Message, state: FSMContext):
    send_status = await db.select_status()

    if send_status is True:
        await message.answer(
            text="Jarayon tugatilmadi!",
            reply_markup=main_keyboard
        )
    else:
        await message.answer(
            text="Xabaringizni yuboring"
        )
        await state.set_state(
            state="elon"
        )


@dp.message_handler(state="elon", user_id=SUPER_ADMIN, content_types=types.ContentTypes.ANY)
async def elonj(message: types.Message, state: FSMContext):
    await state.finish()
    await db.update_status_true()
    all_users = await db.select_all_users()
    success_count, failed_count = 0, 0
    for index, user in enumerate(all_users, start=1):
        try:
            success_count += 1
            await message.copy_to(chat_id=user['telegram_id'])
        except aiogram.exceptions.BotBlocked:
            failed_count += 1
            await db.delete_user_tgid(user['telegram_id'])
        else:
            failed_count += 1
            await db.delete_user_tgid(user['telegram_id'])
        if index % 1500 == 0:
            await asyncio.sleep(30)
        await asyncio.sleep(0.05)
    await message.answer(
        f"Xabar {success_count} ta foydalanuvchiga yuborildi!"
    )
    await db.update_status_false()


@dp.message_handler(F.text == "Count_all_users", user_id=SUPER_ADMIN, state="*")
async def count_users_handler(message: types.Message):
    count = await db.count_users()
    await message.answer(
        text=f"Umumiy foydalanuvchilar soni: {count} ta"
    )


# @dp.message_handler(F.text == "add_users", user_id=SUPER_ADMIN)
# async def add_users(message: types.Message):
#     count = 0
#     for user in users_list:
#         try:
#             count += 1
#             await db.add_user(telegram_id=user)
#         except asyncpg.exceptions.UniqueViolationError:
#             pass
#         else:
#             pass
#
#     await message.answer(text=f"{count} ta foydalanuvchi qo'shildi!")
