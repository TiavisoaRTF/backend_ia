from fastapi import FastAPI
from routers import chat ,agent,workflow

app = FastAPI()

app.include_router(chat.router)
app.include_router(agent.router)

@app.get("/")
def accueil():
    return {"message": "API de chat"}
@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(workflow.router)