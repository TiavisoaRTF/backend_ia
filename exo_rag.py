import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

with open("reglement.txt", encoding="utf-8") as f:
    texte = f.read()

decoupeur = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
morceaux = decoupeur.split_text(texte)

print(f"Document découpé en {len(morceaux)} morceaux\n")

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

base = Chroma.from_texts(morceaux, embeddings)

question = "ai-je droit à un congé pour déménagement ?"
resultats = base.similarity_search(question, k=2)

print(f"Question : {question}\n")
for i, doc in enumerate(resultats, 1):
    print(f"--- Morceau {i} ---")
    print(doc.page_content)
    print()
    contexte = "\n\n".join(doc.page_content for doc in resultats)

prompt = f"""Réponds à la question en te basant uniquement sur les extraits du règlement ci-dessous.
Si la réponse ne s'y trouve pas, dis-le clairement.

Extraits :
{contexte}

Question : {question}"""

modele = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
print("=== RÉPONSE ===")
print(modele.invoke(prompt).text)