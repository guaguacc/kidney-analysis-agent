from typing import Optional

from pydantic import BaseModel, Field


class LabResult(BaseModel):
    scr: Optional[float] = Field(default=None, description="Serum creatinine")
    bun: Optional[float] = None
    egfr: Optional[float] = None
    cystatin_c: Optional[float] = None
    uric_acid: Optional[float] = None
    acr: Optional[float] = None
    urine_protein: Optional[str] = None
    sbp: Optional[int] = None
    dbp: Optional[int] = None
