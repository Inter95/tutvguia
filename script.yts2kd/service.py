# coding: utf-8
import re
import tools
import json
from time import time
from time import asctime
from time import localtime
from time import strftime
from time import gmtime
from xbmc import log
from xbmc import sleep
from xbmc import abortRequested
from xbmcaddon import Addon


def update_service():
    # this read the settings
    settings = tools.Settings()
    # define the browser
    browser = tools.Browser()
    #Begin Service
    if settings.service == 'true':
        if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Checking Online...', settings.icon, settings.time_noti)
        quality = Addon().getSetting('quality')
        text = '&minimum_rating=%s' % Addon().getSetting('minimum')
        sort = Addon().getSetting('sort')
        url_search = "%s/api/v2/list_movies.json?limit=50&quality=%s&sort_by=%s&order_by=desc" % (settings.url_address, quality, sort.lower().replace(' ', '_'))
        settings.log(url_search)
        title = []
        magnet = []
        for page in range(settings.pages):
            if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Checking Online, Page %s...'
                                                                    % str(page + 1), settings.icon, settings.time_noti)
            if browser.open(url_search):
                data = json.loads(browser.content)
                for movie in data['data']['movies']:
                    if movie.has_key('torrents'):
                        for torrent in movie['torrents']:
                            if torrent['quality'] in quality:
                                title.append(movie['title_long'])
                                magnet.append('magnet:?xt=urn:btih:%s' % torrent['hash'])
        if len(title) > 0:
            tools.integration(filename=title, magnet=magnet, type_list='MOVIE', folder=settings.movie_folder, silence=True, name_provider=settings.name_provider)
        else:
            settings.log('[%s] >>>>>>>%s<<<<<<<' % (settings.name_provider_clean, browser.status))
            settings.dialog.notification(settings.name_provider, browser.status, settings.icon, 1000)
    del settings
    del browser


if Addon().getSetting('service') == 'true':
    persistent = Addon().getSetting('persistent')
    name_provider = re.sub('.COLOR (.*?)]', '', Addon().getAddonInfo('name').replace('[/COLOR]', ''))
    every = 28800  # seconds
    previous_time = time()
    log("[%s]Update Service starting..." % name_provider)
    update_service()
    while (not abortRequested) and persistent == 'true':
        if time() >= previous_time + every:  # verification
            previous_time = time()
            update_service()
            log('[%s] Update List at %s' % (name_provider, asctime(localtime(previous_time))))
            log('[%s] Next Update in %s' % (name_provider, strftime("%H:%M:%S", gmtime(every))))
            update_service()
        sleep(500)
