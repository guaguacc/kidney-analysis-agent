from datetime import datetime
from typing import Any, Dict

from app.core.prompts import build_kidney_analysis_prompt
from app.repositories.history_repository import HistoryRepository
from app.services.gpt_service import GPTService
from app.services.rule_engine import RuleEngine
from app.utils.validator import validate_patient_input


class AgentService:
    def __init__(self) -> None:
        self.rule_engine = RuleEngine()
        self.gpt_service = GPTService()
        self.history_repository = HistoryRepository()

    def analyze_patient(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        validated_data = validate_patient_input(patient_data)

        rule_result = self.rule_engine.analyze(validated_data)

        prompt = build_kidney_analysis_prompt(
            patient_data=validated_data,
            rule_result=rule_result,
        )

        gpt_result = self.gpt_service.analyze_with_gpt(prompt)

        result = {
            "patient_id": validated_data.get("patient_id"),
            "risk_level": rule_result.get("risk_level", "未知"),
            "ckd_stage": rule_result.get("ckd_stage", "未知"),
            "egfr_severity": rule_result.get("egfr_severity", "未知"),
            "abnormal_items": rule_result.get("abnormal_items", []),
            "rule_based_summary": rule_result.get("rule_based_summary", ""),
            "gpt_summary": gpt_result.get("summary", ""),
            "gpt_explanation": gpt_result.get("explanation", ""),
            "recommendations": gpt_result.get("recommendations", []),
            "caution": gpt_result.get("caution", ""),
        }

        patient_id = validated_data.get("patient_id")
        if patient_id:
            history_record = {
                **validated_data,
                "timestamp": datetime.utcnow().isoformat(),
                "analysis_result": result,
            }
            self.history_repository.add_record(patient_id, history_record)

        return result