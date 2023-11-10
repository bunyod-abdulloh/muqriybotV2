import asyncio
import logging
import asyncpg

from aiogram import types
from aiogram.dispatcher import FSMContext
from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from keyboards.default.adminkeys import adm_adm
from keyboards.default.start_dk import main_keyboard
from keyboards.inline.elon_keys import yes_no

from data.config import ADMINS
from loader import dp, bot, db, sdb
from states.sos_states import AddAdmin

addbutton = InlineKeyboardMarkup(row_width=2)
addbutton.add(InlineKeyboardButton(text="👮‍♂️ Adminlarni ko'rish", callback_data='admin_see'))
addbutton.add(InlineKeyboardButton(text="➕ Qo'shish", callback_data='admin_add'))

delbutton = InlineKeyboardMarkup(row_width=2)
delbutton.insert(InlineKeyboardButton(text='⬅ Ortga', callback_data='admin_back'))
delbutton.insert(InlineKeyboardButton(text="❌ O'chirish", callback_data='admin_del'))

habar = "\nAvvalgi habarga javob olingan yo'qligini tekshirib ko'ring!"


@dp.message_handler(text='/id', state='*')
async def idaniqlash(msg: Message):
    await msg.answer(f'Сизнинг ID рақамингиз:\n\n<code>{msg.from_user.id}</code>')


