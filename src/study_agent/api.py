"""FastAPI server exposing the StudyAssistantAgent over HTTP."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from .agent import StudyAssistantAgent

app = FastAPI(title="Study Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_agent = StudyAssistantAgent()


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    query: str
    is_valid: bool
    topics_found: List[str]
    answer: str
    next_steps: List[str]
    error: Optional[str] = None


@app.post("/query", response_model=QueryResponse)
def run_query(req: QueryRequest) -> QueryResponse:
    result = _agent.run(req.query)
    return QueryResponse(
        query=result.query,
        is_valid=result.is_valid,
        topics_found=result.topics_found,
        answer=result.answer,
        next_steps=result.next_steps,
        error=result.error,
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
