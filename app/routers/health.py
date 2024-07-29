from fastapi import APIRouter


router = APIRouter(tags=["Health Check Endpoints"])


@router.get("/")
def health_check():
    return { "status": "Running" }
