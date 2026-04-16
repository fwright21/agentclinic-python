import aiosqlite
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_PATH = Path(__file__).parent.parent / "agentclinic.db"


async def assign_visit_number(agent_id: int) -> int:
    """Count existing runs for agent and return next visit number."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM diagnosis_runs WHERE agent_id = ?",
            (agent_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return (row[0] or 0) + 1


async def check_and_apply_chronic(agent_id: int, ailment_id: int) -> None:
    """If same ailment appears 3+ times for agent, mark all as CHRONIC."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            """SELECT COUNT(*) FROM diagnosis_runs
               WHERE agent_id = ? AND ailment_id = ?""",
            (agent_id, ailment_id),
        ) as cursor:
            row = await cursor.fetchone()
            count = row[0] if row else 0

        if count >= 3:
            await db.execute(
                """UPDATE diagnosis_runs
                   SET outcome = 'CHRONIC'
                   WHERE agent_id = ? AND ailment_id = ? AND outcome = 'OPEN'""",
                (agent_id, ailment_id),
            )
            await db.commit()


async def sync_agent_status(agent_id: int) -> None:
    """Update agent status based on visit outcomes."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            """SELECT DISTINCT outcome FROM diagnosis_runs
               WHERE agent_id = ?""",
            (agent_id,),
        ) as cursor:
            outcomes = {row[0] async for row in cursor}

        if "CHRONIC" in outcomes:
            status = "Chronic"
        elif "RECURRING" in outcomes:
            status = "Recurring"
        elif outcomes == {"RESOLVED"} or not outcomes:
            status = "Resolved"
        else:
            status = "Active"

        await db.execute(
            "UPDATE agents SET status = ? WHERE id = ?",
            (status, agent_id),
        )
        await db.commit()


async def get_all_visits_for_agent(agent_id: int) -> List[Dict[str, Any]]:
    """Return all diagnosis runs for an agent with ailment/therapy names."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """SELECT
                dr.id,
                dr.visit_number,
                dr.created_at,
                al.name as ailment_name,
                th.name as therapy_name,
                dr.submitted_symptoms,
                dr.report,
                dr.outcome,
                dr.total_tokens
            FROM diagnosis_runs dr
            LEFT JOIN ailments al ON dr.ailment_id = al.id
            LEFT JOIN therapies th ON dr.therapy_id = th.id
            WHERE dr.agent_id = ?
            ORDER BY dr.visit_number DESC""",
            (agent_id,),
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def update_visit_outcome(visit_id: int, outcome: str) -> None:
    """Update outcome on a single visit. Returns None if outcome is CHRONIC."""
    if outcome == "CHRONIC":
        return

    valid_outcomes = {"OPEN", "RESOLVED", "RECURRING"}
    if outcome not in valid_outcomes:
        return

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE diagnosis_runs SET outcome = ? WHERE id = ?",
            (outcome, visit_id),
        )
        await db.commit()


async def update_agent_status(agent_id: int, status: str) -> None:
    """Update agent status directly."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE agents SET status = ? WHERE id = ?",
            (status, agent_id),
        )
        await db.commit()


async def get_agent_id_for_visit(visit_id: int) -> Optional[int]:
    """Return agent_id for a visit, or None if not found."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT agent_id FROM diagnosis_runs WHERE id = ?",
            (visit_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None