@dp.message_handler(text="🏡 Бош меню", state="*")
async def boshmenyu_func(msg: types.Message, state: FSMContext):
    try:
        await db.add_user(telegram_id=msg.from_user.id)
    except asyncpg.exceptions.UniqueViolationError:
        pass
    await msg.answer("🏡 Бош меню", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(text=['/admins'], user_id=ADMINS, state="*")
async def buttons(msg: types.Message, state: FSMContext):
    admins = await sdb.all_admins()
    if len(admins) == 0:
        await sdb.add_admins(user_id=int(ADMINS),
                             fullname="Бош админ")
    await msg.answer('Админ бош менюси', reply_markup=adm_adm)


@dp.message_handler(text='users', user_id=ADMINS)
async def admin_count_users(msg: Message):
    count = await db.count_users()
    await msg.answer(f"\nBazada {count} ta foydalanuvchi mavjud")


@dp.message_handler(text='Forward ON', user_id=ADMINS)
async def admin_forward_state(msg: Message, state: FSMContext):
    await msg.answer(f"<b>FORWARD STATE</b> yoqildi!{habar}")
    await state.set_state("forw")


@dp.message_handler(text='MediaGroup ON', user_id=ADMINS)
async def admin_mediagr_state(msg: Message, state: FSMContext):
    await msg.answer(f"<b>MEDIA GROUP STATE</b> yoqildi!{habar}")
    await state.set_state("mediagroup")


@dp.message_handler(text='ID ON', user_id=ADMINS)
async def admin_id_state(msg: Message, state: FSMContext):
    await msg.answer(f"<b>ID OLISH STATE</b> yoqildi!{habar}")
    await state.set_state("idolish")


@dp.message_handler(text='Sending messages', user_id=ADMINS)
async def admin_sendmes_state(msg: Message, state: FSMContext):
    await msg.answer(f"<b>E'LON JO'NATISH STATE</b> yoqildi!{habar}")
    await state.set_state("elon")


@dp.message_handler(text="Admin qo'shish/o'chirish", user_id=ADMINS)
async def admin_add_state(msg: Message, state: FSMContext):
    await msg.answer('Тугмалардан бирини танланг:', reply_markup=addbutton)


@dp.callback_query_handler(text='admin_add', state='*')
async def adminadd(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer('Yangi admin ismini kiriting:')
    await AddAdmin.one.set()


@dp.message_handler(state=AddAdmin.one)
async def addadminone(msg: Message, state: FSMContext):
    await state.update_data({'admin_name': msg.text})
    await msg.answer('ID raqamini kiriting:')
    await AddAdmin.two.set()


@dp.message_handler(state=AddAdmin.two)
async def addadmintwo(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        data = await state.get_data()
        await sdb.add_admins(user_id=int(msg.text),
                             fullname=data['admin_name'])
        await msg.answer("Yangi admin qo'shildi")
        await state.finish()
    else:
        await msg.answer('Iltimos, faqat raqam kiriting!')


@dp.callback_query_handler(text='admin_see', state='*')
async def onedel(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    admins = await sdb.all_admins()
    if len(admins) == 0:
        await call.message.answer("Bazadan barcha barcha adminlar o'chirilgan! Iltimos, /admins buyrug'ini qayta "
                                  "kiriting!")
        await state.finish()
    for n in admins:
        await call.message.answer(f'Admin: <b>{n[2]}</b>\n\nID raqam: <b>{n[1]}</b>',
                                  reply_markup=delbutton)
    await AddAdmin.three.set()


@dp.callback_query_handler(state=AddAdmin.three)
async def addadminone(call: CallbackQuery, state: FSMContext):
    if call.data == 'admin_back':
        await call.message.answer('⬅ Ortga', reply_markup=addbutton)
    elif call.data == 'admin_del':
        user_id = call.message.text.split()
        await sdb.delete_admin(user_id=int(user_id[-1]))
        await call.answer(text="Admin bazadan o'chirildi!", show_alert=True)
    await call.message.delete()
    await state.finish()


@dp.message_handler(content_types=['any'], user_id=ADMINS,
                    state="forw")
async def contumum(message: types.Message, state: FSMContext):

    content_type = ["audio", "video", "voice", "document", "photo", "text"]

    if message.text == 'Forward OFF':
        await message.answer(
            text="Forward ON state o'chirildi!"
        )
        await state.finish()
    else:
        if message.content_type in content_type:

            await message.answer(
                text=f"Habar yuborilganligi haqidagi to'liq ma'lumot tez orada yuboriladi!",
                reply_markup=main_keyboard
            )
            await state.finish()

            users = await db.select_all_users()
            count_baza = await db.count_users()
            active = 0
            block = 0
            count_one = 0
            count_two = 0

            for user in users:
                user_id = user[1]
                try:
                    await message.forward(
                        chat_id=user_id
                    )
                    active += 1

                except Exception:
                    block += 1
                    continue

                count_one += 1
                count_two += 1

                if count_one == 25:
                    count_one = 0
                    await asyncio.sleep(0.5)

                if count_two == 1500:
                    await asyncio.sleep(30)
                    count_two = 0

            await state.finish()
            await message.answer(f"SENT: {active}"
                                 f"\nBLOCK: {block}"
                                 f"\nALL_USERS: {count_baza}")

    active = 0
    block = 0
    count_one = 0
    count_two = 0


@dp.message_handler(is_media_group=True, content_types=types.ContentType.ANY, state="mediagroup")
async def mediagr(message: types.Message, album: List[types.Message], state: FSMContext):
    media_group = types.MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id
        try:
            media_group.attach({"media": file_id,
                                "type": obj.content_type,
                                "caption": obj.caption})
        except Exception as err:
            logging.exception(err)
            return await message.answer("Бу альбомни aiogram қўлламайди!")

    users = await db.select_all_users()
    count_baza = await db.count_users()
    active = 0
    block = 0
    count_one = 0
    count_two = 0
    await message.answer(
        text=f"Habar yuborilganligi haqidagi to'liq ma'lumot tez orada yuboriladi!",
        reply_markup=main_keyboard
    )
    for user in users:
        user_id = user[1]
        try:
            await bot.send_media_group(
                chat_id=user_id,
                media=media_group
            )
            active += 1

        except Exception:
            block += 1
            continue

        count_one += 1
        count_two += 1

        if count_one == 25:
            count_one = 0
            await asyncio.sleep(0.5)

        if count_two == 1500:
            await asyncio.sleep(30)
            count_two = 0

    await state.finish()
    await message.answer(
        text=f"SENT: {active}"
             f"\nBLOCK: {block}"
             f"\nALL_USERS: {count_baza}")

    active = 0
    block = 0
    count_one = 0
    count_two = 0


@dp.message_handler(state="mediagroup")
async def mediagryopish(msg: types.Message, state: FSMContext):
    if msg.text == "MediaGroup OFF":
        await msg.answer("<b>MEDIA GROUP STATE</b> o'chirildi!")
        await state.finish()


@dp.message_handler(content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'], user_id=ADMINS,
                    state="idolish")
async def idvideo(message: types.Message, state: FSMContext):
    if message.video:
        await message.answer(
            text=f"<b>VIDEO/CAPTION:</b> \n\n{message.caption}"
                 f"<b>\n\nVIDEO/ID:</b> \n\n{message.video.file_id}"
        )
    if message.audio:
        await message.answer(
            text=f"<b>AUDIO/CAPTION:</b> \n\n{message.caption}"
                 f"\n\n<b>AUDIO/ID:</b>\n\n{message.audio.file_id}"
        )
    if msg.voice:
        await msg.answer(
            text=f"<b>AUDIO/CAPTION:</b> \n\n{msg.caption}"
                 f"\n\n<b>AUDIO/ID:</b>\n\n{msg.voice.file_id}"
        )
    if msg.photo:
        await msg.answer(
            text=f"<b>PHOTO/CAPTION:</b>\n\n{msg.caption}"
                 f"\n\n<b>PHOTO/ID:</b>\n\n{msg.photo[-1].file_id}"
        )
    if msg.document:
        await msg.answer(
            text=f"<b>DOCUMENT/CAPTION:</b>\n\n{msg.caption}"
                 f"\n\n<b>DOCUMENT/ID:</b>\n\n{msg.document.file_id}"
        )

    if msg.text == "ID OFF":
        await msg.answer(
            text="<b>ID OLISH STATE</b> o'chirildi!"
        )
        await state.finish()

    elif msg.text:
        await msg.answer(
            text="Siz <b>ID OLISH STATE</b>dasiz."
                 "\n\nChiqish uchun <b>ID o'chirish</b> tugmasinig bosing!"
        )


@dp.message_handler(content_types=['text'], state="elon", user_id=ADMINS)
async def elonj(msg: types.Message, state: FSMContext):
    if msg.text == "Cancel sending messages":
        await msg.answer("<b>E'LON JO'NATISH STATE</b> o'chirildi!")
        await state.finish()

    elif msg.text:
        matn = msg.text
        await msg.answer(
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
        await call.message.answer(
            text=f"Habar yuborilganligi haqidagi to'liq ma'lumot tez orada yuboriladi!",
            reply_markup=main_keyboard
        )
        await state.finish()

        for user in users:
            user_id = user[1]
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=data['text']
                )
                active += 1

            except Exception:
                block += 1
                continue

            count_one += 1
            count_two += 1

            if count_one == 25:
                count_one = 0
                await asyncio.sleep(0.5)

            if count_two == 1500:
                await asyncio.sleep(30)
                count_two = 0

        await call.message.answer(f"SENT: {active}"
                                  f"\nBLOCK: {block}"
                                  f"\nALL_USERS: {count_baza}")

    elif call.data == "no_again":
        await call.message.answer(
            text="Habaringizni qayta yuborishingiz mumkin!"
        )
        await state.set_state("elon")

    active = 0
    block = 0
    count_one = 0
    count_two = 0
