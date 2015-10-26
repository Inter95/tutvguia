# coding: utf-8

import tools
# import lib.simplejson as json
import lib.mechanize as mechanize
import lib.bs4 as bs4

# this read the settings
settings = tools.Settings()

# define the browser
browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.set_handle_equiv(False)
browser.addheaders = [('User-agent',
                       'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


# define database
storage = tools.Storage("yaske.txt", "dict")


######################################
#############  CLASSES #################
######################################
class Menu:
    def __init__(self, type="movie", url="", channel="", order=""):
        self.url = url
        self.type = type
        self.channel = channel
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
                    urlSearch = urlSearch.replace("URL", settings.url_address)
                    urlSearch = urlSearch.replace("PAGE", str(page))
                    movie.searchMovie(urlSearch=urlSearch)
                    if page % 5 == 0: sleep(1)

                if optionUnica:
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
            if self.type == "show":  # add Shows
                from urllib import urlencode
                show = Shows()
                for page in range(1, settings.pages + 1):
                    parameters = {'grupo_no': page, 'type': 'series', 'order': self.order}
                    urlSearch = self.url
                    urlSearch = urlSearch.replace("URL", settings.url_address2)
                    show.searchShow(urlSearch=urlSearch, parameters=urlencode(parameters))
                    if page % 5 == 0: sleep(1)

                if optionUnica:
                    rep = settings.dialog.select('Seleccionar tu opción:', show.titles + ['CANCEL'])
                    if rep < len(show.titles):
                        show.searchEpisodes(urlSearch=show.url_list[rep])
                        tools.int_pelisalacarta(channel=self.channel, titles=show.titles,
                                                url=show.url_list,
                                                type_list='SHOW', folder=settings.show_folder,
                                                name_provider=settings.name_provider)
                else:
                    if len(show.titles) > 0:
                        urlShows= show.url_list
                        show.url_list=[]
                        show.titles=[]
                        for url in urlShows:
                            show.searchEpisodes(urlSearch=url)
                        tools.int_pelisalacarta(channel=self.channel, titles=show.titles, url=show.url_list,
                                                    type_list='SHOW', folder=settings.show_folder,
                                                    name_provider=settings.name_provider, silence=True)



class Movies:
    def __init__(self):
        self.titles = []
        self.url_list = []

    def searchMovie(self, urlSearch):
        settings.log(message=urlSearch)
        settings.notification(message="Buscando en linea... %s" % urlSearch[urlSearch.rfind("/") + 1:])
        response = browser.open(urlSearch)
        if response.code == 200:
            soup = bs4.BeautifulSoup(response.read())
            links = soup.select('li.item-movies a.image-block')
            for link in links:
                self.url_list.append(link.attrs.get('href'))
                self.titles.append(link.attrs.get('title'))
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
            settings.notification(message="HTTP %s" % response.code, force=True)


class Shows:
    def __init__(self):
        self.titles = []
        self.url_list = []

    def searchShow(self, urlSearch="", parameters=""):
        settings.log(message=urlSearch)
        settings.notification(message="Buscando en linea... %s" % urlSearch[urlSearch.rfind("/") + 1:])
        response = browser.open(urlSearch, parameters)  # open the serie
        if response.code == 200:
            soup = bs4.BeautifulSoup(response.read())
            links = soup.select('a')
            for link in links:
                self.url_list.append(link.attrs.get('href'))
                self.titles.append(link.div.text.strip())
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
            settings.notification(message="HTTP %s" % response.code, force=True)

    def searchEpisodes(self, urlSearch=""):
        title = urlSearch[urlSearch.rfind("/") + 1:-5]
        settings.log(message=urlSearch)
        settings.notification(message="Buscando en linea... %s" % urlSearch[urlSearch.rfind("/") + 1:])
        response = browser.open(urlSearch)  # open the serie
        if response.code == 200:
            soup = bs4.BeautifulSoup(response.read())
            links = soup.select('td.sape a')
            for link in links:
                self.url_list.append(link.attrs.get('href'))
                self.titles.append(link.text)
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
            settings.notification(message="HTTP %s" % response.code, force=True)
