from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from data import config
from data.config import REDIS_PASS
from utils.db_api.ilm_suhbati_db import IlmSuhbatiDB
from utils.db_api.statistics import StatisticsDB
from utils.db_api.users_admins_db import Database, UsersAdminsDB

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(host='localhost', port=6379, password=REDIS_PASS)
dp = Dispatcher(bot, storage=storage)
db = Database()
udb = UsersAdminsDB(db=db)
ilmdb = IlmSuhbatiDB(db=db)
statdb = StatisticsDB(db=db)
