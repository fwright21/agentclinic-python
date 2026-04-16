import aiosqlite
from pathlib import Path
from typing import List, Dict, Any, Optional

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


async def get_agent_by_id(agent_id: int) -> Optional[Dict[str, Any]]:
    """Return a single agent by ID, or None if not found."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM agents WHERE id = ?", (agent_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def get_all_ailments() -> List[Dict[str, Any]]:
    """Return all ailments."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM ailments ORDER BY id") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def get_ailment_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Return a single ailment by name, or None if not found."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM ailments WHERE name = ?", (name,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def save_diagnosis_run(
    agent_id: int,
    ailment_id: Optional[int],
    symptoms: str,
    report: str,
    prompt_tokens: int,
    completion_tokens: int,
    total_tokens: int,
) -> int:
    """Save a diagnosis run and return its ID."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """INSERT INTO diagnosis_runs
               (agent_id, ailment_id, submitted_symptoms, report, prompt_tokens, completion_tokens, total_tokens)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (agent_id, ailment_id, symptoms, report, prompt_tokens, completion_tokens, total_tokens),
        )
        await db.commit()
        return cursor.lastrowid


async def get_last_diagnosis_for_agent(agent_id: int) -> Optional[Dict[str, Any]]:
    """Return the most recent diagnosis run for an agent, with ailment name joined."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """SELECT dr.*, a.name as ailment_name
               FROM diagnosis_runs dr
               LEFT JOIN ailments a ON dr.ailment_id = a.id
               WHERE dr.agent_id = ?
               ORDER BY dr.created_at DESC
               LIMIT 1""",
            (agent_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None
