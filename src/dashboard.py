import aiosqlite
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = Path(__file__).parent.parent / "agentclinic.db"

HIGH_TOKEN_THRESHOLD = 1000


async def get_summary_counts() -> Dict[str, int]:
    """Return total agents, total diagnosis runs, active ailments count, flagged agents count."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        async with db.execute("SELECT COUNT(*) as total FROM agents") as cursor:
            total_agents = (await cursor.fetchone())["total"]

        async with db.execute("SELECT COUNT(*) as total FROM diagnosis_runs") as cursor:
            total_runs = (await cursor.fetchone())["total"]

        async with db.execute(
            "SELECT COUNT(DISTINCT ailment_id) as total FROM diagnosis_runs WHERE ailment_id IS NOT NULL"
        ) as cursor:
            active_ailments = (await cursor.fetchone())["total"]

        async with db.execute(
            f"""SELECT COUNT(DISTINCT agent_id) as total
                FROM diagnosis_runs
                WHERE total_tokens > {HIGH_TOKEN_THRESHOLD}"""
        ) as cursor:
            flagged_agents = (await cursor.fetchone())["total"]

        return {
            "total_agents": total_agents,
            "total_runs": total_runs,
            "active_ailments": active_ailments,
            "flagged_agents": flagged_agents,
        }


async def get_agent_health_table() -> List[Dict[str, Any]]:
    """Return agents with most recent ailment, last diagnosis date, token flag."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        async with db.execute(
            f"""SELECT
                    a.id,
                    a.name,
                    a.model_type,
                    a.status,
                    al.name as ailment_name,
                    dr.total_tokens,
                    dr.created_at as last_diagnosis,
                    CASE WHEN dr.total_tokens > {HIGH_TOKEN_THRESHOLD} THEN 1 ELSE 0 END as has_high_tokens
                FROM agents a
                LEFT JOIN diagnosis_runs dr ON dr.id = (
                    SELECT dr2.id FROM diagnosis_runs dr2
                    WHERE dr2.agent_id = a.id
                    ORDER BY dr2.created_at DESC
                    LIMIT 1
                )
                LEFT JOIN ailments al ON dr.ailment_id = al.id
                ORDER BY a.id"""
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def get_ailment_frequency() -> List[Dict[str, Any]]:
    """Return ailments ranked by diagnosis run count."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        async with db.execute(
            """SELECT
                    a.id,
                    a.name,
                    a.description,
                    COUNT(dr.id) as run_count
                FROM ailments a
                LEFT JOIN diagnosis_runs dr ON a.id = dr.ailment_id
                GROUP BY a.id
                HAVING run_count > 0
                ORDER BY run_count DESC"""
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def get_recent_diagnosis_runs(limit: int = 10) -> List[Dict[str, Any]]:
    """Return most recent diagnosis runs."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        async with db.execute(
            f"""SELECT
                    dr.id,
                    dr.agent_id,
                    a.name as agent_name,
                    al.name as ailment_name,
                    th.name as therapy_name,
                    dr.total_tokens,
                    dr.created_at,
                    dr.submitted_symptoms
                FROM diagnosis_runs dr
                LEFT JOIN agents a ON dr.agent_id = a.id
                LEFT JOIN ailments al ON dr.ailment_id = al.id
                LEFT JOIN therapies th ON dr.therapy_id = th.id
                ORDER BY dr.created_at DESC
                LIMIT {limit}"""
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
