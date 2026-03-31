from app.services.gpt_service import GPTService


def test_gpt_service_returns_placeholder() -> None:
    summary = GPTService().generate_summary({}, {"abnormal_items": ["x"], "risk_level": "medium"})
    assert "placeholder" in summary.lower()
