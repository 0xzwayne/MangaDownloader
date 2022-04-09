import httpx
from lib.manga import Manga
import aiofiles
from pathlib import Path
from bs4 import BeautifulSoup
import os
import threading
from time import sleep
import colorama
from colorama import Fore, init
import asyncio

init(convert=True)


class downloader:
    """ Telecharger toutes les images du manga avec httpx asynchrone
    
    Pack le manga dans un fichier cbz et le renommer avec le nom du tome """
    
    def __init__(self, manga:Manga):
        self.manga = manga
        self.dlpath = f"{Path(__file__).resolve().parents[1]}\downloads\{self.manga.name}_{self.manga.start}_{self.manga.end}"
        self.downloading = None
        #self.displaythread = None
        print(f"Telechargement de {self.manga.name} : {self.manga.start} à {self.manga.end}")
    
    async def download(self):
        
        #on cree le dossier s'il n'existe pas deja
        if not os.path.exists(self.dlpath):
            os.mkdir(self.dlpath)
            
        #boucle chaque chapitre a telecharger
        for url in self.manga.urls:
            numero_chapitre = url.split("/")[5]
            #print(numero_chapitre)
            self.downloading = numero_chapitre
            
            threading.Thread(target=self.displayupdate, daemon=True).start()
            
            #on telecharge les liens des images pour chaque page du tome
            urls = await downloader.fetchurls(url)
            
            page=1
            for url in urls:
               #page = int(url.split("/")[8].split(".")[0])
                #print(page)
                await self.fetchimage(numero_chapitre, page, url.strip())
                page+=1
        self.downloading = None
        print(Fore.GREEN + "Telechargement terminé                                           ")
        print(f"Dossier de téléchargement : {self.dlpath}" + Fore.RESET)
            


    async def fetchimage(self, chapter, page, url):
        async with httpx.AsyncClient() as cl:
            #print(url)
            rep:httpx.Response = await cl.get(url)
            img = rep.read()
            await cl.aclose()
            async with aiofiles.open(f"{self.dlpath}\{chapter}_{page}.jpg", 'wb+') as f:
                await f.write(img)
            
            
            
    async def fetchurls(url):
        #print("fetch")
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as cl:
            rep:httpx.Response = await cl.get(url)
            #print(rep.status_code)
            
            #url error
            if rep.status_code == 500:
                print(f"[ERREUR 500] url non valide : {url}")
                return
            
            
            #print(rep.status_code)
            return downloader.linksfromhtml(rep.content)
            
    #parse the links from full html page of the chapter
    def linksfromhtml(content):
        urls = []
        soup = BeautifulSoup(content, "lxml")
        for i in soup.find_all("img"):
            try:
                urls.append(i["data-src"])
            except:
                ...
        return urls
    
    def displayupdate(self):
        print(end='\r')
        while self.downloading != None:
            print(Fore.RED + f"Telechargement du chapitre {self.manga.name} {self.downloading}...", end="\r")
            sleep(1)
        
        
        

    
    
    
if __name__ == "__main__":
    ...