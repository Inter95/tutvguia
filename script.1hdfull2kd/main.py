# coding: utf-8
from urllib import quote_plus

from xbmc import sleep
from hdfulltv import *

######################################
#############  MAIN MENU  ############
######################################
option_list = ['Busqueda Manual', '[COLOR FF2107a2]Películas[/COLOR] Estreno',
               '[COLOR FF2107a2]Películas[/COLOR] Actualizadas', 'Todas las [COLOR FF2107a2]Películas[/COLOR]',
               '[COLOR FF2107a2]Películas[/COLOR] por categoría', 'Borrar una [COLOR FF2107a2]Película[/COLOR]',
               # 'Últimos [COLOR FF07a221]Episodios[/COLOR]',
               # '[COLOR FF07a221]Episodios[/COLOR] Estreno', '[COLOR FF07a221]Episodios[/COLOR] Actualizados',
               'Todas las [COLOR FF07a221]Series[/COLOR]',
               '[COLOR FF07a221]Series[/COLOR] por categoría', 'Borrar una [COLOR FF07a221]Serie[/COLOR]']
option_list.extend(['-CONFIGURACIÓN', '-AYUDA', 'Salir'])

ret = 0
while ret < len(option_list) - 1:
    ret = settings.dialog.select('Opción:', option_list)
    if ret == 0:  # Busqueda Manual
        search = settings.dialog.input('Palabras clave a buscar:')
        if search is not '':
            urlSearch = '%s/ajax/search.php?q=%s' % (settings.value["urlAddress"], quote_plus(search))
            settings.log(message=urlSearch)
            settings.notification(message="Buscando en línea...")
            response = browser.get(urlSearch)
            if response.status_code == requests.codes.ok:
                data = response.json()
                titles = []
                urlList = []
                meta = []
                for item in data:
                    titles.append(item['title'])
                    urlList.append(item['permalink'])
                    meta.append(item['meta'])
                rep = settings.dialog.select('Seleccionar tu opción:', titles + ['CANCEL'])
                if rep < len(titles):
                    if 'Movie' in meta[rep]:
                        title = urlList[rep][urlList[rep].rfind("/") + 1:]  # get the original name
                        int_pelisalacarta(channel="hdfull", titles=[title], url=[urlList[rep]],
                                          typeList='MOVIE', folder=settings.movieFolder)
                    else:
                        show = Shows()
                        show.searchSerie(urlList[rep])
                        storage.add(urlList[rep][urlList[rep].rfind("/") + 1:])
                        int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.urlList,
                                          typeList='SHOW', folder=settings.showFolder)
            else:
                settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
                settings.notification(message="HTTP %s" % response.code, force=True)

    elif ret == 1:  # Peliculas estreno
        movie = Movies()
        urlSearch = "%s/peliculas-estreno" % settings.value["urlAddress"]
        optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
                                            nolabel="Todas")
        movie.searchMovie(urlSearch=urlSearch)

        if optionUnica:
            rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
            if rep < len(movie.titles):
                int_pelisalacarta(channel="hdfull", titles=[movie.titles[rep]], url=[movie.urlList[rep]],
                                  typeList='MOVIE', folder=settings.movieFolder)
        else:
            if len(movie.titles) > 0:
                int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.urlList, typeList='MOVIE',
                                  folder=settings.movieFolder)

    elif ret == 2:  # Peliculas actualizadas
        movie = Movies()
        urlSearch = "%s/peliculas-actualizadas" % settings.value["urlAddress"]

        optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
                                            nolabel="Todas")
        movie.searchMovie(urlSearch=urlSearch)

        if optionUnica:
            rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
            if rep < len(movie.titles):
                int_pelisalacarta(channel="hdfull", titles=[movie.titles[rep]], url=[movie.urlList[rep]],
                                  typeList='MOVIE', folder=settings.movieFolder)
        else:
            if len(movie.titles) > 0:
                int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.urlList, typeList='MOVIE',
                                  folder=settings.movieFolder)

    elif ret == 3:  # Todas las peliculas
        movie = Movies()
        settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
        if settings.pages == '' or settings.pages == 0:
            settings.pages = "1"
        settings.pages = int(settings.pages)

        optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
                                            nolabel="Todas")
        for page in range(1, settings.pages + 1):
            urlSearch = "%s/peliculas/date/%s" % (settings.value["urlAddress"], page)
            movie.searchMovie(urlSearch=urlSearch)
            if page % 5 == 0: sleep(1)

        if optionUnica:
            rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
            if rep < len(movie.titles):
                int_pelisalacarta(channel="hdfull", titles=[movie.titles[rep]], url=[movie.urlList[rep]],
                                  typeList='MOVIE', folder=settings.movieFolder)
        else:
            if len(movie.titles) > 0:
                int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.urlList, typeList='MOVIE',
                                  folder=settings.movieFolder)

    elif ret == 4:  # Peliculas por categoria
        list_categories = {"Acción": "action",
                           "Animación": "animation",
                           "Aventura": "adventure",
                           "Biografía": "biography",
                           "Bélico": "war",
                           "Ciencia Ficción": "science-fiction",
                           "Comedia": "comedy",
                           "Crimen": "crime",
                           "Deportes": "sport",
                           "Documental": "documentary",
                           "Drama": "drama",
                           "Familia": "family",
                           "Fantasía": "fantasy",
                           "Film-Noir": "film-noir",
                           "Historia": "history",
                           "indie": "Indie",
                           "Misterio": "mystery",
                           "Musical": "musical",
                           "Romance": "romance",
                           "Sci-Fi": "sci-fi",
                           "Suspenso": "thriller",
                           "Terror": "horror",
                           "Western": "western"}
        rep = settings.dialog.select('Categoria:', list_categories.keys())
        category = list_categories[list_categories.keys()[rep]]

        rep = settings.dialog.select('Ordenadas por:', ['Fecha', 'Rating IMDB'])
        sortBy = ['date', 'imdb_rating'][rep]

        movie = Movies()
        settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
        if settings.pages == '' or settings.pages == 0:
            settings.pages = "1"
        settings.pages = int(settings.pages)

        optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
                                            nolabel="Todas")
        for page in range(1, settings.pages + 1):
            urlSearch = "%s/tags-peliculas/%s/%s/%s" % (settings.value["urlAddress"], category, sortBy, page)
            movie.searchMovie(urlSearch=urlSearch)
            if page % 5 == 0: sleep(1)

        if optionUnica:
            rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
            if rep < len(movie.titles):
                int_pelisalacarta(channel="hdfull", titles=[movie.titles[rep]], url=[movie.urlList[rep]],
                                  typeList='MOVIE', folder=settings.movieFolder)
        else:
            if len(movie.titles) > 0:
                int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.urlList, typeList='MOVIE',
                                  folder=settings.movieFolder)
    elif ret == 5:  # Borrar una Película
        from os import listdir
        from xbmc import translatePath

        folder = settings.movieFolder
        folder = folder.replace('special://temp/', translatePath('special://temp'))
        folder = folder.replace('smb:', '')  # network compatibility
        listMovies = listdir(folder)
        rep = settings.dialog.select('Seleccionar la película a borrar:', listMovies + ['-CANCELAR'])
        if rep < len(listMovies):
            if settings.dialog.yesno("Atención!", "Desea borrar los archivos strm?", nolabel="No", yeslabel="Si"):
                __removeDirectory__(folder=settings.movieFolder, title=listMovies[rep])

    elif ret == 6:  # Todas las series
        show = Shows()
        settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
        if settings.pages == '' or settings.pages == 0:
            settings.pages = "1"
        settings.pages = int(settings.pages)
        optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
                                            nolabel="Todas")
        titles = []
        urlList = []
        list_item = []
        for page in range(1, settings.pages + 1):
            urlSearch = "%s/series/date/%s" % (settings.value["urlAddress"], page)
            settings.log(message=urlSearch)
            response = browser.get(urlSearch)
            if response.status_code == requests.codes.ok:
                info = re.findall('<a class="link" href="%s/serie/(.*?)" title="(.*?)"' % settings.value["urlAddress"],
                                  response.text)
                for itemdata in info:
                    if optionUnica:  # one selection
                        titles.append(formatTitle(itemdata[0])['title'])
                        urlList.append(settings.value["urlAddress"] + '/serie/' + itemdata[0])
                        list_item.append(itemdata[0])
                    else:  # all series available
                        url_serie = settings.value["urlAddress"] + '/serie/' + itemdata[0]
                        show.searchSerie(url_serie)
                        storage.add(itemdata[0])
            else:
                settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
                settings.notification(message="HTTP %s" % response.code, force=True)
            if page % 5 == 0: sleep(1)

        if optionUnica:
            rep = settings.dialog.select('Seleccionar tu opción:', titles + ['-CANCELAR'])
            if rep < len(titles):
                show = Shows()
                show.searchSerie(urlList[rep])
                storage.add(list_item[rep])

        if len(show.titles) > 0:
            int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.urlList, typeList='SHOW',
                              folder=settings.showFolder)
    elif ret == 7:  # Series por categoria
        list_categories = {"Acción": "action",
                           "Animación": "animation",
                           "Anime": "anime",
                           "Aventura": "adventure",
                           "Ciencia Ficción": "science-fiction",
                           "Comedia": "comedy",
                           "Crimen": "crime",
                           "Deportes": "sport",
                           "Documental": "documentary",
                           "Drama": "drama",
                           "Fantasía": "fantasy",
                           "Infantil": "children",
                           "Miniseries": "miniserie",
                           "Misterio": "mistery",
                           "Noticias": "news",
                           "Novela": "soap",
                           "Reality Show": "reality",
                           "Talk Show": "talk-show",
                           "Western": "western"}
        rep = settings.dialog.select('Categoria:', list_categories.keys())
        category = list_categories[list_categories.keys()[rep]]

        rep = settings.dialog.select('Ordenadas por:', ['Fecha', 'Rating IMDB'])
        sortBy = ['date', 'imdb_rating'][rep]

        show = Shows()
        settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
        if settings.pages == '' or settings.pages == 0:
            settings.pages = "1"
        settings.pages = int(settings.pages)
        optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
                                            nolabel="Todas")
        titles = []
        urlList = []
        list_item = []
        for page in range(1, settings.pages + 1):
            urlSearch = "%s/tags-tv/%s/%s/%s" % (settings.value["urlAddress"], category, sortBy, page)
            settings.log(message=urlSearch)
            response = browser.get(urlSearch)
            if response.status_code == requests.codes.ok:
                info = re.findall('<a class="link" href="%s/serie/(.*?)" title="(.*?)"' % settings.value["urlAddress"],
                                  response.text)
                for itemdata in info:
                    if optionUnica:  # one selection
                        titles.append(formatTitle(itemdata[0])['title'])
                        urlList.append(settings.value["urlAddress"] + '/serie/' + itemdata[0])
                        list_item.append(itemdata[0])
                    else:  # all series available
                        url_serie = settings.value["urlAddress"] + '/serie/' + itemdata[0]
                        show.searchSerie(url_serie)
                        storage.add(itemdata[0])
            else:
                settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
                settings.notification(message="HTTP %s" % response.code, force=True)
            if page % 5 == 0: sleep(1)

        if optionUnica:
            rep = settings.dialog.select('Seleccionar tu opción:', titles + ['-CANCELAR'])
            if rep < len(titles):
                show = Shows()
                show.searchSerie(urlList[rep])
                storage.add(list_item[rep])

        if len(show.titles) > 0:
            int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.urlList, typeList='SHOW',
                              folder=settings.showFolder)

    elif ret == 8:  # Borrar una serie
        rep = settings.dialog.select('Seleccionar la serie a borrar:', storage.database + ['-CANCELAR'])
        if rep < len(storage.database):
            if settings.dialog.yesno("Atención!", "Desea borrar los archivos strm también?", nolabel="No",
                                     yeslabel="Si"):
                __removeDirectory__(folder=settings.showFolder, title=storage.database[rep])
            storage.remove(storage.database[rep])

    # common menu
    elif ret == len(option_list) - 3:  # Settings
        settings.settings.openSettings()
        settings = Settings()

    elif ret == len(option_list) - 2:  # Help
        settings.dialog.ok("Ayuda",
                           "El manual de operacion se encuentra en esta dirección:\n[B]http://goo.gl/0b44BY[/B]")


# save the database
storage.save()

del storage
del settings
del browser


# elif ret == 5:  # Ultimos Episodios
#     show = Shows()
#     urlSearch = "%s/a/episodes" % settings.value["urlAddress"]
#     show.searchEpisode(url_episode=urlSearch, action="latest")
#     if len(show.titles) > 0:
#         int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.urlList, typeList='SHOW',
#                                 folder=settings.showFolder)
#
# elif ret == 6:  # Episodios Estreno
#     show = Shows()
#     urlSearch = "%s/a/episodes" % settings.value["urlAddress"]
#     show.searchEpisode(url_episode=urlSearch, action="premiere")
#     if len(show.titles) > 0:
#         int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.urlList, typeList='SHOW',
#                                 folder=settings.showFolder)
#
# elif ret == 7:  # Episodios Actualizados
#     show = Shows()
#     urlSearch = "%s/a/episodes" % settings.value["urlAddress"]
#     show.searchEpisode(url_episode=urlSearch, action="updated")
#     if len(show.titles) > 0:
#         int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.urlList, typeList='SHOW',
#                                 folder=settings.showFolder)
