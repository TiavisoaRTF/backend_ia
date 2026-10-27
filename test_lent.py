import asyncio
import time

async def tache(nom, duree):
    print(f"{nom} : début")
    await asyncio.sleep(duree)
    print(f"{nom} : fin")

async def main():
    debut = time.time()

    await asyncio.gather(
        tache("A", 2),
        tache("B", 2),
        tache("C", 2),
    )

    print(f"Total : {time.time() - debut:.1f} s")

asyncio.run(main())