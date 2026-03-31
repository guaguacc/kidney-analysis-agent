from app.schemas.analysis import AnalysisResponse
from app.schemas.patient import PatientInput


class ReportService:
    def build_response(self, payload: PatientInput, rule_result: dict, gpt_summary: str) -> AnalysisResponse:
        return AnalysisResponse(
            patient_id=payload.patient_id,
            risk_level=rule_result["risk_level"],
            abnormal_items=rule_result["abnormal_items"],
            rule_hits=rule_result["rule_hits"],
            rule_based_summary=rule_result["rule_based_summary"],
            gpt_summary=gpt_summary,
            recommendations=rule_result["recommendations"],
        )
