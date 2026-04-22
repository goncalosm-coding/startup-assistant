from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.agents.orchestrator import run_orchestrator

router = APIRouter()


class UserRequest(BaseModel):
    message: str
    startup_name: Optional[str] = None


class AgentResponse(BaseModel):
    response: str
    intent: Optional[str] = None


@router.post("/chat", response_model=AgentResponse)
async def chat(request: UserRequest):
    try:
        response = run_orchestrator(request.message)
        return AgentResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health():
    return {"status": "ok"}