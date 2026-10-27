# import asyncio
# import os
# import time
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()

# MODELE = "gemini-3.8-flash"
# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# async def poser(question):
#     reponse = await client.aio.models.generate_content(
#         model=MODELE,
#         contents=question
#     )
#     return reponse.text


# async def main():
#     debut = time.time()

#     resultats = await asyncio.gather(
#         poser("Qu'est-ce qu'une API REST ? En une phrase."),
#         poser("Qu'est-ce que le JSON ? En une phrase."),
#         poser("Qu'est-ce que le protocole HTTP ? En une phrase."),
#     )

#     for r in resultats:
#         print(r.strip())
#         print()

#     print(f"Total : {time.time() - debut:.1f} s")


# asyncio.run(main())
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODELE = "gemini-3.8-flash"
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def poser(question):
    reponse = client.models.generate_content(
        model=MODELE,
        contents=question
    )
    return reponse.text


def main():
    debut = time.time()

    resultats = [
        poser("Qu'est-ce qu'une API REST ? En une phrase."),
        poser("Qu'est-ce que le JSON ? En une phrase."),
        poser("Qu'est-ce que le protocole HTTP ? En une phrase."),
    ]

    for r in resultats:
        print(r.strip())
        print()

    print(f"Total : {time.time() - debut:.1f} s")


main()