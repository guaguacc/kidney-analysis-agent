from typing import List, Optional

from pydantic import BaseModel


class PatientInput(BaseModel):
    patient_id: Optional[str] = None
    age: int
    gender: Optional[str] = None
    scr: Optional[float] = None
    bun: Optional[float] = None
    egfr: Optional[float] = None
    acr: Optional[float] = None
    urine_protein: Optional[str] = None
    sbp: Optional[float] = None
    dbp: Optional[float] = None
    history: Optional[List[str]] = None