from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.start_dk import main_keyboard
from loader import dp


@dp.callback_query_handler(text="main_menu", state="*")
async def main_menu_handler(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()

    await call.message.answer(
        text="🏡 Bosh sahifa",
        reply_markup=main_keyboard
    )
    await state.finish()
