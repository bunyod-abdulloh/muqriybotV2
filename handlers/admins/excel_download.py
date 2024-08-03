from aiogram import types
from aiogram.dispatcher import FSMContext
from openpyxl import Workbook

from keyboards.default.start_dk import main_keyboard
from loader import dp, db, bot


@dp.message_handler(text="Download blocked", state="*")
async def download_active_users(message: types.Message, state: FSMContext):
    users = await db.select_all_users()

    wb = Workbook()
    ws = wb.active

    ws.append(["Blocked Users"])

    for user_id in users:
        ws.append([user_id[1]])

    wb.save("Blocked_Muqriy.xlsx")

    await bot.send_document(
        chat_id=message.from_user.id,
        document=types.InputFile(
            path_or_bytesio="Blocked_Muqriy.xlsx"
        ),
        reply_markup=main_keyboard
    )
