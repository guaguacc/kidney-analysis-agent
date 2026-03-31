from fastapi import FastAPI

from app.api.routes.analyze import router as analyze_router
from app.api.routes.health import router as health_router
from app.api.routes.history import router as history_router
from app.api.routes.patient import router as patient_router
from app.config import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(health_router)
app.include_router(analyze_router)
app.include_router(patient_router)
app.include_router(history_router)

print("\n===== REGISTERED ROUTES =====")
for route in app.routes:
    methods = getattr(route, "methods", None)
    path = getattr(route, "path", None)
    print(path, methods)
print("===== END ROUTES =====\n")