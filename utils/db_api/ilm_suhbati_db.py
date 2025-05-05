from utils.db_api.users_admins_db import Database


class IlmSuhbatiDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_ilm_suhbati_video(self, title, title_id, video):
        sql = """ INSERT INTO ilm_suhbati (title, title_id, video) VALUES ($1, $2, $3) """
        return await self.db.execute(sql, title, title_id, video, fetchval=True)

    async def get_titles(self):
        sql = """ SELECT id, title FROM ilm_suhbati """
        return await self.db.execute(sql, fetch=True)

    async def set_ilm_suhbat_video(self, video_id, row_id):
        sql = """ UPDATE ilm_suhbati SET video = $1 WHERE id = $1 """
        return await self.db.execute(sql, video_id, row_id, execute=True)
