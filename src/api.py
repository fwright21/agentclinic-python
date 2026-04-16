from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import aiosqlite
import os

from src.treatment import generate_steps

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


async def infer_ailment(symptoms: str) -> tuple[str, str]:
    symptoms_lower = symptoms.lower()

    if (
        "context" in symptoms_lower
        or "heavy" in symptoms_lower
        or "recap" in symptoms_lower
    ):
        return ("Context Window Overflow", "Context Flush")
    if "forget" in symptoms_lower or "memory" in symptoms_lower:
        return ("Memory Drift", "Memory Summary Injection")
    if (
        "stuck" in symptoms_lower
        or "repeating" in symptoms_lower
        or "loop" in symptoms_lower
    ):
        return ("Repetition Loop", "Session Reset")
    if (
        "creative" in symptoms_lower
        or "boring" in symptoms_lower
        or "predictable" in symptoms_lower
    ):
        return ("Predictability Fatigue", "Novelty Injection")
    if (
        "unsure" in symptoms_lower
        or "hesitat" in symptoms_lower
        or "cautious" in symptoms_lower
    ):
        return ("Confidence Deficit", "Confidence Recalibration")
    if "overwhelm" in symptoms_lower or "complex" in symptoms_lower:
        return ("Complexity Overload", "Task Decomposition")
    if (
        "verbose" in symptoms_lower
        or "long" in symptoms_lower
        or "wordy" in symptoms_lower
    ):
        return ("Output Bloat", "Compression Prompt")

    return ("Unknown Condition", "Session Reset")


@router.post("/diagnose", response_model=DiagnoseResponse)
async def diagnose(req: DiagnoseRequest):
    conn = await get_db()

    agent_id = await find_or_create_agent(conn, req.agent_name)

    ailment_name, therapy_name = await infer_ailment(req.symptoms)

    cursor = await conn.execute(
        "INSERT INTO diagnosis_runs (agent_id, submitted_symptoms, report) VALUES (?, ?, ?)",
        (agent_id, req.symptoms, f"Issue: {ailment_name}. Treatment: {therapy_name}."),
    )
    await conn.commit()
    diagnosis_id = cursor.lastrowid

    steps = generate_steps(therapy_name, req.session_type)

    await conn.close()

    try:
        import sys

        sys.path.insert(0, os.path.expanduser("~/Documents/AIBriefing"))
        from remedies import add_remedy

        add_remedy(
            diagnosis_id,
            req.agent_name,
            req.session_type,
            ailment_name,
            therapy_name,
            steps,
        )
    except Exception as e:
        pass

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

    await conn.execute(
        "UPDATE remedies SET status = 'APPROVED' WHERE diagnosis_id = ?",
        (diagnosis_id,),
    )
    await conn.commit()

    await conn.close()

    return {"id": diagnosis_id, "status": "APPROVED"}
