from urllib import urlencode

import tools
import lib.simplejson as json
import lib.mechanize as mechanize

# this read the settings
settings = tools.Settings()

# define the browser
# browser = tools.Browser()
browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.set_handle_equiv(False)
browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#define database
storage = tools.Storage("hdfulltv.txt", "list")

#define htmlParser
scraper = tools.HtmlScraper()

######################################
#############  CLASSES #################
######################################
class Movies:
    def __init__(self):
        self.titles = []
        self.url_list = []

    def searchMovie(self, url_search):
        settings.log(message=url_search)
        settings.notification(message="Buscando en linea... %s" % url_search[url_search.rfind("/") + 1:])

        response = browser.open(url_search)
        if response.code == 200:
            scraper.html = response.read()
            scraper.findAll(key='div class="top"')
            self.url_list.extend(scraper.aHref[0])
            self.titles.extend(scraper.imgAlt[0])
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
            settings.notification(message="HTTP %s" % response.code, force=True)


class Shows:
    def __init__(self):
        self.titles = []
        self.url_list = []

    def searchSerie(self, url_serie=""):
        import re
        settings.log(message=url_serie)
        settings.notification(message="Buscando en linea... %s" % url_serie[url_serie.rfind("/") + 1:])
        response = browser.open(url_serie)  # open the serie
        if response.code == 200:
            html = response.read()
            seasons = re.findall("/temporada-(.*?)'", html)
            seasons = list(set(seasons))
            sid = re.findall("var sid = '(.*?)'", html)[0]
            for season in seasons:
                url_search = "%s/a/episodes" % settings.url_address
                response = browser.open(url_search, urlencode(
                    {"action": "season", "start": "0", "limit": "0", "show": sid, "season": season}))
                if response.code == 200:
                    data = json.loads(response.read())
                    for item in data:
                        self.url_list.append(
                            settings.url_address + '/serie/' + item['permalink'] + '/temporada-' + item[
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

    def searchEpisode(self, url_episode="", action=""):
        settings.log(message=url_episode)
        settings.notification(message="Buscando en linea... %s" % url_episode[url_episode.rfind("/") + 1:])
        response = browser.open(url_episode, urlencode({"action": action, "start": "0", "limit": "24", "elang": "ALL"}))
        if response.code == 200:
            data = json.loads(response.read())
            for item in data:
                self.url_list.append(
                    settings.url_address + '/serie/' + item['permalink'] + '/temporada-' + item[
                        'season'] + '/episodio-' + item['episode'])
                self.titles.append(
                    item['show']['title']['en'] + " S%sE%s" % (item['season'], item['episode']))  # get the title
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
            settings.notification(message="HTTP %s" % response.code, force=True)

