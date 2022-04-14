import asyncio
import lib.manga as manga
from lib.downloader import downloader
import lib.database as db

def main(manga_name,start,end):
    test = manga.Mangas(manga_name,start,end)


    dl1 = downloader(test)
    
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(dl1.download())
    input("Appuyez sur entrée pour quitter")
    
def input_numberonly(text):
    try:
        i = int(input(text))
    except:
        print("choix incorrect, entrez un nombre")
        return input_numberonly(text)
    return i
    
def choix_manga() -> str:
    """
    Ask for manga name until at least a result is found on the database 
    Returns:
        str: manga name
    """
    manga_name = input("Quel manga telecharger >> ")
    results = db.search(manga_name)
    if results == []:
        print("aucun resultat")
        return choix_manga()
    n=0
    for result in results:
        print(f"[{n}] - {result[0]}")
        n+=1
    print("[-1] - Retour a la recherche")
    
    choix = input_numberonly("votre choix >> ")
    
    if choix == -1:
        return choix_manga()
    
    url = results[choix][1]
    print("\n")
    #on retourne le tag du manga sur le site
    print(f"choix : {results[choix][0]}")
    return url.split("/")[4]
    
    
    
if __name__ == "__main__":
    
    print("---Manga Downloader v1.0.0 by Zwayne---")
    print("\n")

    manga_name = choix_manga()
    start = input("chapitre de debut >> ")
    end = input("chapitre de fin >> ")
    main(manga_name, int(start), int(end))
