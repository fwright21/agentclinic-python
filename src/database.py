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


async def get_agent_by_id(agent_id: int) -> Dict[str, Any] | None:
    """Return a single agent by ID, or None if not found."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM agents WHERE id = ?", (agent_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None
