# coding: utf-8

import tools
# import lib.simplejson as json
import requests
import bs4

# this read the settings
settings = tools.Settings()

# define the browser
browser = requests.Session()
browser.headers[
    'User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'


# define database
storage = tools.Storage("videoteca-series.txt", "dict")
storageAnime = tools.Storage("videoteca-anime.txt", "dict")


######################################
#############  CLASSES #################
######################################
class Menu:
    def __init__(self, type="movie", url="", channel="", type2="", order=""):
        self.url = url
        self.type = type
        self.channel = channel
        self.type2 = type2
        self.order = order

    def play(self, silence=False):
        if self.type == "erase-movie":  # Erase a movie
            from os import listdir
            from xbmc import translatePath

            folder = settings.movie_folder
            folder = folder.replace('special://temp/', translatePath('special://temp'))
            folder = folder.replace('smb:', '')  # network compatibility
            list_movies = listdir(folder)
            rep = settings.dialog.select('Seleccionar la película a borrar:', list_movies + ['-CANCELAR'])
            if rep < len(list_movies):
                if settings.dialog.yesno("Atención!", "Desea borrar los archivos strm?", nolabel="No", yeslabel="Si"):
                    tools.removeDirectory(folder=settings.movie_folder, title=list_movies[rep])
        elif self.type == "erase-show":  # Erase a show
            from os import listdir
            from xbmc import translatePath
        else:
            from time import sleep
            if not silence:
                settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
            if settings.pages == '' or settings.pages == 0:
                settings.pages = "1"
            settings.pages = int(settings.pages)

            if silence:  # for the service
                optionUnica = False
            else:
                optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección",
                                                    yeslabel="Individual", nolabel="Todas")
            if self.type == "movie":  # add movies
                movie = Movies()
                for page in range(1, settings.pages + 1):
                    urlSearch = self.url
                    if page==1 and ("genero" not in urlSearch) and ("?search=" not in urlSearch):
                        urlSearch = "URL"  # first page different TODAS
                    if page==1 and ("genero" in urlSearch):
                        urlSearch = urlSearch.replace("/page/PAGE/", "/")  # first page different with genre
                    urlSearch = urlSearch.replace("URL", settings.url_address)
                    urlSearch = urlSearch.replace("PAGE", str(page))
                    movie.searchMovie(urlSearch=urlSearch)
                    if page % 5 == 0: sleep(1)

                if optionUnica or "?search=" in urlSearch:
                    rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
                    if rep < len(movie.titles):
                        tools.int_pelisalacarta(channel=self.channel, titles=[movie.titles[rep]],
                                                url=[movie.url_list[rep]],
                                                type_list='MOVIE', folder=settings.movie_folder,
                                                name_provider=settings.name_provider)
                else:
                    if len(movie.titles) > 0:
                        tools.int_pelisalacarta(channel=self.channel, titles=movie.titles, url=movie.url_list,
                                                type_list='MOVIE', folder=settings.movie_folder,
                                                name_provider=settings.name_provider, silence=silence)
            elif self.type == "show":  # add Shows
                show = Shows()
                for page in range(1, settings.pages + 1):
                    if self.type2 == "search":
                        parameters = ""
                    else:
                        parameters = {'grupo_no': page, 'type': self.type2, 'order': self.order}
                    urlSearch = self.url
                    urlSearch = urlSearch.replace("URL", settings.url_address2)
                    show.searchShow(urlSearch=urlSearch, parameters=parameters)
                    if page % 5 == 0: sleep(1)

                if optionUnica or "?q=" in urlSearch:
                    rep = settings.dialog.select('Seleccionar tu opción:', show.titles + ['CANCEL'])
                    if rep < len(show.titles):
                        storage.add(key=show.titles[rep], info=show.url_list[rep])
                        show.searchEpisodes(urlSearch=show.url_list[rep], exclude="Animes", erase=True)
                        tools.int_pelisalacarta(channel=self.channel, titles=show.titles,
                                                url=show.url_list,
                                                type_list='SHOW', folder=settings.show_folder,
                                                name_provider=settings.name_provider)
                else:
                    if len(show.titles) > 0:
                        urlShows = show.url_list
                        titleShows = show.titles
                        show.url_list = []
                        show.titles = []
                        for cm, url in enumerate(urlShows):
                            storage.add(key=titleShows[cm], info=url)
                            show.searchEpisodes(urlSearch=url, exclude="Animes", erase=False)
                        tools.int_pelisalacarta(channel=self.channel, titles=show.titles, url=show.url_list,
                                                type_list='SHOW', folder=settings.show_folder,
                                                name_provider=settings.name_provider, silence=True)
            elif self.type == "anime":  # add Anime
                show = Shows()
                for page in range(1, settings.pages + 1):
                    if self.type2 == "search":
                        parameters = ""
                    else:
                        parameters = {'grupo_no': page, 'type': self.type2, 'order': self.order}
                    urlSearch = self.url
                    urlSearch = urlSearch.replace("URL", settings.url_address2)
                    show.searchShow(urlSearch=urlSearch, parameters=parameters)
                    if page % 5 == 0: sleep(1)

                if optionUnica:
                    rep = settings.dialog.select('Seleccionar tu opción:', show.titles + ['CANCEL'])
                    if rep < len(show.titles):
                        storageAnime.add(key=show.titles[rep], info=show.url_list[rep])
                        show.searchEpisodes(urlSearch=show.url_list[rep], erase=True)
                        for cm, title in enumerate(show.titles):  # convertir in EP00 format
                            pos = title.rfind(' ')
                            show.titles[cm] = title[:pos] + ' EP' + title[pos + 1:]
                        tools.int_pelisalacarta(channel=self.channel, titles=show.titles,
                                                url=show.url_list,
                                                type_list='SHOW', folder=settings.anime_folder,
                                                name_provider=settings.name_provider)
                else:
                    if len(show.titles) > 0:
                        urlShows = show.url_list
                        titleShows = show.titles
                        show.url_list = []
                        show.titles = []
                        for cm, url in enumerate(urlShows):
                            storageAnime.add(key=titleShows[cm], info=url)
                            show.searchEpisodes(urlSearch=url, erase=False)
                        for cm, title in enumerate(show.titles):  # convertir in EP00 format
                            pos = title.rfind(' ')
                            show.titles[cm] = title[:pos] + ' EP' + title[pos + 1:]
                        tools.int_pelisalacarta(channel=self.channel, titles=show.titles, url=show.url_list,
                                                type_list='SHOW', folder=settings.anime_folder,
                                                name_provider=settings.name_provider, silence=True)


