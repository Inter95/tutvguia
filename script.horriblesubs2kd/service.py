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
    # get the list
    try:
        with open(path + 'HorribleSubs2PULSAR.txt', "r") as text_file:  # create .strm
            List_shows = [line.strip() for line in text_file]
            text_file.close()
    except:
        #convert from the old version
        database = shelve.open(path + 'HorribleSubs2PULSAR.db')
        List_shows = []
        if database.has_key('list'):
            List_shows = database['list']
        else:
            List_shows = []

    # this read the settings
    settings = tools.Settings(anime=True)
    # define the browser
    browser = tools.Browser()

    # Begin Service
    if settings.service == 'true':
        List_name = []
        if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Checking Online...', settings.icon, settings.time_noti)
        if len(List_shows) > 0:
            quality_keys = settings.settings.getSetting('quality').split(":")
            magnet_list = []
            file_list = []
            url_search = '%s/lib/latest.php' % settings.url_address
            settings.log('[%s]%s' % (settings.name_provider_clean, url_search))
            if browser.open(url_search):
                data = browser.content
                zip_list = zip(re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data), re.findall('<i>(.*?)<', data))
                for quality in quality_keys:
                    for (magnet, name_file) in zip_list:
                        for show in List_shows:
                            if show.lower() in name_file.lower() and quality.lower() in name_file.lower():
                                name_file = name_file.replace('_', ' ')
                                magnet_list.append(magnet)
                                pos = name_file.rfind('- ')
                                name_file = name_file[:pos] + 'EP' + name_file[pos + 2:]  # insert EP to be identificated in kodi
                                file_list.append(name_file)
                tools.integration(filename=file_list, magnet=magnet_list, type_list='SHOW', silence=True,
                                        folder=settings.show_folder, name_provider=settings.name_provider)
            else:
                settings.log('[%s]>>>>>>>%s<<<<<<<' % (settings.name_provider_clean, browser.status))
                settings.dialog.notification(settings.name_provider, browser.status, settings.icon, 1000)
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
