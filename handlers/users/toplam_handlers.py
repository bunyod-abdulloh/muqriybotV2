from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from handlers.users.ilmiysuhbatlar_hr import CHANNEL_ID
from keyboards.default.ilmiysuhbatlar_dk import ilmiy_suhbatlar_home_page, audio_video_page
from keyboards.inline.ilmiy_suhbatlar_harxil import tort_suhbat_video, tort_suhbat_audio, ilm_suhbat_inkeys
from loader import dp, bot
from states.toplam_states import TortToplam


def collection_four():
    text = ('1. "Kompas - liderlar akademiyasi"da "Oilaviy munosabatlar" mavzusida tashkil etilgan suhbat'
            '\n2. «Kitobxonlik maktabi» loyihasining maxsus soni chaqiruv xatmonasi'
            '\n3. Radikal ateistlar, feminizm, terrorizm, gender tengligi va johil musulmonlar'
            '\n4. Islomda hamjihatlik tinchlik garovi'
            '\n5. "Munosib beka tayyorlash va ularni jamiyatga taqdim etish"'
            '\n6. SSSR taqiqlagan ibodat. Hasanxon Yahyo Abdulmajid va Olimjon G‘ulomov bilan | "Fikrat"'
            '\n7. Islom to‘g‘ri o‘rganilsa, hamma zamonga mos keladi. 13 yoshida qori bo‘lgan qori bilan suhbat'
            '\n8. Arab tili va eski o‘zbek yozuvini o‘rganishning ahamiyati'
            '\n9. Bilganlar bilan bilmaganlar teng bo‘ladimi? "Najot Ta’lim" o‘quv markazida bo‘lib o‘tgan suhbat'
            '\n10. "Rasululloh - ulug‘ ne’mat"'
            '\n11. Ilm olishning hayotimizdagi o‘rni'
            '\n12. Ayol kishi pul topishi kerakmi?'
            '\n13. Ustoz Hasanxon Yahyo Abdulmajid bilan ochiq suhbat'
            '\n14. Ustozlar bilan jonli suhbat'
            '\n15. Islom bilan biznes qilganlar'
            '\n16. Hasanxon Yahyo Abdulmajid bilan psixogenetika mavzusida suhbat'
            '\n17. Jamiyatimizga qanday jinsiy tarbiya kerak?')
    return text


@dp.message_handler(state="tortt")
async def jonlifunc(msg: Message, state: FSMContext):
    if msg.text == "⏮ Олдинги":
        await msg.answer("⏮ Олдинги",
                         reply_markup=await ilmiy_suhbatlar_home_page())
        await state.set_state("ilmsuh")
    elif msg.text == "🎬 Видео":
        await msg.answer(text=collection_four(), reply_markup=await ilm_suhbat_inkeys(torttoplam=True))
        message = await msg.answer('Видео', reply_markup=ReplyKeyboardRemove())
        await message.delete()
        await TortToplam.video_one.set()

    elif msg.text == "🎧 Ayдиo":
        await msg.answer(text=await tort_suhbatlar(), reply_markup=await ilm_suhbat_inkeys(torttoplam=True))
        message = await msg.answer('Аудио', reply_markup=ReplyKeyboardRemove())
        await message.delete()
        await TortToplam.audio_one.set()


@dp.callback_query_handler(state=TortToplam.video_one)
async def tort_video_one(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
        if call.data in tort_suhbat_video.keys():
            await bot.copy_message(chat_id=call.from_user.id, from_chat_id=CHANNEL_ID,
                                   message_id=tort_suhbat_video[call.data],
                                   reply_markup=await ilm_suhbat_inkeys(back=True))
            await TortToplam.video_two.set()
        elif call.data == 'back_tash_suh2':
            await call.message.answer('⬅ Ортга', reply_markup=audio_video_page)
            await state.set_state("tortt")
    except Exception:
        pass


@dp.callback_query_handler(state=TortToplam.video_two)
async def torttoplam_video_two(call: CallbackQuery):
    try:
        await call.message.delete()
        if call.data == 'back_tash_suh1':
            await call.message.answer(text=await tort_suhbatlar(), reply_markup=await ilm_suhbat_inkeys(
                torttoplam=True))
            await TortToplam.video_one.set()
    except Exception:
        pass


@dp.callback_query_handler(state=TortToplam.audio_one)
async def torttoplam_audio_one(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
        if call.data in tort_suhbat_audio.keys():
            await bot.copy_message(chat_id=call.from_user.id, from_chat_id=CHANNEL_ID,
                                   message_id=tort_suhbat_audio[call.data],
                                   reply_markup=await ilm_suhbat_inkeys(back=True))
            await TortToplam.audio_two.set()
        elif call.data == 'back_tash_suh2':
            await call.message.answer('⬅ Ортга', reply_markup=audio_video_page)
            await state.set_state("tortt")
    except Exception:
        pass


@dp.callback_query_handler(state=TortToplam.audio_two)
async def torttoplam_audio_two(call: CallbackQuery):
    try:
        await call.message.delete()
        if call.data == 'back_tash_suh1':
            await call.message.answer(text=await tort_suhbatlar(), reply_markup=await ilm_suhbat_inkeys(torttoplam=True))
            await TortToplam.audio_one.set()
    except Exception:
        pass
