from utils.db_api.create_tables import Database


class UsersAdminsDB:
    def __init__(self, db: Database):
        self.db = db

    # ==================== USERS ====================
    async def add_user(self, telegram_id):
        sql = "INSERT INTO Users (telegram_id) VALUES($1) ON CONFLICT (telegram_id) DO NOTHING"
        return await self.db.execute(sql, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.db.execute(sql, fetch=True)

    async def select_user(self, telegram_id):
        sql = "SELECT * FROM Users WHERE telegram_id=$1"
        return await self.db.execute(sql, telegram_id, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.db.execute(sql, fetchval=True)

    async def delete_user_tgid(self, tgid):
        await self.db.execute("DELETE FROM Users WHERE telegram_id=$1", tgid, execute=True)

    async def drop_table_users(self):
        await self.db.execute("DROP TABLE Users", execute=True)

    # ==================== ADMIN ====================
    async def add_status(self):
        sql = "INSERT INTO admin (status) VALUES(FALSE)"
        return await self.db.execute(sql, fetchrow=True)

    async def select_status(self):
        sql = "SELECT status FROM admin"
        return await self.db.execute(sql, fetchval=True)

    async def update_status_true(self):
        sql = f"UPDATE admin SET status=TRUE"
        return await self.db.execute(sql, execute=True)

    async def update_status_false(self):
        sql = f"UPDATE admin SET status=FALSE"
        return await self.db.execute(sql, execute=True)

    # ==================== HUSARY ====================
    async def add_husary(self, sura_name, total_verses, zip_, audio):
        sql = "INSERT INTO husary (sura_name, total_verses, zip, audio) VALUES($1, $2, $3, $4)"
        return await self.db.execute(sql, sura_name, total_verses, zip_, audio, fetchrow=True)
