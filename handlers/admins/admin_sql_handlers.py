from aiogram import types

from data.config import ADMINS
from keyboards.default.adminkeys import adm_adm
from loader import dp, db


@dp.message_handler(text="Add column admin", user_id=ADMINS, state="*")
async def add_column_admin_handler(message: types.Message):
    await db.alter_add_column_admin()
    await message.answer(
        text="Admin ustuni ma'lumotlar omboriga qo'shildi"
    )


@dp.message_handler(text="Add column blocks", user_id=ADMINS, state="*")
async def alter_table_admin(message: types.Message):
    await db.alter_add_column_blocks()
    await message.answer(
        text="Blocks ustuni qo'shildi!"
    )


@dp.message_handler(text="Drop table blocks", user_id=ADMINS, state="*")
async def drop_blocks_handler(message: types.Message):
    await db.alter_drop_column_blocks()
    await message.answer(
        text="Blocks ustuni o'chirildi!"
    )


@dp.message_handler(text="Count_all_users", user_id=ADMINS, state="*")
async def count_users_handler(message: types.Message):
    count = await db.count_users()
    await message.answer(
        text=f"Umumiy foydalanuvchilar soni: {count} ta"
    )


@dp.message_handler(text="Count_blocked_users", user_id=ADMINS, state="*")
async def count_blocked_users_handler(message: types.Message):
    blocked = await db.count_blocked_users()
    await message.answer(
        text=f"\nBotni block qilgan foydalanuvchilar soni: {blocked} ta"
    )


@dp.message_handler(text="Delete blocked users", user_id=ADMINS, state="*")
async def delete_blocked_users_admin(message: types.Message):
    blocked_users = await db.select_all_users()

    c = 0
    for user in blocked_users:
        if user[3] is not None:
            c += 1
            await db.delete_user_tgid(
                tgid=user[3]
            )
    await message.answer(
        text=f"Jami {c} ta foydalanuvchi ma'lumotlar omboridan o'chirildi!"
    )
    c = 0


@dp.message_handler(text="🔙 Ortga", state="*")
async def admin_back_button(message: types.Message):
    await message.answer(text=message.text,
                         reply_markup=adm_adm)
