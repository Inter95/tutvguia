from urllib import urlencode
from urllib import urlencode
from tools import *

try:
    import simplejson as json
except:
    import json

# define database
storage = Storage("hdfulltv.txt", "list")


######################################
#############  CLASSES #################
######################################
class Movies:
    def __init__(self):
        self.titles = []
        self.urlList = []

    def searchMovie(self, urlSearch):
        settings.log(message=urlSearch)
        settings.notification(message="Buscando en linea... %s" % urlSearch[urlSearch.rfind("/") + 1:])
        goodSpider()
        response = browser.get(urlSearch)
        if response.status_code == requests.codes.ok:
            info = re.findall('<a class="link" href="%s/pelicula/(.*?)" title="(.*?)"' % settings.value["urlAddress"],
                              response.text)
            for item in info:
                self.urlList.append(settings.value["urlAddress"] + '/pelicula/' + item[0])
                self.titles.append(item[0][item[0].rfind("/") + 1:])
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
            settings.notification(message="HTTP %s" % response.code, force=True)


class Shows:
    def __init__(self):
        self.titles = []
        self.urlList = []

    def searchSerie(self, urlSerie=""):
        settings.log(message=urlSerie)
        settings.notification(message="Buscando en linea... %s" % urlSerie[urlSerie.rfind("/") + 1:])
        goodSpider()
        response = browser.get(urlSerie)  # open the serie
        if response.status_code == requests.codes.ok:
            html = response.text
            seasons = re.findall("/temporada-(.*?)'", html)
            seasons = list(set(seasons))
            sid = re.findall("var sid = '(.*?)'", html)[0]
            for season in seasons:
                urlSearch = "%s/a/episodes" % settings.value["urlAddress"]
                goodSpider()
                response = browser.post(urlSearch, data={"action": "season", "start": "0", "limit": "0", "show": sid,
                                                         "season": season})
                if response.status_code == requests.codes.ok:
                    data = response.json()
                    for item in data:
                        self.urlList.append(
                            settings.value["urlAddress"] + '/serie/' + item['permalink'] + '/temporada-' + item[
                                'season'] + '/episodio-' +
                            item['episode'])
                        self.titles.append(item['show']['title']['en'] + " S%sE%s" % (
                            item['season'], item['episode']))  # get the title
                else:
                    settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
                    settings.notification(message="HTTP %s" % response.code, force=True)
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
            settings.notification(message="HTTP %s" % response.code, force=True)

    def searchEpisode(self, urlEpisode="", action=""):
        settings.log(message=urlEpisode)
        settings.notification(message="Buscando en linea... %s" % urlEpisode[urlEpisode.rfind("/") + 1:])
        goodSpider()
        response = browser.get(urlEpisode, urlencode({"action": action, "start": "0", "limit": "24", "elang": "ALL"}))
        if response.status_code == requests.codes.ok:
            data = response.json()
            for item in data:
                self.urlList.append(
                    settings.value["urlAddress"] + '/serie/' + item['permalink'] + '/temporada-' + item[
                        'season'] + '/episodio-' + item['episode'])
                self.titles.append(
                    item['show']['title']['en'] + " S%sE%s" % (item['season'], item['episode']))  # get the title
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
            settings.notification(message="HTTP %s" % response.code, force=True)
