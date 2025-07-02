from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from data.config import TAROVEH_1444
from keyboards.default.audio_video_dk import alldk
from loader import dp, bot, statdb
from states.taroveh_states import TarovehTitle, TarovehAudio, TarovehVideo

audio_dict = {'1 - 5': [2040, 2052, 2053, 2055, 2056], '6 - 10': [2057, 2058, 2059, 2060, 2061],
              '11 - 15': [2062, 2063, 2064, 2065, 2066], '16 - 20': [2067, 2068, 2069, 2070, 2071],
              '21 - 25': [2072, 2073, 2074, 2075, 2076], '26 - 27': [2077, 2078]}

video_dict = {1: 2083, 2: 2084, 3: 2085, 4: 2086, 5: 2087, 6: 2088, 7: 2089, 8: 2090, 9: 2091, 10: 2092, 11: 2093,
              12: 2094, 13: 2095, 14: 2096, 15: 2097, 16: 2098, 17: 2099, 18: 2100, 19: 2101, 20: 2102, 21: 2103,
              22: 2104, 23: 2105, 24: 2106, 25: 2107, 26: 2108, 27: 2109}

markup_audio = InlineKeyboardMarkup(row_width=5)
for k in audio_dict.keys():
    markup_audio.insert(InlineKeyboardButton(text=str(k), callback_data=str(k)))
markup_audio.add(InlineKeyboardButton(text='⬅️ Ortga', callback_data='back_audio'))

markup_video = InlineKeyboardMarkup(row_width=4)
for n in range(1, 28):
    markup_video.insert(InlineKeyboardButton(text=f"{n} - kun", callback_data=f"{n}"))
markup_video.add(InlineKeyboardButton(text='⬅️ Ortga', callback_data='back_video'))

markup_back = InlineKeyboardMarkup(row_width=1)
markup_back.add(InlineKeyboardButton(text='⬅️ Ortga', callback_data='back_back'))


@dp.message_handler(text='📌 Таровеҳ намози 1444', state='*')
async def t1444_one(m: Message):
    await statdb.upsert_statistics(chapter_name="Taroveh 1444")
    await m.answer(m.text, reply_markup=alldk)
    await TarovehTitle.one.set()


@dp.message_handler(state=TarovehTitle.one)
async def t1444_two(m: Message):

    if m.text == '🎧 Ayдиo':
        await m.answer(m.text, reply_markup=markup_audio)
        await TarovehAudio.one.set()

    elif m.text == '🎬 Видео':
        await m.answer(m.text, reply_markup=markup_video)
        await TarovehVideo.one.set()


@dp.callback_query_handler(state=TarovehAudio.one)
async def t1444_three(c: CallbackQuery):
    await c.message.delete()

    if c.data == 'back_audio':
        await c.message.answer('📌 Таровеҳ намози 1444', reply_markup=alldk)
        await TarovehTitle.one.set()

    elif c.data in audio_dict.keys():
        for n in audio_dict[c.data]:
            await bot.copy_message(chat_id=c.from_user.id,
                                   from_chat_id=TAROVEH_1444,
                                   message_id=n,
                                   reply_markup=markup_back)
        await TarovehAudio.two.set()


@dp.callback_query_handler(state=TarovehAudio.two)
async def t1444_four(c: CallbackQuery):

    if c.data == 'back_back':
        await c.message.answer('📌 Таровеҳ намози 1444', reply_markup=markup_audio)
        await TarovehAudio.one.set()


@dp.callback_query_handler(state=TarovehVideo.one)
async def t1444_five(call: CallbackQuery):
    await call.message.delete()

    if call.data == 'back_video':
        await call.message.answer('📌 Таровеҳ намози 1444', reply_markup=alldk)
        await TarovehTitle.one.set()

    elif int(call.data) in video_dict.keys():
        await bot.copy_message(chat_id=call.from_user.id,
                               from_chat_id=TAROVEH_1444,
                               message_id=video_dict[int(call.data)],
                               reply_markup=markup_back)
        await TarovehVideo.two.set()


@dp.callback_query_handler(state=TarovehVideo.two)
async def t1444_six(call: CallbackQuery):
    await call.message.delete()

    if call.data == 'back_back':
        await call.message.answer('📌 Таровеҳ намози 1444', reply_markup=markup_video)
        await TarovehVideo.one.set()
