from typing import Any, Dict


def validate_patient_input(data: Dict[str, Any]) -> Dict[str, Any]:
    required_numeric_fields = ["age"]
    optional_numeric_fields = ["scr", "bun", "egfr", "acr", "sbp", "dbp"]

    for field in required_numeric_fields:
        if field not in data or data[field] is None:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(data[field], (int, float)):
            raise ValueError(f"Field '{field}' must be numeric")

    for field in optional_numeric_fields:
        if field in data and data[field] is not None and not isinstance(data[field], (int, float)):
            raise ValueError(f"Field '{field}' must be numeric if provided")

    gender = data.get("gender")
    if gender is not None and str(gender).lower() not in {"male", "female", "other"}:
        raise ValueError("Field 'gender' must be one of: male, female, other")

    return data