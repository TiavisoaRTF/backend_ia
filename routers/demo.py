import os

from fastapi import APIRouter

router = APIRouter(prefix="/demo", tags=["demo"])

API_KEY = os.getenv("API_KEY")


@router.get("/ping")
def ping():
    return {"ok": True}