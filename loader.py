from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.ilm_suhbati_db import IlmSuhbatiDB
from utils.db_api.users_admins_db import Database, UsersAdminsDB

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
udb = UsersAdminsDB(db)
ilmdb = IlmSuhbatiDB(db)

