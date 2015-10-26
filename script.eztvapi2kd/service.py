# coding: utf-8
import re
import tools
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
    path = translatePath('special://temp')
    # get the Dictionary
    Dict_tvshows = {}
    try:
        with open(path + 'EZTVapi2KD.txt', 'r') as fp:
            for line in fp:
                listedline = line.strip().split('::')  # split around the :: sign
                if len(listedline) > 1:  # we have the : sign in there
                    Dict_tvshows[listedline[0]] = listedline[1]
    except:
        pass

    # this read the settings
    settings = tools.Settings()
    # define the browser
    browser = tools.Browser()

    # Begin Service
    if settings.service == 'true':
        if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Checking Online...', settings.icon, settings.time_noti)
        if len(Dict_tvshows.keys()) > 0:
            quality_keys = settings.settings.getSetting('quality').lower().split(":")
            magnet_list = []
            file_list = []
            title_list = []
            for (show, value) in Dict_tvshows.items():
                if settings.time_noti > 0: settings.dialog.notification(settings.name_provider,
                                            'Checking Online for %s...' % show, settings.icon, settings.time_noti)
                url_search = '%s/show/%s' % (settings.url_address, value)  # search for the tvshow
                settings.log('[%s]%s' % (settings.name_provider_clean, url_search))
                browser.open(url_search)
                data = browser.content
                magnets = re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)
                for quality in quality_keys:
                    for magnet in magnets:
                        name_file = magnet.lower() + ' hdtv'  # take any file as hdtv by default
                        if quality == 'hdtv' and ('720p' in name_file or '1080p' in name_file):
                            name_file = name_file.replace('hdtv', '')
                        if quality in name_file:
                            magnet_list.append(magnet)
                            title = magnet[magnet.find('&dn=') + 4:] + '&'  # find the start of the name
                            title = title[:title.find('&')]
                            file_list.append(title)
                            title_list.append(show)
            if len(file_list) > 0:
                tools.integration(title=title_list, filename=file_list, magnet=magnet_list, type_list='SHOW',
                              folder=settings.show_folder, name_provider=settings.name_provider, silence=True)
        else:
            if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Empty List', settings.icon, settings.time_noti)
    del settings
    del browser


if Addon().getSetting('service') == 'true':
    persistent = Addon().getSetting('persistent')
    name_provider = re.sub('.COLOR (.*?)]', '', Addon().getAddonInfo('name').replace('[/COLOR]', ''))
    every = 28800  # seconds
    previous_time = time()
    log("[%s] Update Service starting..." % name_provider)
    update_service()
    while (not abortRequested) and persistent == 'true':
        if time() >= previous_time + every:  # verification
            previous_time = time()
            update_service()
            log('[%s] Update List at %s' % (name_provider, asctime(localtime(previous_time))))
            log('[%s] Next Update in %s' % (name_provider, strftime("%H:%M:%S", gmtime(every))))
            update_service()
        sleep(500)
