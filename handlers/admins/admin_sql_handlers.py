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
