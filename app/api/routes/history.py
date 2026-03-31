from fastapi import APIRouter, HTTPException

from app.repositories.history_repository import HistoryRepository
from app.services.trend_service import TrendService

router = APIRouter(prefix="/history", tags=["history"])

history_repository = HistoryRepository()
trend_service = TrendService()


@router.get("/{patient_id}")
def get_patient_history(patient_id: str):
    records = history_repository.get_records(patient_id)
    if not records:
        raise HTTPException(status_code=404, detail="未找到该患者的历史记录")
    return {
        "patient_id": patient_id,
        "history_count": len(records),
        "records": records,
    }


@router.get("/{patient_id}/trend")
def get_patient_trend(patient_id: str):
    records = history_repository.get_records(patient_id)
    if not records:
        raise HTTPException(status_code=404, detail="未找到该患者的历史记录")

    return {
        "patient_id": patient_id,
        "trend_analysis": trend_service.analyze_trend(records),
    }