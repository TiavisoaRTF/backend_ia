from fastapi import FastAPI
from routers import chat ,agent

app = FastAPI()

app.include_router(chat.router)
app.include_router(agent.router)

@app.get("/")
def accueil():
    return {"message": "API de chat"}