from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import SUPER_ADMIN
from keyboards.default.adminkeys import adm_adm, admin_sql_buttons
from loader import dp, db
from states.admin_states import AdminSqlButtons


@dp.message_handler(text="Sql buttons", state="*")
async def admin_sql_btn(message: types.Message):
    await message.answer(text=message.text, reply_markup=admin_sql_buttons)
    await AdminSqlButtons.main.set()


@dp.message_handler(state=AdminSqlButtons.main)
async def add_column_admin_handler(message: types.Message, state: FSMContext):
    if message.text == "Delete blocked users":
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
    elif message.text == "🔙 Ortga":
        await message.answer(text=message.text,
                             reply_markup=adm_adm)
        await state.finish()


@dp.message_handler(text="Count_all_users", user_id=SUPER_ADMIN, state="*")
async def count_users_handler(message: types.Message):
    count = await db.count_users()
    await message.answer(
        text=f"Umumiy foydalanuvchilar soni: {count} ta"
    )


@dp.message_handler(text="Count_blocked_users", user_id=SUPER_ADMIN, state="*")
async def count_blocked_users_handler(message: types.Message):
    blocked = await db.count_blocked_users()
    await message.answer(
        text=f"\nBotni block qilgan foydalanuvchilar soni: {blocked} ta"
    )
