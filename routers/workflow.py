import os
from typing import TypedDict

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from functools import lru_cache

load_dotenv()

router = APIRouter(prefix="/workflow", tags=["workflow"])

CONGES = {"Tiavisoa": 12, "Marie": 5, "Paul": 23}

@lru_cache
def get_modele():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )


# --- L'état qui circule dans le graphe ---

class Etat(TypedDict):
    question: str
    categorie: str
    reponse: str


# --- Les nœuds ---

def classifier(etat: Etat) -> dict:
    prompt = (
        "Classe cette question dans une seule catégorie : 'rh' si elle concerne "
        "les congés ou le personnel, 'general' sinon. "
        "Réponds par un seul mot, sans ponctuation.\n\n"
        f"Question : {etat['question']}"
    )
    resultat = modele.invoke(prompt).text.strip().lower()
    categorie = "rh" if "rh" in resultat else "general"
    return {"categorie": categorie}


def repondre_rh(etat: Etat) -> dict:
    liste = "\n".join(f"- {nom} : {jours} jours" for nom, jours in CONGES.items())
    prompt = (
        "Réponds à la question en utilisant uniquement ces données de congés.\n"
        "Si la personne n'y figure pas, dis-le clairement.\n\n"
        f"{liste}\n\nQuestion : {etat['question']}"
    )
    return {"reponse": modele.invoke(prompt).text}


def repondre_general(etat: Etat) -> dict:
    return {"reponse": modele.invoke(etat["question"]).text}


# --- L'aiguillage ---

def router_categorie(etat: Etat) -> str:
    return etat["categorie"]


# --- Construction du graphe ---

constructeur = StateGraph(Etat)

constructeur.add_node("classifier", classifier)
constructeur.add_node("repondre_rh", repondre_rh)
constructeur.add_node("repondre_general", repondre_general)

constructeur.add_edge(START, "classifier")
constructeur.add_conditional_edges(
    "classifier",
    router_categorie,
    {"rh": "repondre_rh", "general": "repondre_general"},
)
constructeur.add_edge("repondre_rh", END)
constructeur.add_edge("repondre_general", END)

graphe = constructeur.compile()

 #API

class Demande(BaseModel):
    question: str


class Resultat(BaseModel):
    categorie: str
    reponse: str


@router.post("", response_model=Resultat)
async def lancer(demande: Demande):
    try:
        final = await graphe.ainvoke({"question": demande.question})
    except Exception as e:
        print("TYPE DE L'ERREUR :", type(e))
        raise HTTPException(status_code=503, detail="Modèle indisponible.")

    return Resultat(categorie=final["categorie"], reponse=final["reponse"])