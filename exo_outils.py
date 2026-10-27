import os
from datetime import datetime
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

load_dotenv()


@tool
def heure_actuelle() -> str:
    """Donne l'heure et la date actuelles."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")


modele = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

agent = create_agent(model=modele, tools=[heure_actuelle])

resultat = agent.invoke({"messages": [{"role": "user", "content": "Quelle heure est-il ?"}]})

print(resultat["messages"][-1].content)