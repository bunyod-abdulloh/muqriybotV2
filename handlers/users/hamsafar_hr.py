from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.hamsafar_dk import h1, h_empty
from loader import dp, bot, statdb

CHANNEL_ID = -1001793651408


@dp.message_handler(text="🌏 Ҳамсафар", state="*")
async def hvid_hands(msg: types.Message, state:FSMContext):
	await state.finish()
	await msg.answer("🌏 Ҳамсафар",
					 reply_markup = h1)
	await state.set_state("hamsafar_state")


@dp.message_handler(state="hamsafar_state")
async def hamsafar_func(msg: types.Message):
	await statdb.set_statistics(chapter_name="Hamsafar")
	if msg.text in h_empty.keys():
		await bot.copy_message(
			chat_id=msg.from_user.id,
			from_chat_id=CHANNEL_ID,
			message_id=h_empty[msg.text]
		)