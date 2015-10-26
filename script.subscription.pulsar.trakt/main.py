# coding: utf-8
from tools import *

categories = {settings.string(32105): 'http://trakt.tv/movies/popular',
              settings.string(32106): 'http://trakt.tv/movies/trending',
              settings.string(32107): 'http://trakt.tv/shows/popular',
              settings.string(32108): 'http://trakt.tv/shows/trending',
              settings.string(32110): '',  # watchlist
              settings.string(32101): ''  # list
              }
options = categories.keys()
options.sort()

lists = []
ret = settings.dialog.select(settings.string(32100), options + [settings.string(32015),  # Erase Folders
                                                                settings.string(32016),  # -SETTINGS
                                                                settings.string(32017),  # -HELP
                                                                settings.string(32018)  # Exit
                                                                ])

if ret < len(options):  # Exit
    if options[ret] == settings.string(32110):  # WatchList
        user = settings.dialog.input(settings.string(321091), settings.value["user"])
        categories[options[ret]] = 'http://trakt.tv/users/%s/watchlist' % user.lower()

    if options[ret] == settings.string(32101):  # List
        user = settings.dialog.input(settings.string(321091), settings.value["user"])
        # password = settings.dialog.input('Password:', password, option=2)
        # browser.open('http://trakt.tv/auth/signin')
        # token = re.search('name="authenticity_token" value="(.*?)"', browser.content).group(1)
        # print '************************************'
        # print token
        # browser.login('http://trakt.tv/auth/signin', {'utf8': '&#x2713;', 'user[login]': user,
        # 'user[password]': password, 'commit': 'Sign in',
        # 'user[remember_me]': 1,
        # 'authenticity_token': token})
        categories[options[ret]] = "http://trakt.tv"
        settings.log("http://trakt.tv/users/%s/lists/" % user.lower())
        response = browser.get('http://trakt.tv/users/%s/lists/' % user.lower())
        soup = bs4.BeautifulSoup(response.text)
        links = soup.select("div.posters a")
        for link in links:
            lists.append(link.attrs.get("href"))

    # main
    url_search = categories[options[ret]]  # define the url search
    if url_search is not '':
        listing = []
        ID = []  # IMDB_ID or thetvdb ID
        cm = 0
        marker = settings.dialog.yesno(settings.cleanName, "Which list do you want to integrate?",
                                       yeslabel="only with #PULSAR& marker", nolabel="All")
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
                    subscription(titles=titlesMovies, id=ID, typeList='MOVIE', folder=settings.movieFolder)

                if len(titlesShows) > 0:  # there is tv shows
                    subscription(titles=titlesShows, id=ID, typeList='SHOW', folder=settings.showFolder)
            else:
                settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
                settings.notification(message="HTTP %s" % response.status_code, force=True)
                break

            cm += 1
            if cm >= len(lists): break

if ret == len(options):  # Erase Folder
    selectionRemove = settings.dialog.select(settings.string(32010),
                                             [settings.string(32022), settings.string(32023),
                                              settings.string(32024)])
    if selectionRemove == 0:
        removeDirectory(settings.movieFolder)
    else:
        removeDirectory(settings.showFolder)

if ret == len(options) + 1:  # Settings
    settings.settings.openSettings()
    del settings
    settings = Settings()

if ret == len(options) + 2:  # Help
    settings.dialog.ok(settings.string(32017), settings.string(32025))

del settings
del browser
