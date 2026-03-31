from typing import List

from pydantic import BaseModel, Field


class AnalysisResponse(BaseModel):
    patient_id: str
    risk_level: str
    abnormal_items: List[str] = Field(default_factory=list)
    rule_hits: List[str] = Field(default_factory=list)
    rule_based_summary: str
    gpt_summary: str
    recommendations: List[str] = Field(default_factory=list)


class TrendSummaryResponse(BaseModel):
    patient_id: str
    trend_summary: str
    key_changes: List[str] = Field(default_factory=list)
