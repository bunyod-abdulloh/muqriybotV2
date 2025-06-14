import middlewares, filters, handlers
from aiogram import executor

from loader import dp, db
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    await db.create_tables()
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, allowed_updates=["message", "callback_query", "chat_member"],
                           skip_updates=True)
