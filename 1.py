import os

def create_kidney_agent_structure():
    # 根目录名称
    root = ""
    
    # 定义目录结构 (包括嵌套路径)
    dirs = [
        "app/api/routes",
        "app/schemas",
        "app/services",
        "app/core",
        "app/utils",
        "app/repositories",
        "app/db/models",
        "app/knowledge/templates",
        "tests",
        "scripts",
        "data/output",
        "logs"
    ]

    # 定义需要生成的具体文件及其默认内容
    files = {
        "app/__init__.py": "",
        "app/main.py": "from fastapi import FastAPI\napp = FastAPI(title='Kidney Agent API')\n\n@app.get('/')\ndef index(): return {'status': 'healthy'}",
        "app/config.py": "from pydantic_settings import BaseSettings\nclass Settings(BaseSettings):\n    APP_NAME: str = 'Kidney Agent'\n    DATABASE_URL: str = 'sqlite:///./kidney.db'\n    OPENAI_API_KEY: str = ''\n    class Config: env_file = '.env'\n\nsettings = Settings()",
        "app/dependencies.py": "def get_db():\n    pass # Yield db session here",
        
        # API Routes
        "app/api/__init__.py": "",
        "app/api/routes/__init__.py": "",
        "app/api/routes/health.py": "from fastapi import APIRouter\nrouter = APIRouter()\n@router.get('/health')\ndef health(): return {'status': 'ok'}",
        "app/api/routes/analyze.py": "from fastapi import APIRouter\nrouter = APIRouter()",
        "app/api/routes/patient.py": "from fastapi import APIRouter\nrouter = APIRouter()",
        "app/api/routes/history.py": "from fastapi import APIRouter\nrouter = APIRouter()",
        
        # Schemas (Pydantic models)
        "app/schemas/__init__.py": "",
        "app/schemas/patient.py": "from pydantic import BaseModel\nclass PatientBase(BaseModel):\n    name: str\n    age: int",
        "app/schemas/lab_result.py": "from pydantic import BaseModel\nclass LabResult(BaseModel):\n    creatinine: float",
        "app/schemas/analysis.py": "from pydantic import BaseModel\nclass AnalysisResult(BaseModel):\n    egfr: float\n    stage: str",
        "app/schemas/common.py": "from pydantic import BaseModel\nclass MsgResponse(BaseModel):\n    message: str",
        
        # Services
        "app/services/__init__.py": "",
        "app/services/agent_service.py": "class AgentService:\n    def run_workflow(self): pass",
        "app/services/rule_engine.py": "class RuleEngine:\n    def check_ckd_stage(self, egfr: float): pass",
        "app/services/gpt_service.py": "class GPTService:\n    def generate_advice(self, data: dict): pass",
        "app/services/report_service.py": "class ReportService: pass",
        "app/services/patient_service.py": "class PatientService: pass",
        "app/services/trend_service.py": "class TrendService: pass",

        # Core
        "app/core/__init__.py": "",
        "app/core/prompts.py": "SYSTEM_PROMPT = 'You are a renal specialist...'",
        "app/core/constants.py": "CKD_STAGES = {1: 'Normal', 2: 'Mild'}",
        "app/core/enums.py": "from enum import Enum\nclass Gender(str, Enum):\n    MALE = 'male'\n    FEMALE = 'female'",
        "app/core/exceptions.py": "class MedicalLogicError(Exception): pass",

        # Repositories
        "app/repositories/__init__.py": "",
        "app/repositories/patient_repository.py": "class PatientRepository: pass",
        "app/repositories/analysis_repository.py": "class AnalysisRepository: pass",
        "app/repositories/history_repository.py": "class HistoryRepository: pass",

        # DB
        "app/db/__init__.py": "",
        "app/db/base.py": "from sqlalchemy.ext.declarative import declarative_base\nBase = declarative_base()",
        "app/db/session.py": "from sqlalchemy import create_engine\nfrom sqlalchemy.orm import sessionmaker",
        "app/db/models/__init__.py": "",
        "app/db/models/patient.py": "from ..base import Base\nfrom sqlalchemy import Column, Integer, String\nclass PatientModel(Base):\n    __tablename__ = 'patients'\n    id = Column(Integer, primary_key=True)",
        "app/db/models/lab_record.py": "from ..base import Base",
        "app/db/models/analysis_record.py": "from ..base import Base",

        # Utils
        "app/utils/__init__.py": "",
        "app/utils/logger.py": "import logging",
        "app/utils/validator.py": "def validate_lab_input(data): pass",
        "app/utils/unit_converter.py": "def umol_to_mgdl(val): return val / 88.4",
        "app/utils/formatter.py": "def format_report(data): pass",
        "app/utils/helpers.py": "def get_now(): pass",

        # Knowledge
        "app/knowledge/kidney_rules.json": "{}",
        "app/knowledge/reference_ranges.json": "{\"creatinine\": [0.7, 1.3]}",
        "app/knowledge/templates/doctor_report.txt": "Doctor Report Template",
        "app/knowledge/templates/patient_report.txt": "Patient Advice Template",
        "app/knowledge/templates/followup_qa.txt": "Q&A Template",

        # Roots
        "tests/__init__.py": "",
        "tests/test_rule_engine.py": "def test_stage_calc(): assert True",
        "tests/test_gpt_service.py": "",
        "tests/test_api_analyze.py": "",
        "tests/test_validator.py": "",
        
        "scripts/seed_reference_data.py": "if __name__ == '__main__': print('Seeding...')",
        "scripts/import_demo_data.py": "",
        "scripts/run_local.sh": "#!/bin/bash\nuvicorn app.main:app --reload",
        
        "data/demo_patients.json": "[]",
        "data/demo_lab_results.json": "[]",
        
        ".env": "OPENAI_API_KEY=sk-xxxx\nDATABASE_URL=sqlite:///./kidney.db",
        ".env.example": "OPENAI_API_KEY=\nDATABASE_URL=",
        "requirements.txt": "fastapi\nuvicorn\nsqlalchemy\npydantic\npydantic-settings\nopenai\npython-dotenv",
        "README.md": "# Kidney Agent Project",
        "run.py": "import uvicorn\nif __name__ == '__main__':\n    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)"
    }

    # 创建目录
    for d in dirs:
        path = os.path.join(root, d)
        os.makedirs(path, exist_ok=True)
        print(f"Created directory: {path}")

    # 创建文件
    for file_path, content in files.items():
        full_path = os.path.join(root, file_path)
        # 确保父目录存在 (有些文件在根目录或深层目录)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created file: {full_path}")

    print("\n[Success] Kidney Agent 完整架构已生成！")

if __name__ == "__main__":
    create_kidney_agent_structure()