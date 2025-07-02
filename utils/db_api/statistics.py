from utils.db_api.create_tables import Database


class StatisticsDB:
    def __init__(self, db: Database):
        self.db = db

    async def upsert_statistics(self, chapter_name):
        sql = """
            INSERT INTO statistics (chapter_name, view_count)
            VALUES ($1, 1)
            ON CONFLICT (chapter_name) 
            DO UPDATE SET view_count = statistics.view_count + 1
        """
        return await self.db.execute(sql, chapter_name, execute=True)
