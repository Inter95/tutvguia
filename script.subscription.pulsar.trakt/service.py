# coding: utf-8
from tools import *
from time import time
from time import asctime
from time import localtime
from time import strftime
from time import gmtime


def update_service():
    if settings.value['service'] == 'true':
        categories = {settings.string(32105): 'http://trakt.tv/movies/popular',
                      settings.string(32106): 'http://trakt.tv/movies/trending',
                      settings.string(32107): 'http://trakt.tv/shows/popular',
                      settings.string(32108): 'http://trakt.tv/shows/trending',
                      settings.string(32110): '',  # watchlist
                      settings.string(32101): ''  # list
                      }
        options = categories.keys()
        options.sort()
        rets = []
        lists = []
        if settings.value["moviesPopular"] == 'true':
            rets.append(options.index(settings.string(32105)))
        if settings.value["moviesTrending"] == 'true':
            rets.append(options.index(settings.string(32106)))
        if settings.value["tvPopular"] == 'true':
            rets.append(options.index(settings.string(32107)))
        if settings.value["tvTrending"] == 'true':
            rets.append(options.index(settings.string(32108)))
        if settings.value["watchlist"] == 'true' and settings.value["user"] is not '':
            rets.append(options.index(settings.string(32110)))
        if settings.value["syncList"] == 'true' and settings.value["user"] is not '':
            rets.append(options.index(settings.string(32101)))
        # start checking
        for ret in rets:
            if options[ret] == settings.string(32110):  # watchlist
                categories[options[ret]] = 'http://trakt.tv/users/%s/watchlist' % settings.value["user"].lower()
            if options[ret] == settings.string(32101):  # List
                categories[options[ret]] = "http://trakt.tv"
                settings.log("http://trakt.tv/users/%s/lists/" % settings.value["user"].lower())
                response = browser.get('http://trakt.tv/users/%s/lists/' % settings.value["user"].lower())
                soup = bs4.BeautifulSoup(response.text)
                links = soup.select("div.posters a")
                for link in links:
                    lists.append(link.attrs.get("href"))
            url_search = categories[options[ret]]  # define the url search
            ID = []  # IMDB_ID or thetvdb ID
            cm = 0
            marker = True if settings.value["marker"] == "true" else False
            while True:
                settings.notification(settings.string(32044))
                if len(lists) > 0 and (not marker or (marker and "pulsar" in lists[cm])):
                    settings.log(url_search + lists[cm])
                    response = browser.get(url_search + lists[cm])
                    settings.log(url_search + lists[cm])
                else:
                    settings.log(url_search)
                    response = browser.get(url_search)
                    settings.log(url_search)

                if response.status_code == requests.codes.ok:
                    titlesMovies = []
                    titlesShows = []

                    soup = bs4.BeautifulSoup(response.text)
                    links = soup.select("div.row.fanarts div.grid-item > a")
                    if len(links) == 0:  # it is the list
                        links = soup.select("div.row.posters div.grid-item > a")

                    for link in links:
                        subLinks = link.select('div.titles h3')
                        if len(subLinks) > 0:
                            url = link.attrs.get("href")
                            title = subLinks[0].text
                            if "movies" in url:
                                tempYear = link.parent.attrs.get("data-title")
                                if tempYear is not None:
                                    year = formatTitle(tempYear)["year"]
                                    titlesMovies.append(title + " %s" % year)
                                else:
                                    titlesMovies.append(title)
                            else:
                                titlesShows.append(title)

                    if len(titlesMovies) > 0:  # there is movies
                        subscription(titles=titlesMovies, id=ID, typeList='MOVIE', folder=settings.movieFolder,
                                     silence=True)

                    if len(titlesShows) > 0:  # there is tv shows
                        subscription(titles=titlesShows, id=ID, typeList='SHOW', folder=settings.showFolder,
                                     silence=True)
                else:
                    settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
                    settings.notification(message="HTTP %s" % response.status_code, force=True)
                    break

                cm += 1
                if cm >= len(lists): break


if settings.value['service'] == 'true':
    sleep(int(settings.value['delayTime']))  # get the delay to allow pulsar starts
    every = 28800  # seconds
    previous_time = time()
    settings.log("Persistent Update Service starting...")
    update_service()
    while (not xbmc.abortRequested) and settings.value["persistent"] == 'true':
        if time() >= previous_time + every:  # verification
            previous_time = time()
            update_service()
            settings.log('Update List at %s' % asctime(localtime(previous_time)))
            settings.log('Next Update in %s' % strftime("%H:%M:%S", gmtime(every)))
            update_service()
        sleep(1)

del settings
del browser