class Movies:
    def __init__(self):
        self.titles = []
        self.url_list = []

    def searchMovie(self, urlSearch):
        from time import sleep
        settings.log(message=urlSearch)
        settings.notification(message="Buscando en linea... %s" % urlSearch[urlSearch.rfind("/") + 1:])
        tools.goodSpider()
        response = browser.get(settings.url_address, allow_redirects=True)
        response = browser.get(urlSearch, allow_redirects=True)
        if response.status_code == requests.codes.ok:
            soup = bs4.BeautifulSoup(response.text)
            links = soup.select('li.item-movies a.image-block')
            for link in links:
                self.url_list.append(link.attrs.get('href'))
                self.titles.append(link.attrs.get('title'))
        # else:
        #     settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
        #     settings.notification(message="HTTP %s" % response.status_code, force=True)


class Shows:
    def __init__(self):
        self.titles = []
        self.url_list = []

    def searchShow(self, urlSearch="", parameters=""):
        settings.log(message=urlSearch)
        settings.notification(message="Buscando en linea... %s" % urlSearch[urlSearch.rfind("/") + 1:])
        tools.goodSpider()
        response = browser.post(url=urlSearch, data=parameters)  # open the serie
        if response.status_code == requests.codes.ok:
            soup = bs4.BeautifulSoup(response.text)
            links = soup.select('a')
            for link in links:
                self.url_list.append(link.attrs.get('href'))
                if parameters == "":
                    self.titles.append(link.span.text)
                else:
                    self.titles.append(link.div.text.strip())
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
            settings.notification(message="HTTP %s" % response.status_code, force=True)

    def searchEpisodes(self, urlSearch="", exclude="", erase=True):
        settings.log(message=urlSearch)
        settings.notification(message="Buscando en linea... %s" % urlSearch[urlSearch.rfind("/") + 1:])
        if erase:
            self.url_list = []
            self.titles = []
        tools.goodSpider()
        response = browser.get(urlSearch)  # open the serie
        if response.status_code == requests.codes.ok:
            soup = bs4.BeautifulSoup(response.text)
            if soup.select('tr.mainInfoClass a')[0].text <> exclude:
                links = soup.select('td.sape a')
                for link in links:
                    self.url_list.append(link.attrs.get('href'))
                    self.titles.append(link.text)
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
            settings.notification(message="HTTP %s" % response.status_code, force=True)


def readOptions(url=""):
    result = (None, None)
    tools.goodSpider()
    response = browser.get(url)  # open the serie
    if response.status_code == requests.codes.ok:
        soup = bs4.BeautifulSoup(response.text)
        years = {" TODAS": ""}
        links = soup.select('form#form_custom select#years option')
        links.pop(0)
        for link in links:
            years[link.text] = link.attrs.get("value")
        genres = {" TODAS": ""}
        links = soup.select('form#form_custom select#genres option')
        links.pop(0)
        for link in links:
            genres[link.text] = link.attrs.get("value")
        result = (years, genres)
    else:
        settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
        settings.notification(message="HTTP %s" % response.status_code, force=True)
    return result
