# coding: utf-8
from tools import *

ret = settings.dialog.select(settings.string(32010),
                             [settings.string(32170),  # Manual Search
                              settings.string(32171),  # PreFixed List
                              settings.string(32016),  # -SETTINGS
                              settings.string(32017),  # -HELP
                              settings.string(32018)])  # Exit
if ret == 0:
    search = settings.dialog.input(settings.string(32172))  # Name Movie:
    if search is not '':
        urlSearch = '%s/ajax/search?query=%s' % (settings.value["urlAddress"], quote_plus(search))
        settings.notification(settings.string(32044))
        settings.log(urlSearch)
        response = browser.get(urlSearch)
        if response.status_code == requests.codes.ok:
            data = response.json()
            title = []
            urlSearch = []
            if 'Success' in data['message']:
                for item in data['data']:
                    title.append(item['title'])
                    urlSearch.append(item['url'].replace('\\', ''))
            rep = settings.dialog.select(settings.string(32173), title + ['CANCEL'])
            if rep < len(title):
                response=browser.get(urlSearch[rep])
                data = response.text
                qualities = re.findall('id="modal-quality-(.*?)"', data)
                magnet = re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)
                ret = settings.dialog.select(settings.string(32160), qualities + ['CANCEL'])
                if ret < len(qualities):
                    integration(titles=[title[rep]], id=[], magnets=[magnet[ret]], typeList='MOVIE',
                                folder=settings.movieFolder)
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
            settings.notification(message="HTTP %s" % response.status_code, force=True)
elif ret == 1:
    settings.pages = settings.dialog.numeric(0, settings.string(32163))  #'Number of Pages to download:'
    if settings.pages == '' or settings.pages == 0:
        settings.pages = "1"
    settings.pages = int(settings.pages)
    qualities = ['720p', '1080p', '3D']
    sorts = ['Year', 'Rating', 'Seeds', 'Downloaded Count', 'Like Count', 'Date Addded']
    quality = settings.dialog.select(settings.string(32160), qualities)  #Quality:
    minimum = settings.dialog.numeric(0, settings.string(32161)  + ' [0-9]:')
    if minimum == '':
        minimum = 0
    text = '&minimum_rating=%s' % minimum
    sort = settings.dialog.select(settings.string(32162), sorts)  #Sorting by
    urlSearch = "%s/api/v2/list_movies.json?limit=50&quality=%s&sort_by=%s&order_by=desc%s" % (
        settings.value["urlAddress"], qualities[quality], sorts[sort].lower().replace(' ', '_'), text)
    settings.log(urlSearch)
    titles = []
    id = []
    magnets = []
    for page in range(settings.pages):
        settings.notification(settings.string(32021) % "Page " + str(page + 1))
        settings.log(urlSearch)
        response = browser.get(urlSearch + '&page=' + str(page + 1))
        if response.status_code == requests.codes.ok:
            data = response.json()
            for movie in data['data']['movies']:
                if movie.has_key('torrents'):
                    for torrent in movie['torrents']:
                        if torrent['quality'] in qualities[quality]:
                            titles.append(movie['title_long'])
                            id.append(movie['imdb_code'])
                            magnets.append('magnet:?xt=urn:btih:%s' % torrent['hash'])
        if page % 5 == 0:
            sleep(1)
    if len(titles) > 0:
        integration(titles=titles, id=id, magnets=magnets, typeList='MOVIE', folder=settings.movieFolder)
    else:
        settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
        settings.notification(message="HTTP %s" % response.status_code, force=True)
elif ret == 2:  # Settings
    settings.settings.openSettings()
    settings = Settings()
elif ret == 3:  # Help
    settings.dialog.ok("Help", "Please, check this address to find the user's operation:\n[B]http://goo.gl/8nYU6R[/B]")

del settings
del browser
