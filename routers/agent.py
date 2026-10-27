# import os
# from datetime import datetime
# from dotenv import load_dotenv
# from fastapi import APIRouter
# from langchain.agents import create_agent
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.tools import tool
# from pydantic import BaseModel
# from fastapi import APIRouter, HTTPException
# from langchain_google_genai.chat_models import GoogleAPIError
# from langgraph.checkpoint.memory import InMemorySaver
# from langchain_groq import ChatGroq

# load_dotenv()
# modele = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     groq_api_key=os.getenv("GROQ_API_KEY")
# )

# router = APIRouter(prefix="/agent", tags=["agent"])

# CONGES = {
#     "Tiavisoa": 12,
#     "Marie": 5,
#     "Paul": 23,
# }

# @tool
# def heure_actuelle() -> str:
#     """Donne l'heure et la date actuelles."""
#     return datetime.now().strftime("%d/%m/%Y %H:%M")

# @tool
# def solde_conges(nom: str) -> str:
#     """Donne le nombre de jours de congés restants pour un employé donné."""
#     if nom not in CONGES:
#         return f"Aucun employé nommé {nom} dans la base."
#     return f"{nom} dispose de {CONGES[nom]} jours de congés." 

# modele = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     groq_api_key=os.getenv("GROQ_API_KEY")
# )

# agent = create_agent(
#     model=modele,
#     tools=[heure_actuelle, solde_conges],
#     checkpointer=InMemorySaver()
# )


# class Question(BaseModel):
#     texte: str


# class Reponse(BaseModel):
#     reponse: str


# class Question(BaseModel):
#     texte: str
#     thread_id: str = "defaut"


# @router.post("", response_model=Reponse)
# async def poser(question: Question):
#     config = {"configurable": {"thread_id": question.thread_id}}
#     try:
#         resultat = await agent.ainvoke(
#             {"messages": [{"role": "user", "content": question.texte}]},
#             config
#         )
#     except Exception as e:
#         print("TYPE DE L'ERREUR :", type(e))
#         raise HTTPException(status_code=503, detail="Modèle indisponible.")

#     return Reponse(reponse=resultat["messages"][-1].text)




import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel

load_dotenv()

router = APIRouter(prefix="/agent", tags=["agent"])

CONGES = {
    "Tiavisoa": 12,
    "Marie": 5,
    "Paul": 23,
}


@tool
def heure_actuelle() -> str:
    """Donne l'heure et la date actuelles."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")


@tool
def solde_conges(nom: str) -> str:
    """Donne le nombre de jours de congés restants pour un employé donné."""
    if nom not in CONGES:
        return f"Aucun employé nommé {nom} dans la base."
    return f"{nom} dispose de {CONGES[nom]} jours de congés."


modele = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

agent = create_agent(
    model=modele,
    tools=[heure_actuelle, solde_conges],
    checkpointer=InMemorySaver()
)


class Question(BaseModel):
    texte: str
    thread_id: str = "defaut"


class Reponse(BaseModel):
    reponse: str


@router.post("", response_model=Reponse)
async def poser(question: Question):
    config = {"configurable": {"thread_id": question.thread_id}}
    try:
        resultat = await agent.ainvoke(
            {"messages": [{"role": "user", "content": question.texte}]},
            config
        )
    except Exception as e:
        print("TYPE DE L'ERREUR :", type(e))
        raise HTTPException(status_code=503, detail="Modèle indisponible.")

    return Reponse(reponse=resultat["messages"][-1].text)