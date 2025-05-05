from utils.db_api.users_admins_db import Database


class IlmSuhbatiDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_ilm_suhbati(self, title):
        sql = """ INSERT INTO ilm_suhbati (title) VALUES ($1) RETURNING id """
        return await self.db.execute(sql, title, fetchval=True)
