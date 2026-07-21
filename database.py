import aiosqlite

DB_NAME = "database.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                history TEXT DEFAULT ''
            )
        """)
        await db.commit()

async def get_history(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT history FROM users WHERE user_id=?",
            (user_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else ""

async def save_history(user_id, history):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO users(user_id, history)
            VALUES(?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET history=excluded.history
        """, (user_id, history))
        await db.commit()
