from fastapi import APIRouter

router = APIRouter(prefix="/demo", tags=["demo"])

API_KEY = "sk-test-1234567890abcdef"


@router.get("/ping")
def ping():
    return {"ok": True}