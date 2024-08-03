from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
SUPER_ADMIN = env.str("SUPER_ADMIN")
IP = env.str("IP")
CHANNELS = env.list("CHANNELS")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
