import asyncio

import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ChatMemberUpdated, Message, ReplyKeyboardRemove

from data.config import CHANNEL_ID, CHANNEL_LINK, CHANNEL_TITLE
from keyboards.inline.qversein import check_button
from loader import bot, dp, db
from utils.misc import subscription
from keyboards.default.start_dk import main_keyboard


@dp.message_handler(commands=['start'], state="*")
async def show_channels(message: Message, state: FSMContext):
    await message.answer(message.text)
    try:
        await db.add_user(message.from_user.id)
    except asyncpg.exceptions.UniqueViolationError:
        pass
    else:
        pass
    channels_format = f"👉 <a href='{CHANNEL_LINK}'>{CHANNEL_TITLE}</a>\n"
    await message.answer(
        "Ассалому алайкум!\nБу бот орқали Сиз Ҳасанхон Яҳё Абдулмажид қори дарсликларини аудио ва видео "
        "шаклда кўришингиз ва эшитишингиз мумкин.", reply_markup=ReplyKeyboardRemove())
    await message.answer(f"Ботни ишлатиш учун қуйидаги каналимизга обуна бўлинг\n"
                         f"{channels_format}", reply_markup=check_button, disable_web_page_preview=True)
    await state.finish()


@dp.chat_member_handler(state='*')
async def members(message: ChatMemberUpdated):
    status = message.new_chat_member.status
    user_id = int(message.from_user.id)
    if status == 'left' or status == 'kicked':
        channels_format = f" 👉 <a href='{CHANNEL_LINK}'>{CHANNEL_TITLE}</a>\n"

        await bot.send_message(chat_id=user_id,
                               text=f'Сиз, {channels_format}каналимиздан чиқиб кетдингиз!'
                                    '\nБотимиздан фойдаланиш имконияти чекланди!',
                               reply_markup=ReplyKeyboardRemove())
        await db.delete_user_tgid(user_id)
    else:
        await bot.send_message(chat_id=user_id,
                               text='Сиз каналимизга аъзо бўлдингиз! Ботимиздан фойдаланишингиз мумкин!',
                               reply_markup=main_keyboard)


@dp.message_handler(text="🏡 Бош саҳифа", state="*")
async def boshmenyu_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="🏡 Бош саҳифа",
        reply_markup=main_keyboard
    )

    await state.finish()


@dp.callback_query_handler(text="check_subs")
async def checker(call: CallbackQuery):
    await call.answer()

    status = await subscription.check(user_id=call.from_user.id,
                                      channel=CHANNEL_ID)

    if status:
        result = f"<b>{CHANNEL_TITLE}</b> каналимизга обуна бўлгансиз!\n\n"
        await call.message.answer(result, reply_markup=main_keyboard, disable_web_page_preview=True)

    else:
        result = (f"Сиз, 👉 <a href='{CHANNEL_LINK}'>{CHANNEL_TITLE}</a>\nканалига обуна бўлмагансиз"
                  f"\n<a href='{CHANNEL_LINK}'>Обуна бўлиш</a>")
        await call.message.answer(result, disable_web_page_preview=True)


@dp.message_handler(text='id', state='*')
async def idolish_admin(message: Message, state: FSMContext):
    await message.answer("ID OLISH YOQILDI! VIDEO YOKI RASMLARNI JO'NATISHINGIZ MUMKIN!")
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
