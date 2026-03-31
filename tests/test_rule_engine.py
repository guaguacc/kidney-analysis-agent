from app.schemas.lab_result import LabResult
from app.schemas.patient import PatientInput
from app.services.rule_engine import RuleEngine


def test_rule_engine_flags_high_risk() -> None:
    payload = PatientInput(
        patient_id="P001",
        age=60,
        gender="male",
        history=["hypertension"],
        labs=LabResult(scr=150, egfr=40, acr=80, urine_protein="positive", sbp=150, dbp=95),
    )
    result = RuleEngine().evaluate(payload)
    assert result["risk_level"] == "high"
