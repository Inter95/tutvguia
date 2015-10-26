# coding: utf-8
from time import time
from time import asctime
from time import localtime
from time import strftime
from time import gmtime

from peliculasaudiolatino import *
from xbmc import log
from xbmc import sleep
from xbmc import abortRequested
from xbmcaddon import Addon


def update_service():
    settings = tools.Settings()
    # if settings.service == 'true':
        # Begin Service
        #update series
        # for item in storage.database:
        #     show = Shows()
        #     show.searchSerie(settings.url_address + '/serie/' + item)
        #     tools.int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.url_list,
        #                             type_list='SHOW',
        #                             folder=settings.show_folder, name_provider=settings.name_provider, silence=True)
        # #rest of the options
        # if Addon().getSetting('peliculasEstreno') == "true":  # Peliculas estreno
        #
        #     movie = Movies()
        #     url_search = "%s/peliculas-estreno" % settings.url_address
        #     movie.searchMovie(url_search=url_search)
        #     if len(movie.titles) > 0:
        #         tools.int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.url_list, type_list='MOVIE',
        #                                 folder=settings.movie_folder, name_provider=settings.name_provider,
        #                                 silence="true")
        #
        # elif Addon().getSetting('peliculasActualizadas') == "true":  # Peliculas actualizadas
        #     movie = Movies()
        #     url_search = "%s/peliculas-actualizadas" % settings.url_address
        #     movie.searchMovie(url_search=url_search)
        #     if len(movie.titles) > 0:
        #         tools.int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.url_list, type_list='MOVIE',
        #                                 folder=settings.movie_folder, name_provider=settings.name_provider,
        #                                 silence="true")
        #
        # elif Addon().getSetting('todasPeliculas') == 'true':  # Todas las peliculas
        #     movie = Movies()
        #     if settings.pages == '' or settings.pages == 0:
        #         settings.pages = "1"
        #     settings.pages = int(settings.pages)
        #     for page in range(1, settings.pages + 1):
        #         url_search = "%s/peliculas/date/%s" % (settings.url_address, page)
        #         movie.searchMovie(url_search=url_search)
        #         if page % 5 == 0: sleep(1)
        #     if len(movie.titles) > 0:
        #         tools.int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.url_list, type_list='MOVIE',
        #                                 folder=settings.movie_folder, name_provider=settings.name_provider,
        #                                 silence="true")
        #
        # elif Addon().getSetting('episodioEstreno') == 'true':  # Ultimos Episodios
        #     show = Shows()
        #     url_search = "%s/a/episodes" % settings.url_address
        #     show.searchEpisode(url_episode=url_search, action="latest")
        #     if len(show.titles) > 0:
        #         tools.int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.url_list, type_list='SHOW',
        #                                 folder=settings.show_folder, name_provider=settings.name_provider,
        #                                 silence="true")
        #
        #
        # elif Addon().getSetting('premiereEpisodio') == 'true':  # Episodios Estreno
        #     show = Shows()
        #     url_search = "%s/a/episodes" % settings.url_address
        #     show.searchEpisode(url_episode=url_search, action="premiere")
        #     if len(show.titles) > 0:
        #         tools.int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.url_list, type_list='SHOW',
        #                                 folder=settings.show_folder, name_provider=settings.name_provider,
        #                                 silence="true")
        #
        #
        # elif Addon().getSetting('actualizadosEpisodes') == 'true':  # Episodios Actualizados
        #     show = Shows()
        #     url_search = "%s/a/episodes" % settings.url_address
        #     show.searchEpisode(url_episode=url_search, action="updated")
        #     if len(show.titles) > 0:
        #         tools.int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.url_list, type_list='SHOW',
        #                                 folder=settings.show_folder, name_provider=settings.name_provider,
        #                                 silence="true")

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
