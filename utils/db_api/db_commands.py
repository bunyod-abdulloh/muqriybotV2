from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, telegram_id):
        sql = "INSERT INTO Users (telegram_id) VALUES($1) returning *"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def alter_add_column(self):
        sql = "ALTER TABLE Users ADD COLUMN admin BOOLEAN NULL"
        return await self.execute(sql, fetch=True)

    async def alter_drop_column_blocks(self):
        await self.execute("ALTER TABLE Users DROP COLUMN admin",
                           execute=True)

    async def alter_add_column_blocks(self):
        sql = "ALTER TABLE Users ADD COLUMN blocks BIGINT NULL"
        return await self.execute(sql, fetch=True)

    async def update_admin(self, telegram_id, bool_value):
        sql = f"UPDATE Users SET admin='{bool_value}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_blocked_user(self, telegram_id, blocked_user):
        sql = f"UPDATE Users SET blocks='{blocked_user}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, telegram_id):
        sql = "SELECT * FROM Users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def delete_user_tgid(self, tgid):
        await self.execute("DELETE FROM Users WHERE telegram_id=$1", tgid, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_table_users(self):
        await self.execute("DROP TABLE Users", execute=True)
