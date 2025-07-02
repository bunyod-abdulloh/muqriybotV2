import asyncio
from datetime import datetime

import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from magic_filter import F

from data.config import SUPER_ADMIN
from keyboards.default.adminkeys import adm_adm
from keyboards.default.start_dk import main_keyboard
from keyboards.inline.admin import key_returner
from loader import dp, udb, statdb
from services.admin import extracter, process_page
from states.admin_states import AdminStates


@dp.message_handler(Command('admins'), user_id=SUPER_ADMIN, state="*")
async def admin_main_handler(message: types.Message):
    await message.answer(
        text='Admin bosh menyusi',
        reply_markup=adm_adm
    )


@dp.message_handler(F.text == "E'lon yuborish", user_id=SUPER_ADMIN)
async def admin_sendmes_state(message: types.Message, state: FSMContext):
    send_status = await udb.select_status()

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
            await udb.delete_user_tgid(user['telegram_id'])
        except Exception:
            pass

        if index % 1500 == 0:
            await asyncio.sleep(30)
        await asyncio.sleep(0.05)

    await message.answer(
        f"Xabar {success_count} ta foydalanuvchiga muvaffaqiyatli yuborildi!\n"
        f"{failed_count} ta foydalanuvchiga yuborilmadi."
    )
    await udb.update_status_false()


@dp.message_handler(F.text == "Foydalanuvchilar soni", user_id=SUPER_ADMIN, state="*")
async def count_users_handler(message: types.Message):
    count = await udb.count_users()
    await message.answer(
        text=f"Foydalanuvchilar soni: {count} ta"
    )


@dp.message_handler(F.text == "Barcha statistika", state="*", user_id=SUPER_ADMIN)
async def handle_all_statistics(message: types.Message, state: FSMContext):
    await state.finish()

    all_statistics = await statdb.get_all_statistics()

    extract = extracter(all_medias=all_statistics, delimiter=10)
    current_page = 1
    all_pages = len(extract)
    extracted_data = extract[current_page - 1]

    text = "\n".join(
        f"{n['created_at']} | {n['chapter_name']} - {n['view_count']}" for n in extracted_data
    )

    await message.answer(
        text=text,
        reply_markup=key_returner(current_page=current_page, all_pages=all_pages)
    )


@dp.callback_query_handler(F.data.startswith("prev_stat:"), state="*")
async def handle_stat_prev(call: types.CallbackQuery):
    await process_page(call=call, direction="prev")


@dp.callback_query_handler(F.data.startswith("next_stat:"))
async def handle_stat_next(call: types.CallbackQuery):
    await process_page(call, direction="next")


@dp.callback_query_handler(F.data.startswith("alert_stat:"))
async def handle_stat_alert(call: types.CallbackQuery):
    current_page = call.data.split(":")[1]
    await call.answer(text=f"Siz {current_page} - sahifadasiz", show_alert=True)


@dp.message_handler(F.text == "Sana bo'yicha", state="*", user_id=SUPER_ADMIN)
async def handle_stat_by_date(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(text="Sanani kiriting\n\nNamuna: 2025-12-30")
    await AdminStates.GET_STATISTICS.set()


@dp.message_handler(state=AdminStates.GET_STATISTICS, content_types=types.ContentType.TEXT)
async def handle_stat_by_date_two(message: types.Message, state: FSMContext):
    try:
        date_obj = datetime.strptime(message.text.strip(), "%Y-%m-%d").date()
    except ValueError:
        return await message.answer("❌ Sana noto‘g‘ri formatda. To‘g‘ri format: YYYY-MM-DD (masalan: 2025-12-30)")

    stat_by_date = await statdb.get_statistics_by_date(created_at=date_obj)

    if not stat_by_date:
        return await message.answer("ℹ️ Ko‘rsatilgan sana uchun statistika topilmadi.")

    text = ""
    for index, stat in enumerate(stat_by_date, start=1):
        text += f"{index}. {stat['created_at']} | {stat['chapter_name']} - {stat['view_count']}\n"

    await message.answer(text=text)
    await state.finish()
    return None
