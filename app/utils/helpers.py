def safe_lower(value: str | None) -> str:
    return (value or "").lower()
