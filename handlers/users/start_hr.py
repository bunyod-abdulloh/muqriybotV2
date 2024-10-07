import asyncio

import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ChatMemberUpdated, Message, ReplyKeyboardRemove

from data.config import CHANNELS
from keyboards.inline.qversein import check_button
from loader import bot, dp, db
from utils.misc import subscription
from keyboards.default.start_dk import main_keyboard


@dp.message_handler(commands=['start'], state="*")
async def show_channels(msg: Message, state: FSMContext):
    channels_format = str()
    chat = await bot.get_chat(CHANNELS)
    invite_link = await chat.export_invite_link()
    channels_format += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"
    await msg.answer("Ассалому алайкум!\nБу бот орқали Сиз Ҳасанхон Яҳё Абдулмажид қори дарсликларини аудио ва видео "
                     "шаклда кўришингиз ва эшитишингиз мумкин.", reply_markup=ReplyKeyboardRemove())
    await msg.answer(f"Ботни ишлатиш учун қуйидаги каналимизга обуна бўлинг\n"
                     f"{channels_format}", reply_markup=check_button, disable_web_page_preview=True)
    await state.finish()


@dp.chat_member_handler(state='*')
async def members(msg: ChatMemberUpdated):
    user_id = msg.new_chat_member.user.id
    try:
        if msg.new_chat_member.status == 'member':
            await bot.send_message(chat_id=user_id,
                                   text='Сиз каналимизга аъзо бўлдингиз! Ботимиздан фойдаланишингиз мумкин!',
                                   reply_markup=main_keyboard)
            try:
                await db.add_user(telegram_id=msg.from_user.id)
            except asyncpg.exceptions.UniqueViolationError:
                pass

        elif msg.new_chat_member.status == 'left':
            channels_format = str()
            for channel in CHANNELS:
                chat = await bot.get_chat(channel)
                invite_link = await chat.export_invite_link()
                channels_format += f" 👉 <a href='{invite_link}'>{chat.title}</a>\n"

            await bot.send_message(chat_id=user_id,
                                   text=f'Сиз, {channels_format}каналимиздан чиқиб кетдингиз!'
                                        '\nБотимиздан фойдаланиш имконияти чекланди!',
                                   reply_markup=ReplyKeyboardRemove())
            await db.delete_user_tgid(msg.from_user.id)
    except Exception:
        pass


@dp.message_handler(text="🏡 Бош саҳифа", state="*")
async def boshmenyu_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_in_db = await db.select_user(
        telegram_id=user_id
    )

    await message.answer(
        text="🏡 Бош саҳифа",
        reply_markup=main_keyboard
    )
    if user_in_db is None:
        await db.add_user(telegram_id=message.from_user.id)
    await state.finish()


@dp.callback_query_handler(text="check_subs")
async def checker(call: CallbackQuery):
    await call.answer()
    result = str()
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            result += f"<b>{channel.title}</b> каналимизга обуна бўлгансиз!\n\n"
            await call.message.answer(result, reply_markup=main_keyboard, disable_web_page_preview=True)
            user_id = call.from_user.id
            user_in_db = await db.select_user(
                telegram_id=user_id
            )
            if user_in_db is None:
                await db.add_user(telegram_id=user_id)

        else:
            invite_link = await channel.export_invite_link()
            result += (f"Сиз, 👉 <a href='{invite_link}'>{channel.title}</a>\nканалига обуна бўлмагансиз"
                       f"\n<a href='{invite_link}'>Обуна бўлиш</a>")
            await call.message.answer(result, disable_web_page_preview=True)


@dp.message_handler(text='id', state='*')
async def idolish_admin(msg: Message, state: FSMContext):
    await msg.answer("ID OLISH YOQILDI! VIDEO YOKI RASMLARNI JO'NATISHINGIZ MUMKIN!")
    await state.set_state('admin_id')


@dp.message_handler(content_types=['any'], state='admin_id')
async def get_id(message: types.Message):
    await asyncio.sleep(2)
    
    if message.content_type == 'animation':
        await message.answer(text=f"<code>{message.animation.file_id}</code>")

    if message.content_type == 'audio':
        await message.answer(text=f"<code>{message.audio.file_id}</code>")

    if message.content_type == 'video':
        await message.answer(text=f"<code>{message.video.file_id}</code>")

    if message.content_type == 'photo':
        await message.answer(text=f"<code>{message.photo[-1].file_id}</code>")
