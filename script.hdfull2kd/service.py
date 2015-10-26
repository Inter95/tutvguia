# coding: utf-8
from time import time
from time import asctime
from time import localtime
from time import strftime
from time import gmtime

from hdfulltv import *
from xbmc import log
from xbmc import sleep
from xbmc import abortRequested
from xbmcaddon import Addon


def update_service():
    settings = Settings()
    if settings.value["service"] == 'true':
        # Begin Service
        if Addon().getSetting('series') == "true":  # Peliculas estreno
            # update series
            for item in storage.database:
                show = Shows()
                goodSpider()
                show.searchSerie(settings.value["urlAddress"] + '/serie/' + item)
                int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.urlList,
                                  typeList='SHOW', folder=settings.showFolder, silence=True)
        # rest of the options
        if Addon().getSetting('peliculasEstreno') == "true":  # Peliculas estreno
            movie = Movies()
            urlSearch = "%s/peliculas-estreno" % settings.value["urlAddress"]
            movie.searchMovie(urlSearch=urlSearch)
            if len(movie.titles) > 0:
                int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.urlList, typeList='MOVIE',
                                  folder=settings.movieFolder, silence="true")

        elif Addon().getSetting('peliculasActualizadas') == "true":  # Peliculas actualizadas
            movie = Movies()
            urlSearch = "%s/peliculas-actualizadas" % settings.value["urlAddress"]
            movie.searchMovie(urlSearch=urlSearch)
            if len(movie.titles) > 0:
                int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.urlList, typeList='MOVIE',
                                  folder=settings.movieFolder, silence="true")

        elif Addon().getSetting('todasPeliculas') == 'true':  # Todas las peliculas
            movie = Movies()
            if settings.value["pages"] == '' or settings.value["pages"] == 0:
                settings.value["pages"] = "1"
            settings.value["pages"] = int(settings.value["pages"])
            for page in range(1, settings.value["pages"] + 1):
                urlSearch = "%s/peliculas/date/%s" % (settings.value["urlAddress"], page)
                movie.searchMovie(urlSearch=urlSearch)
                goodSpider()
            if len(movie.titles) > 0:
                int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.urlList, typeList='MOVIE',
                                  folder=settings.movieFolder, silence="true")

        elif Addon().getSetting('episodioEstreno') == 'true':  # Ultimos Episodios
            show = Shows()
            urlSearch = "%s/a/episodes" % settings.value["urlAddress"]
            show.searchEpisode(urlEpisode=urlSearch, action="latest")
            if len(show.titles) > 0:
                int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.urlList, typeList='SHOW',
                                  folder=settings.showFolder, silence="true")

        elif Addon().getSetting('premiereEpisodio') == 'true':  # Episodios Estreno
            show = Shows()
            urlSearch = "%s/a/episodes" % settings.value["urlAddress"]
            show.searchEpisode(urlEpisode=urlSearch, action="premiere")
            if len(show.titles) > 0:
                int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.urlList, typeList='SHOW',
                                  folder=settings.showFolder, silence="true")

        elif Addon().getSetting('actualizadosEpisodes') == 'true':  # Episodios Actualizados
            show = Shows()
            urlSearch = "%s/a/episodes" % settings.value["urlAddress"]
            show.searchEpisode(urlEpisode=urlSearch, action="updated")
            if len(show.titles) > 0:
                int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.urlList, typeList='SHOW',
                                  folder=settings.showFolder, silence="true")


if Addon().getSetting('service') == 'true':
    persistent = Addon().getSetting('persistent')
    nameProvider = re.sub('.COLOR (.*?)]', '', Addon().getAddonInfo('name').replace('[/COLOR]', ''))
    every = 28800  # seconds
    previous_time = time()
    log("[%s]Update Service starting..." % nameProvider)
    update_service()
    while (not abortRequested) and persistent == 'true':
        if time() >= previous_time + every:  # verification
            previous_time = time()
            update_service()
            settings.log('Update List at %s' % (asctime(localtime(previous_time))))
            settings.log('Next Update in %s' % (strftime("%H:%M:%S", gmtime(every))))
            update_service()
        sleep(500)
