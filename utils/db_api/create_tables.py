from typing import Union

import asyncpg
from asyncpg import Pool, Connection

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

    async def create_tables(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS Users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT NOT NULL UNIQUE        
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS admin(
                id SERIAL PRIMARY KEY,
                status BOOLEAN DEFAULT FALSE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS husary (
                id SERIAL PRIMARY KEY,
                sura_name VARCHAR(60) NULL,
                total_verses INTEGER NULL,
                zip VARCHAR(200) NULL,
                audio VARCHAR(200) NULL                     
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS ilm_suhbati (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NULL,
                title_id INTEGER NULL,                
                audio INTEGER NULL,
                video INTEGER NULL                 
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS statisticts (
                id SERIAL PRIMARY KEY,
                chapter_name VARCHAR(255) NULL UNIQUE,
                view_count INTEGER DEFAULT 1
            ); 
            """
        ]
        for query in queries:
            await self.execute(query, execute=True)
