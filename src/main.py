from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv
import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("agentclinic")

from src.database import (
    get_all_agents,
    get_agent_by_id,
    get_all_ailments,
    get_ailment_by_name,
    get_all_therapies,
    get_therapy_by_name,
    save_diagnosis_run,
    get_last_diagnosis_for_agent,
)
from src.diagnosis import run_diagnosis
from src.dashboard import (
    get_summary_counts,
    get_agent_health_table,
    get_ailment_frequency,
    get_recent_diagnosis_runs,
)
from src.visits import (
    assign_visit_number,
    check_and_apply_chronic,
    sync_agent_status,
    get_all_visits_for_agent,
    update_visit_outcome,
    get_agent_id_for_visit,
)

load_dotenv()

app = FastAPI()

from src.api import router as api_router

app.include_router(api_router)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = (time.time() - start_time) * 1000
        logger.info(
            f"{request.method} {request.url.path} {response.status_code} {duration:.1f}ms"
        )
        return response


app.add_middleware(LoggingMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="src/templates")


@app.get("/")
def read_root(request: Request):
    return HTMLResponse(templates.get_template("index.html").render(request=request))


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return HTMLResponse(
        templates.get_template("404.html").render(request=request),
        status_code=404,
    )


@app.exception_handler(500)
async def custom_500_handler(request: Request, exc):
    return HTMLResponse(
        templates.get_template("500.html").render(request=request),
        status_code=500,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    return HTMLResponse(
        templates.get_template("400.html").render(request=request, error=str(exc)),
        status_code=400,
    )


@app.get("/agents")
async def list_agents(request: Request):
    agents = await get_all_agents()
    return HTMLResponse(
        templates.get_template("agents.html").render(request=request, agents=agents)
    )


@app.get("/agents/{agent_id}")
async def agent_detail(request: Request, agent_id: int):
    agent = await get_agent_by_id(agent_id)
    if not agent:
        return HTMLResponse("Agent not found", status_code=404)
    visits = await get_all_visits_for_agent(agent_id)
    last_diagnosis = visits[0] if visits else None
    error = request.query_params.get("error")
    return HTMLResponse(
        templates.get_template("agent_detail.html").render(
            request=request,
            agent=agent,
            visits=visits,
            last_diagnosis=last_diagnosis,
            error=error,
        )
    )


@app.post("/agents/{agent_id}/diagnose")
async def diagnose_agent(request: Request, agent_id: int, symptoms: str = Form(...)):
    agent = await get_agent_by_id(agent_id)
    if not agent:
        return HTMLResponse("Agent not found", status_code=404)

    symptoms = symptoms.strip()
    if len(symptoms) < 10:
        return RedirectResponse(
            url=f"/agents/{agent_id}?error=Symptoms must be at least 10 characters",
            status_code=303,
        )

    result = await run_diagnosis(agent["name"], symptoms)

    ailment = await get_ailment_by_name(result["ailment_name"])
    ailment_id = ailment["id"] if ailment else None

    therapy = await get_therapy_by_name(result["therapy_name"])
    therapy_id = therapy["id"] if therapy else None

    visit_number = await assign_visit_number(agent_id)

    diagnosis_id = await save_diagnosis_run(
        agent_id=agent_id,
        ailment_id=ailment_id,
        symptoms=symptoms,
        report=result["report"],
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

    return RedirectResponse(url=f"/agents/{agent_id}", status_code=303)


@app.get("/ailments")
async def list_ailments(request: Request):
    ailments = await get_all_ailments()
    return HTMLResponse(
        templates.get_template("ailments.html").render(
            request=request, ailments=ailments
        )
    )


@app.get("/therapies")
async def list_therapies(request: Request):
    therapies = await get_all_therapies()
    return HTMLResponse(
        templates.get_template("therapies.html").render(
            request=request, therapies=therapies
        )
    )


@app.get("/dashboard")
async def dashboard(request: Request):
    summary_counts = await get_summary_counts()
    agent_health = await get_agent_health_table()
    ailment_freq = await get_ailment_frequency()
    recent_runs = await get_recent_diagnosis_runs(limit=10)
    return HTMLResponse(
        templates.get_template("dashboard.html").render(
            request=request,
            summary_counts=summary_counts,
            agent_health=agent_health,
            ailment_freq=ailment_freq,
            recent_runs=recent_runs,
        )
    )


@app.post("/agents/{agent_id}/visits/{visit_id}/outcome")
async def update_visit_outcome_route(
    request: Request,
    agent_id: int,
    visit_id: int,
    outcome: str = Form(...),
):
    agent = await get_agent_by_id(agent_id)
    if not agent:
        return HTMLResponse("Agent not found", status_code=404)

    actual_agent_id = await get_agent_id_for_visit(visit_id)
    if actual_agent_id != agent_id:
        return HTMLResponse("Visit not found for this agent", status_code=404)

    await update_visit_outcome(visit_id, outcome)
    await sync_agent_status(agent_id)

    return RedirectResponse(url=f"/agents/{agent_id}", status_code=303)
