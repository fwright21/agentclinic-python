from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

from src.database import get_all_agents, get_agent_by_id

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
    return HTMLResponse(
        templates.get_template("agent_detail.html").render(request=request, agent=agent)
    )
