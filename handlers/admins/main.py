import asyncio

import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from magic_filter import F

from data.config import SUPER_ADMIN
from keyboards.default.adminkeys import adm_adm
from keyboards.default.start_dk import main_keyboard
from loader import dp, db, udb
from services.users_json import users


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
    await udb.update_status_true()
    all_users = await udb.select_all_users()
    success_count, failed_count = 0, 0

    for index, user in enumerate(all_users, start=1):
        try:
            await message.copy_to(chat_id=user['telegram_id'])
            success_count += 1
        except aiogram.exceptions.BotBlocked:
            failed_count += 1
            await db.delete_user_tgid(user['telegram_id'])  # Faqat bloklangan foydalanuvchilar o'chiriladi
        except Exception:
            pass

        if index % 1500 == 0:
            await asyncio.sleep(30)  # Yuborishni vaqtincha to'xtatish
        await asyncio.sleep(0.05)  # Bir xabar yuborish orasida kichik kechikish

    await message.answer(
        f"Xabar {success_count} ta foydalanuvchiga muvaffaqiyatli yuborildi!\n"
        f"{failed_count} ta foydalanuvchiga yuborilmadi."
    )
    await db.update_status_false()


@dp.message_handler(F.text == "Count_all_users", user_id=SUPER_ADMIN, state="*")
async def count_users_handler(message: types.Message):
    count = await udb.count_users()
    await message.answer(
        text=f"Foydalanuvchilar soni: {count} ta"
    )


@dp.message_handler(F.text == "add_users", user_id=SUPER_ADMIN)
async def add_users(message: types.Message):
    await message.answer(text="User qo'shish boshlandi!")
    count = 0
    for user in users:
        try:
            count += 1
            await udb.add_user(telegram_id=user)
        except Exception as err:
            pass

    await message.answer(text=f"{count} ta foydalanuvchi qo'shildi!")
