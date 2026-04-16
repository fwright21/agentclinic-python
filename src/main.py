from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()


class Message(BaseModel):
    message: str


@app.get("/")
def read_root() -> Message:
    return Message(message="AgentClinic is open for business")
