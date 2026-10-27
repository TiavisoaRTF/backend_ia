import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from google import genai
from google.genai import errors
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

load_dotenv()

MODELE = "gemini-3.8-flash"
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

router = APIRouter(prefix="/chat", tags=["chat"])


class Question(BaseModel):
    texte: str


class Reponse(BaseModel):
    reponse: str
    modele: str


@router.post("", response_model=Reponse)
async def chat(question: Question):
    try:
        resultat = await client.aio.models.generate_content(
            model=MODELE,
            contents=question.texte
        )
    except errors.ServerError:
        raise HTTPException(status_code=503, detail="Modèle temporairement indisponible.")
    except errors.APIError as e:
        raise HTTPException(status_code=502, detail=f"Erreur du fournisseur : {e.message}")

    return Reponse(reponse=resultat.text, modele=MODELE)

@router.post("/stream")
async def chat_stream(question: Question):
    async def generer():
        flux = await client.aio.models.generate_content_stream(
            model=MODELE,
            contents=question.texte
        )
        async for morceau in flux:
            if morceau.text:
                yield morceau.text

    return StreamingResponse(generer(), media_type="text/plain")