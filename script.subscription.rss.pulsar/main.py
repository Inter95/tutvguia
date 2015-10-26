# coding: utf-8
import re
import subscription
import shelve
import xbmc


# this read the settings
settings = subscription.Settings()
browser = subscription.Browser()

# define the browser
list_url_search = []
path = xbmc.translatePath('special://temp')
database = shelve.open(path + 'SUBSCRIPTION-PULSAR-RSS.db')
rep = 0
Dict_RSS = {}
if database.has_key('dict'):
    Dict_RSS = database['dict']
while rep < 5:
    rep = settings.dialog.select('Choose an Option:',
                                 ['Add a New RSS', 'Remove a RSS', 'Modify Saved RSS', 'View Saved RSS list',
                                  'Read RSS list and create .strm Files',  '-SETTINGS', '-HELP', 'Exit'])
    if rep == 0:  # Add a New RSS
        selection = settings.dialog.input('URL RSS:')
        name = ''
        while name is '':
            name = settings.dialog.input('Name to this RSS:').title()
        Dict_RSS[name] = selection
        database['dict'] = Dict_RSS
        database.sync()
    if rep == 1 and len(Dict_RSS.keys()) > 0:  # Remove a RSS
        List = [name + ": " + RSS for (name, RSS) in zip(Dict_RSS.keys(), Dict_RSS.values())]
        list_rep = settings.dialog.select('Choose RSS to Remove', List + ['CANCEL'])
        if list_rep < len (List):
            if settings.dialog.yesno('', 'Do you want Remove %s?' % List[list_rep]):
                del Dict_RSS[Dict_RSS.keys()[list_rep]]
                database['dict'] = Dict_RSS
                database.sync()
    if rep == 2:  # Modify RSS list
        List = [name + ": " + RSS for (name, RSS) in zip(Dict_RSS.keys(), Dict_RSS.values())]
        list_rep = settings.dialog.select('Shows', List + ['CANCEL'])
        if list_rep < len(List):
            name = Dict_RSS.keys()[list_rep]
            Dict_RSS[name] = settings.dialog.input('URL RSS:', Dict_RSS[name])
            database['dict'] = Dict_RSS
            database.sync()
    if rep == 3:  # View Saved RSS list
        List = [name + ": " + RSS for (name, RSS) in zip(Dict_RSS.keys(), Dict_RSS.values())]
        settings.dialog.select('Shows', List)
    if rep == 4:
        list_url_search = Dict_RSS.values()
        if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Checking Online...', settings.icon, settings.time_noti)
        # Begin reading
        for url_search in list_url_search:
            if url_search is not '':
                title_movie = []
                movie_ID = []
                title_show = []
                if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Checking %s...' % url_search, settings.icon, settings.time_noti)
                acum = 0
                settings.log('[%s]%s' % (settings.name_provider_clean, url_search))
                if browser.open(url_search):
                    items = re.findall('<item>(.*?)</item>', browser.content, re.S)
                    for item in items:
                        s_title = re.findall('title>(.*?)<', item)
                        s_link = re.findall('link>(.*?)<', item)
                        IMDB = re.search('TT[0-9]+', s_link[0] + ' #TT00', re.I).group(0)
                        if s_title[0] != '':
                            info = subscription.format_title(s_title[0])
                            if 'MOVIE' in info['type'] and 'TV Series' not in s_title[0]:
                                title_movie.append(s_title[0])
                                if 'TT00' not in IMDB:
                                    movie_ID.append(IMDB)
                                acum += 1
                            if 'SHOW' in info['type'] or 'TV Series' in s_title[0]:
                                title_show.append(s_title[0].replace('TV Series', ''))
                                acum += 1
                    if acum == 0:
                        if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'No Movies nor Shows!!', settings.icon, settings.time_noti)
                    if len(title_movie) > 0:
                        subscription.integration(listing=title_movie, ID=movie_ID, type_list='MOVIE', folder=settings.movie_folder, name_provider=settings.name_provider)
                    if len(title_show) > 0:
                        print title_show
                        subscription.integration(listing=title_show, ID=[], type_list='SHOW', folder=settings.show_folder, name_provider=settings.name_provider)
                else:
                    settings.log('[%s]>>>>>>>%s<<<<<<<' % (settings.name_provider_clean, browser.status))
                    settings.dialog.notification(settings.name_provider, browser.status, settings.icon, 1000)
    if rep == 5:  # Settings
        settings.settings.openSettings()
    if rep == 6:  # Help
        settings.dialog.ok("Help",
                           "Please, check this address to find the user's operation:\n[B]http://goo.gl/8nYU6R[/B]")

database.close()
del browser
del settings