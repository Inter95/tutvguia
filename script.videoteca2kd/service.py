# coding: utf-8
from time import time
from time import asctime
from time import localtime
from time import strftime
from time import gmtime

from videoteca import *
from xbmc import log
from xbmc import sleep
from xbmc import abortRequested
from xbmcaddon import Addon
import re


def update_service():
    settings = tools.Settings()
    if settings.service == 'true':
        # Begin Service
        if Addon().getSetting('peliculas') == "true":  # Peliculas Audio Latino #1
            menu = Menu(type="movie", url="URL/es/peliculas/page/PAGE", channel="yaske")
            menu.play(silence=True)
        if Addon().getSetting('series') == "true":  #series
            show=Shows()
            for cm, url in enumerate(storage.database.values()):
                show.searchEpisodes(urlSearch=url, exclude="Animes", erase=False)
            tools.int_pelisalacarta(channel="seriesflv", titles=show.titles, url=show.url_list,
                                    type_list='SHOW', folder=settings.show_folder,
                                    name_provider=settings.name_provider, silence=True)
        if Addon().getSetting('animes') == "true":  #anime
            show=Shows()
            for url in storageAnime.database.values():
                show.searchEpisodes(urlSearch=url, erase=False)
            for cm, title in enumerate(show.titles):  # convertir in EP00 format
                pos = title.rfind(' ')
                show.titles[cm] = title[:pos] + ' EP' + title[pos + 1:]
            tools.int_pelisalacarta(channel="seriesflv", titles=show.titles, url=show.url_list,
                                    type_list='SHOW', folder=settings.anime_folder,
                                    name_provider=settings.name_provider, silence=True)

    del settings


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
