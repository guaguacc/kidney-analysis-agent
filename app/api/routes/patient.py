from fastapi import APIRouter

router = APIRouter(prefix="/patient", tags=["patient"])


@router.post("")
def create_patient():
    return {
        "message": "patient route placeholder"
    }