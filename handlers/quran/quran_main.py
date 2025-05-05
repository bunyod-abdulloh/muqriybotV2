from aiogram import types
from magic_filter import F

from loader import dp


@dp.message_handler(F.text == "📖 Qur'oni Karim")
async def quran_main_handler(message: types.Message):
    await message.answer(
        text=message.text, reply_markup=None  # quran_main_buttons()
    )
