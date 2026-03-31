from app.config import get_settings
from app.services.agent_service import AgentService
from app.services.gpt_service import GPTService
from app.services.patient_service import PatientService
from app.services.report_service import ReportService
from app.services.rule_engine import RuleEngine
from app.services.trend_service import TrendService


def get_rule_engine() -> RuleEngine:
    return RuleEngine()


def get_gpt_service() -> GPTService:
    settings = get_settings()
    return GPTService(api_key=settings.openai_api_key, model=settings.openai_model)


def get_report_service() -> ReportService:
    return ReportService()


def get_patient_service() -> PatientService:
    return PatientService()


def get_trend_service() -> TrendService:
    return TrendService()


def get_agent_service() -> AgentService:
    return AgentService(
        rule_engine=get_rule_engine(),
        gpt_service=get_gpt_service(),
        report_service=get_report_service(),
    )
