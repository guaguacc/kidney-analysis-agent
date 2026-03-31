from fastapi import APIRouter, HTTPException

from app.schemas.patient import PatientInput
from app.services.agent_service import AgentService

router = APIRouter(prefix="/analyze", tags=["analyze"])

agent_service = AgentService()


@router.post("")
def analyze_patient(payload: PatientInput):
    try:
        return agent_service.analyze_patient(payload.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc