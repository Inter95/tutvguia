# coding: utf-8
import re
import subscription
import shelve
from xbmc import translatePath
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
    settings = subscription.Settings()
    # define the browser
    browser = subscription.Browser()
    #Begin Service
    if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Checking Online...', settings.icon,
                                                            settings.time_noti)
    list_url_search = []
    path = translatePath('special://temp')
    database = shelve.open(path + 'SUBSCRIPTION-PULSAR-RSS.db')
    rep = 0
    Dict_RSS = {}
    if database.has_key('dict'):
        Dict_RSS = database['dict']
    database.close()
    list_url_search = Dict_RSS.values()
    if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Checking Online...', settings.icon,
                                                            settings.time_noti)
    # Begin reading
    for url_search in list_url_search:
        if url_search is not '':
            title_movie = []
            movie_ID = []
            title_show = []
            if settings.time_noti > 0: settings.dialog.notification(settings.name_provider,
                                        'Checking %s...' % url_search, settings.icon, settings.time_noti)
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
                    if settings.time_noti > 0: settings.dialog.notification(settings.name_provider,
                                                                            'No Movies nor Shows!!', settings.icon,
                                                                            settings.time_noti)
                if len(title_movie) > 0:
                    subscription.integration(listing=title_movie, ID=movie_ID, type_list='MOVIE', silence=True,
                                             folder=settings.movie_folder, name_provider=settings.name_provider)
                if len(title_show) > 0:
                    subscription.integration(listing=title_show, ID=[], type_list='SHOW', folder=settings.show_folder,
                                             silence=True, name_provider=settings.name_provider)
            else:
                settings.log('[%s]>>>>>>>%s<<<<<<<' % (settings.name_provider_clean, browser.status))
                settings.dialog.notification(settings.name_provider, browser.status, settings.icon, 1000)
    del settings
    del browser


if Addon().getSetting('service') == 'true':
    sleep(int(Addon().getSetting('delay_time'))*1000)  # get the delay to allow pulsar starts
    persistent = Addon().getSetting('persistent')
    name_provider = re.sub('.COLOR (.*?)]', '', Addon().getAddonInfo('name').replace('[/COLOR]', ''))
    every = 28800  # seconds
    previous_time = time()
    log("[%s] Update Service starting..." % name_provider)
    update_service()
    while (not abortRequested) and persistent == 'true':
        if time() >= previous_time + every:  # verification
            previous_time = time()
            if not xbmc.Player().isPlaying():
                update_service()
                log('[%s] Update List at %s' % (name_provider, asctime(localtime(previous_time))))
            else:
                log('[%s] Missed update, because the system was busy playing something' % name_provider)
            log('[%s] Next Update in %s' % (name_provider, strftime("%H:%M:%S", gmtime(every))))
            update_service()
        sleep(500)
