from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import CHANNEL_ID, CHANNEL_LINK, CHANNEL_TITLE
from utils.misc import subscription
from loader import bot


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
            if update.message.text in ['/start', '/help']:
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data == 'check_subs':
                return
        else:
            return
        result = "Ботдан фойдаланиш учун қуйидаги каналимизга обуна бўлинг:\n "
        final_status = True

        status = await subscription.check(user_id=user,
                                          channel=CHANNEL_ID)
        final_status *= status

        if not status:
            result += f"👉 <a href='{CHANNEL_LINK}'>{CHANNEL_TITLE}</a>\n"

        if not final_status:
            await update.message.answer(result, disable_web_page_preview=True)
            raise CancelHandler()
