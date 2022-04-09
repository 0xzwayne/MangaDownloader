

class Mangas:
    def __init__(self, manga, startchapter, endchapter):
        self.name = manga
        self.start = startchapter
        self.end = endchapter
        self.urls = [f"https://www.scan-fr.cc/manga/{self.name}/{i}/1" for i in range(self.start, self.end+1)]
        

class Manga(Mangas):
    """
    Telecharger un seul tome
    """
    def __init__(self,manga,chapter):
        super().__init__(manga,chapter,chapter)