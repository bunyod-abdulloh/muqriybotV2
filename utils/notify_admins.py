import logging

from aiogram import Dispatcher

from data.config import SUPER_ADMIN


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(
            chat_id=SUPER_ADMIN,
            text="Bot ishga tushdi!"
        )
    except Exception as err:
        logging.exception(err)
