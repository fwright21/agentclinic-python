"""
Diagnosis engine — LangChain chain using Groq.
Reads agent symptoms, classifies ailment, returns structured report + token usage.
"""

import os
from typing import Any
from langchain_groq import ChatGroq
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

VALID_AILMENTS = [
    "Context Window Overflow",
    "Prompt Fatigue",
    "Hallucination Anxiety",
    "Token Budget Exhaustion",
    "Instruction Drift",
    "Repetition Compulsion",
]


class TokenTracker(BaseCallbackHandler):
    """Captures token usage from Groq response metadata."""

    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        usage = getattr(response, "llm_output", {}) or {}
        token_usage = usage.get("token_usage", {})
        self.prompt_tokens = token_usage.get("prompt_tokens", 0)
        self.completion_tokens = token_usage.get("completion_tokens", 0)
        self.total_tokens = token_usage.get("total_tokens", 0)


class DiagnosisResult(BaseModel):
    ailment_name: str = Field(description="Must exactly match one of the valid ailment names")
    report: str = Field(description="Plain-English report: Issue: X. Treatment: Y.")


async def run_diagnosis(agent_name: str, symptoms: str) -> dict:
    """
    Run the diagnosis chain for an agent.
    Returns ailment_name, report, prompt_tokens, completion_tokens, total_tokens.
    """
    tracker = TokenTracker()

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        callbacks=[tracker],
        temperature=0,
    )

    parser = JsonOutputParser(pydantic_object=DiagnosisResult)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a clinical AI diagnostician. You diagnose AI agents based on their symptoms.

You must classify the agent's symptoms into EXACTLY ONE of these ailments:
{ailments}

Respond with valid JSON only, no other text:
{{
  "ailment_name": "<exact ailment name from the list above>",
  "report": "Issue: <ailment name>. Treatment: <recommended treatment>."
}}"""),
        ("human", "Agent: {agent_name}\nSymptoms: {symptoms}"),
    ])

    chain = prompt | llm | parser

    result = await chain.ainvoke({
        "ailments": "\n".join(f"- {a}" for a in VALID_AILMENTS),
        "agent_name": agent_name,
        "symptoms": symptoms,
    })

    return {
        "ailment_name": result.get("ailment_name", "Unknown"),
        "report": result.get("report", ""),
        "prompt_tokens": tracker.prompt_tokens,
        "completion_tokens": tracker.completion_tokens,
        "total_tokens": tracker.total_tokens,
    }
