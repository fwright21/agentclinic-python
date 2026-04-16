import json
import logging
import os
import sys

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.database import (
    get_ailment_by_name,
    get_therapy_by_name,
    save_diagnosis_run,
)
from src.diagnosis import run_diagnosis
from src.treatment import generate_steps
from src.visits import assign_visit_number, check_and_apply_chronic, sync_agent_status

import aiosqlite

logger = logging.getLogger("agentclinic.api")

router = APIRouter(prefix="/api", tags=["api"])

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "agentclinic.db")


class DiagnoseRequest(BaseModel):
    agent_name: str
    session_type: str = "claude-code"
    symptoms: str


class DiagnoseResponse(BaseModel):
    diagnosis_id: int
    ailment: str
    therapy: str
    treatment_steps: list[str]
    status: str


async def get_db():
    conn = await aiosqlite.connect(DB_PATH)
    conn.row_factory = aiosqlite.Row
    return conn


async def find_or_create_agent(conn, agent_name: str) -> int:
    async with conn.execute(
        "SELECT id FROM agents WHERE name = ?", (agent_name,)
    ) as cursor:
        row = await cursor.fetchone()
        if row:
            return row["id"]

    cursor = await conn.execute(
        "INSERT INTO agents (name, model_type, status, presenting_complaints) VALUES (?, ?, ?, ?)",
        (agent_name, "unknown", "active", ""),
    )
    await conn.commit()
    return cursor.lastrowid


@router.post("/diagnose", response_model=DiagnoseResponse)
async def diagnose(req: DiagnoseRequest):
    conn = await get_db()
    agent_id = await find_or_create_agent(conn, req.agent_name)
    await conn.close()

    result = await run_diagnosis(req.agent_name, req.symptoms)

    ailment_name = result["ailment_name"]
    therapy_name = result["therapy_name"]

    ailment = await get_ailment_by_name(ailment_name)
    ailment_id = ailment["id"] if ailment else None

    therapy = await get_therapy_by_name(therapy_name)
    therapy_id = therapy["id"] if therapy else None

    visit_number = await assign_visit_number(agent_id)

    report = result["report"].replace("visit #N", f"visit #{visit_number}")

    diagnosis_id = await save_diagnosis_run(
        agent_id=agent_id,
        ailment_id=ailment_id,
        symptoms=req.symptoms,
        report=report,
        prompt_tokens=result["prompt_tokens"],
        completion_tokens=result["completion_tokens"],
        total_tokens=result["total_tokens"],
        therapy_id=therapy_id,
        visit_number=visit_number,
        outcome="OPEN",
    )

    if ailment_id:
        await check_and_apply_chronic(agent_id, ailment_id)
    await sync_agent_status(agent_id)

    steps = generate_steps(therapy_name, req.session_type)

    try:
        sys.path.insert(0, os.path.expanduser("~/Documents/AIBriefing"))
        from remedies import add_remedy
        add_remedy(diagnosis_id, req.agent_name, req.session_type, ailment_name, therapy_name, steps)
    except Exception as e:
        logger.warning(f"add_remedy failed — remedy not queued in AIBriefing: {e}")

    return DiagnoseResponse(
        diagnosis_id=diagnosis_id,
        ailment=ailment_name,
        therapy=therapy_name,
        treatment_steps=steps,
        status="PENDING_APPROVAL",
    )


@router.get("/diagnose/{diagnosis_id}")
async def get_diagnosis(diagnosis_id: int):
    conn = await get_db()
    async with conn.execute(
        """SELECT dr.id, dr.submitted_symptoms, dr.report, dr.created_at, dr.outcome,
                  a.name as agent_name, r.ailment, r.therapy, r.treatment_steps
           FROM diagnosis_runs dr
           JOIN agents a ON dr.agent_id = a.id
           LEFT JOIN remedies r ON r.diagnosis_id = dr.id
           WHERE dr.id = ?""",
        (diagnosis_id,),
    ) as cursor:
        row = await cursor.fetchone()

    if not row:
        await conn.close()
        raise HTTPException(status_code=404, detail="Diagnosis not found")

    ailment = row["ailment"] or "Unknown"
    therapy = row["therapy"] or "Session Reset"
    steps = (
        json.loads(row["treatment_steps"])
        if row["treatment_steps"]
        else generate_steps(therapy, "claude-code")
    )

    await conn.close()

    return {
        "id": row["id"],
        "agent_name": row["agent_name"],
        "symptoms": row["submitted_symptoms"],
        "ailment": ailment,
        "therapy": therapy,
        "treatment_steps": steps,
        "status": row["outcome"] or "OPEN",
        "created_at": row["created_at"],
    }


@router.patch("/diagnose/{diagnosis_id}/approve")
async def approve_diagnosis(diagnosis_id: int):
    conn = await get_db()

    async with conn.execute(
        "SELECT id FROM diagnosis_runs WHERE id = ?", (diagnosis_id,)
    ) as cursor:
        row = await cursor.fetchone()

    if not row:
        await conn.close()
        raise HTTPException(status_code=404, detail="Diagnosis not found")

    await conn.execute(
        "UPDATE diagnosis_runs SET outcome = 'APPROVED' WHERE id = ?", (diagnosis_id,)
    )
    await conn.commit()
    await conn.close()

    return {"id": diagnosis_id, "status": "APPROVED"}
