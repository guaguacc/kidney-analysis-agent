import pytest

from app.core.exceptions import ValidationError
from app.schemas.lab_result import LabResult
from app.schemas.patient import PatientInput
from app.utils.validator import validate_patient_payload


def test_validator_rejects_bad_gender() -> None:
    payload = PatientInput(patient_id="P001", age=20, gender="bad", history=[], labs=LabResult())
    with pytest.raises(ValidationError):
        validate_patient_payload(payload)
