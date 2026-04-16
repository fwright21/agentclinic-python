from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv

from src.database import (
    get_all_agents,
    get_agent_by_id,
    get_all_ailments,
    get_ailment_by_name,
    save_diagnosis_run,
    get_last_diagnosis_for_agent,
)
from src.diagnosis import run_diagnosis

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="src/templates")


@app.get("/")
def read_root(request: Request):
    return HTMLResponse(templates.get_template("index.html").render(request=request))


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
    last_diagnosis = await get_last_diagnosis_for_agent(agent_id)
    return HTMLResponse(
        templates.get_template("agent_detail.html").render(
            request=request, agent=agent, last_diagnosis=last_diagnosis
        )
    )


@app.post("/agents/{agent_id}/diagnose")
async def diagnose_agent(request: Request, agent_id: int, symptoms: str = Form(...)):
    agent = await get_agent_by_id(agent_id)
    if not agent:
        return HTMLResponse("Agent not found", status_code=404)

    result = await run_diagnosis(agent["name"], symptoms)

    ailment = await get_ailment_by_name(result["ailment_name"])
    ailment_id = ailment["id"] if ailment else None

    await save_diagnosis_run(
        agent_id=agent_id,
        ailment_id=ailment_id,
        symptoms=symptoms,
        report=result["report"],
        prompt_tokens=result["prompt_tokens"],
        completion_tokens=result["completion_tokens"],
        total_tokens=result["total_tokens"],
    )

    return RedirectResponse(url=f"/agents/{agent_id}", status_code=303)


@app.get("/ailments")
async def list_ailments(request: Request):
    ailments = await get_all_ailments()
    return HTMLResponse(
        templates.get_template("ailments.html").render(request=request, ailments=ailments)
    )
