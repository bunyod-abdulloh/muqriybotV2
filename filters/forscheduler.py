from loader import db
from aiogram import types
from aiogram.dispatcher.filters import Filter


class ForXatmona(Filter):
    async def check(self, message: types.Message):
        xatmona = await db.get_users()[0][0]
        return xatmona
