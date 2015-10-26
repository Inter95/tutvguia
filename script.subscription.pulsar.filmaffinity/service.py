# coding: utf-8
import re
import subscription
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

    url_search = "http://www.filmaffinity.com/en/topcat_DVD_VID_US.html"
    listing = []
    ID = []  # IMDB_ID or thetvdb ID
    if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Checking Online...', settings.icon,
                                                            settings.time_noti)
    settings.log('[%s]%s' % (settings.name_provider_clean, url_search))
    if browser.open(url_search):
        data = browser.content.replace('</a>', '')
        listing = [item[1] for item in re.findall('<div class="mc-title">(.*?)>(.*?)<', data)]
        subscription.integration(listing, ID, 'MOVIE', settings.movie_folder, silence=True, name_provider=settings.name_provider)
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
