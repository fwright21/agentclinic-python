import aiosqlite
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = Path(__file__).parent.parent / "agentclinic.db"


async def get_db() -> aiosqlite.Connection:
    """Return a connection to the database."""
    conn = aiosqlite.connect(DB_PATH)
    conn.row_factory = aiosqlite.Row
    return conn


async def get_all_agents() -> List[Dict[str, Any]]:
    """Return all agents from the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM agents ORDER BY id") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
