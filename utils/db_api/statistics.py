from utils.db_api.create_tables import Database


class StatisticsDB:
    def __init__(self, db: Database):
        self.db = db

    async def upsert_statistics(self, chapter_name: str):
        sql = """
            INSERT INTO statistics (chapter_name, view_count)
            VALUES ($1, 1)
            ON CONFLICT (chapter_name, created_at)
            DO UPDATE SET view_count = statistics.view_count + 1
        """
        return await self.db.execute(sql, chapter_name, execute=True)

    async def get_all_statistics(self):
        sql = """ SELECT created_at, chapter_name, view_count FROM statistics """
        return await self.db.execute(sql, fetch=True)

    async def get_statistics_by_date(self, created_at):
        sql = """ SELECT created_at, chapter_name, view_count FROM statistics WHERE created_at = $1 """
        return await self.db.execute(sql, created_at, fetch=True)
