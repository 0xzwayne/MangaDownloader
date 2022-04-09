from typing import List
import httpx
from bs4 import BeautifulSoup
from lxml import etree
import asyncio
import database

class browser:
    def __init__(self):
        self.allnames = []
    
    
    def getlistpages(self):
        """ On obtient le nombre de page présente sur la liste des mangas """
        url = "https://www.scan-fr.cc/manga-list"
        with httpx.Client(timeout=httpx.Timeout(15.0)) as cl:
            rep:httpx.Response = cl.get(url)
            soup = BeautifulSoup(rep.content, "lxml")
            pagelist = []
            for i in soup.find_all("ul", {"class": "pagination"})[0]:
                try:
                    page = int(str(i).split('page=')[1].split('">')[0])
                    pagelist.append(page)
                except:
                    ...
            pagelist.sort(reverse=True)
            return [f"https://www.scan-fr.cc/manga-list?page={i}" for i in range(1, pagelist[0]+1)]

    def parsemanganames(self,page):
        soup = BeautifulSoup(page)
        xpaths = [(f"/html/body/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/div[{x}]/div/div[2]/h5/a/strong//text()", f"/html/body/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/div[{x}]/div/div[2]/h5/a//@href") for x in range(1,20)]
        dom = etree.HTML(str(soup))
        
        names = []
        urls = []
        
        for path in xpaths:
            namepath = path[0]
            urlpath = path[1]
            try:
                #on recupere le nom du manga
                name = str(dom.xpath(namepath)[0])
                
                #on recupere l'url du manga
                url = str(dom.xpath(urlpath)[0])
                
            except:...
            
            self.allnames.append({"name": name,
                                 "url" : url})
            
            
    async def getallmanganames(self,urls:List):
        """ Telecharger tout les noms des mangas présent sur fr-scan-cc (https://www.scan-fr.cc/manga-list) """
        n=1
        async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as cl:
            for url in urls:
                print(f"parsing page {n}/{len(urls)}({len(self.allnames)} titles)...")
                rep = await cl.get(url)
                self.parsemanganames(rep.content)
                n+=1
        
        database.update(self.allnames)  

if __name__ == "__main__":
    br = browser()
    pages = br.getlistpages()
    asyncio.run(br.getallmanganames(pages))