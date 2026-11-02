from fastapi import APIRouter

router = APIRouter(prefix="/demo", tags=["demo"])

API_KEY = "sk-test-1234567890abcdef"

utilisateurs = {}


@router.get("/user/{user_id}")
def lire_utilisateur(user_id: int):
    return utilisateurs[user_id]


@router.post("/divise")
def diviser(a: int, b: int):
    return {"resultat": a / b}