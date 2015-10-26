# coding: utf-8

from xbmc import sleep
from peliculasaudiolatino import *

######################################
#############  MAIN MENU  ############
######################################
option_list = ['Busqueda Manual',  #0
               '[COLOR FF2107a2]Películas[/COLOR] Estreno',  #1
               '[COLOR FF2107a2]Películas[/COLOR] Últimas Agregadas',  #2
               '[COLOR FF2107a2]Películas[/COLOR] Recien Actualizadas',  # 3
               '[COLOR FF2107a2]Películas[/COLOR] Las Más Vistas',  # 4
               '[COLOR FF2107a2]Películas[/COLOR] por Años',  # 5
               '[COLOR FF2107a2]Películas[/COLOR] por Géneros',  # 6
               'Todas las [COLOR FF2107a2]Películas[/COLOR]',  #7
               'Borrar una [COLOR FF2107a2]Película[/COLOR]',  #8
               'Todas las [COLOR FF07a221]Series[/COLOR]',  #9
               'Borrar una [COLOR FF07a221]Serie[/COLOR]']  #10
option_list.extend(['-CONFIGURACIÓN', '-AYUDA', 'Salir'])

ret = 0
while ret < len(option_list) - 1:
    ret = settings.dialog.select('Opción:', option_list)
    if ret == 0:  # Busqueda Manual
        search = settings.dialog.input('Palabras clave a buscar:')
        # if search is not '':
        #     url_search = '%s/ajax/search.php?q=%s' % (settings.url_address, quote_plus(search))
        #     settings.log(message=url_search)
        #     settings.notification(message="Buscando en línea...")
        #     response = browser.open(url_search)
        #     if response.code == 200:
        #         data = json.loads(response.read())
        #         titles = []
        #         url_list = []
        #         meta = []
        #         for item in data:
        #             titles.append(item['title'])
        #             url_list.append(item['permalink'])
        #             meta.append(item['meta'])
        #         rep = settings.dialog.select('Seleccionar tu opción:', titles + ['CANCEL'])
        #         if rep < len(titles):
        #             if 'Movie' in meta[rep]:
        #                 title = url_list[rep][url_list[rep].rfind("/") + 1:]  # get the original name
        #                 tools.int_pelisalacarta(channel="hdfull", titles=[title], url=[url_list[rep]],
        #                                         type_list='MOVIE', folder=settings.movie_folder,
        #                                         name_provider=settings.name_provider)
        #             else:
        #                 show = Shows()
        #                 show.searchSerie(url_list[rep])
        #                 storage.add(url_list[rep][url_list[rep].rfind("/") + 1:])
        #                 tools.int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.url_list,
        #                                         type_list='SHOW',
        #                                         folder=settings.show_folder, name_provider=settings.name_provider)
        #     else:
        #         settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
        #         settings.notification(message="HTTP %s" % response.code, force=True)
    elif ret == 1:  # Peliculas Estreno
        movie = Movies()
        settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
        if settings.pages == '' or settings.pages == 0:
            settings.pages = "1"
        settings.pages = int(settings.pages)

        optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
                                            nolabel="Todas")
        for page in range(1, settings.pages + 1):
            url_search = "%s/estrenos-2015/pagina/%s.html" % (settings.url_address, page)
            movie.searchMovie(url_search=url_search)
            if page % 5 == 0: sleep(1)

        if optionUnica:
            rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
            if rep < len(movie.titles):
                tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=[movie.titles[rep]], url=[movie.url_list[rep]],
                                        type_list='MOVIE', folder=settings.movie_folder,
                                        name_provider=settings.name_provider)
        else:
            if len(movie.titles) > 0:
                tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=movie.titles, url=movie.url_list, type_list='MOVIE',
                                        folder=settings.movie_folder, name_provider=settings.name_provider)
    elif ret == 2:  # Últimas Agregadas',  #2
        movie = Movies()
        settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
        if settings.pages == '' or settings.pages == 0:
            settings.pages = "1"
        settings.pages = int(settings.pages)

        optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
                                            nolabel="Todas")
        for page in range(1, settings.pages + 1):
            url_search = "%s/ultimas-agregadas/pagina/%s.html" % (settings.url_address, page)
            movie.searchMovie(url_search=url_search)
            if page % 5 == 0: sleep(1)

        if optionUnica:
            rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
            if rep < len(movie.titles):
                tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=[movie.titles[rep]], url=[movie.url_list[rep]],
                                        type_list='MOVIE', folder=settings.movie_folder,
                                        name_provider=settings.name_provider)
        else:
            if len(movie.titles) > 0:
                tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=movie.titles, url=movie.url_list,
                                        type_list='MOVIE',
                                        folder=settings.movie_folder, name_provider=settings.name_provider)

    elif ret == 3:  # Recien Actualizadas',  # 3
        movie = Movies()
        settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
        if settings.pages == '' or settings.pages == 0:
            settings.pages = "1"
        settings.pages = int(settings.pages)

        optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
                                            nolabel="Todas")
        for page in range(1, settings.pages + 1):
            url_search = "%s/recien-actualizadas/pagina/%s.html" % (settings.url_address, page)
            movie.searchMovie(url_search=url_search)
            if page % 5 == 0: sleep(1)

        if optionUnica:
            rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
            if rep < len(movie.titles):
                tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=[movie.titles[rep]], url=[movie.url_list[rep]],
                                        type_list='MOVIE', folder=settings.movie_folder,
                                        name_provider=settings.name_provider)
        else:
            if len(movie.titles) > 0:
                tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=movie.titles, url=movie.url_list,
                                        type_list='MOVIE',
                                        folder=settings.movie_folder, name_provider=settings.name_provider)

    elif ret == 4:  # Las Más Vistas',  # 4
        movie = Movies()
        settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
        if settings.pages == '' or settings.pages == 0:
            settings.pages = "1"
        settings.pages = int(settings.pages)

        optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
                                            nolabel="Todas")
        for page in range(1, settings.pages + 1):
            url_search = "%s/las-mas-vistas/pagina/%s.html" % (settings.url_address, page)
            movie.searchMovie(url_search=url_search)
            if page % 5 == 0: sleep(1)

        if optionUnica:
            rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
            if rep < len(movie.titles):
                tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=[movie.titles[rep]],
                                        url=[movie.url_list[rep]],
                                        type_list='MOVIE', folder=settings.movie_folder,
                                        name_provider=settings.name_provider)
        else:
            if len(movie.titles) > 0:
                tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=movie.titles, url=movie.url_list,
                                        type_list='MOVIE',
                                        folder=settings.movie_folder, name_provider=settings.name_provider)
    elif ret == 5:  # Peliculas por Años
        response = browser.open(settings.url_address)  # getting years
        if response.code == 200:
            scraper.html = response.read().replace('<span class="icon-dot-single"></span>', '')
            scraper.find('ul class="children"', order=2)
            list_categories = dict(zip(scraper.aTexts, scraper.aHrefs))
            rep = settings.dialog.select('Categoria:', list_categories.keys())
            category = list_categories[list_categories.keys()[rep]]

            movie = Movies()
            settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
            if settings.pages == '' or settings.pages == 0:
                settings.pages = "1"
            settings.pages = int(settings.pages)

            optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección",
                                                yeslabel="Individual",
                                                nolabel="Todas")
            for page in range(1, settings.pages + 1):
                url_search = ("%s%s" % (settings.url_address, category)).replace(".html", "/pagina/%s.html" % page )
                movie.searchMovie(url_search=url_search)
                if page % 5 == 0: sleep(1)

            if optionUnica:
                rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
                if rep < len(movie.titles):
                    tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=[movie.titles[rep]],
                                            url=[movie.url_list[rep]],
                                            type_list='MOVIE', folder=settings.movie_folder,
                                            name_provider=settings.name_provider)
            else:
                if len(movie.titles) > 0:
                    tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=movie.titles, url=movie.url_list,
                                            type_list='MOVIE',
                                            folder=settings.movie_folder,
                                            name_provider=settings.name_provider)
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
            settings.notification(message="HTTP %s" % response.code, force=True)

    elif ret == 6:  # Peliculas por categoria
        response = browser.open(settings.url_address)  #getting the genres
        if response.code == 200:
            scraper.html=response.read().replace('<span class="icon-dot-single"></span>', '')
            scraper.find('ul class="children"', order=1)
            list_categories = dict(zip(scraper.aTexts, scraper.aHrefs))
            rep = settings.dialog.select('Categoria:', list_categories.keys())
            category = list_categories[list_categories.keys()[rep]]

            movie = Movies()
            settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
            if settings.pages == '' or settings.pages == 0:
                settings.pages = "1"
            settings.pages = int(settings.pages)

            optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección",
                                                yeslabel="Individual",
                                                nolabel="Todas")
            for page in range(1, settings.pages + 1):
                url_search = ("%s%s" % (settings.url_address, category)).replace(".html", "/pagina/%s.html" % page)
                movie.searchMovie(url_search=url_search)
                if page % 5 == 0: sleep(1)

            if optionUnica:
                rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
                if rep < len(movie.titles):
                    tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=[movie.titles[rep]],
                                            url=[movie.url_list[rep]],
                                            type_list='MOVIE', folder=settings.movie_folder,
                                            name_provider=settings.name_provider)
            else:
                if len(movie.titles) > 0:
                    tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=movie.titles, url=movie.url_list,
                                            type_list='MOVIE',
                                            folder=settings.movie_folder,
            name_provider=settings.name_provider)
        else:
            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
            settings.notification(message="HTTP %s" % response.code, force=True)

    elif ret == 7:  # Todas Las películas',  # 7
        movie = Movies()
        settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
        if settings.pages == '' or settings.pages == 0:
            settings.pages = "1"
        settings.pages = int(settings.pages)

        optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
                                            nolabel="Todas")
        for page in range(1, settings.pages + 1):
            url_search = "%s/lista-completa/pagina/%s.html" % (settings.url_address, page)
            movie.searchMovie(url_search=url_search)
            if page % 5 == 0: sleep(1)

        if optionUnica:
            rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
            if rep < len(movie.titles):
                tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=[movie.titles[rep]],
                                        url=[movie.url_list[rep]],
                                        type_list='MOVIE', folder=settings.movie_folder,
                                        name_provider=settings.name_provider)
        else:
            if len(movie.titles) > 0:
                tools.int_pelisalacarta(channel="peliculasaudiolatino", titles=movie.titles, url=movie.url_list,
                                        type_list='MOVIE',
                                        folder=settings.movie_folder, name_provider=settings.name_provider)
    elif ret == 8:  # Borrar una Película
        from os import listdir

        list_movies = listdir(settings.movie_folder)
        rep = settings.dialog.select('Seleccionar la película a borrar:', list_movies + ['-CANCELAR'])
        if rep < len(list_movies):
            if settings.dialog.yesno("Atención!", "Desea borrar los archivos strm?", nolabel="No", yeslabel="Si"):
                tools.removeDirectory(folder=settings.movie_folder, title=list_movies[rep])







    # elif ret == 1:  # Peliculas estreno
    #     movie = Movies()
    #     url_search = "%s/peliculas-estreno" % settings.url_address
    #     optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
    #                                         nolabel="Todas")
    #     movie.searchMovie(url_search=url_search)
    #
    #     if optionUnica:
    #         rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
    #         if rep < len(movie.titles):
    #             tools.int_pelisalacarta(channel="hdfull", titles=[movie.titles[rep]], url=[movie.url_list[rep]],
    #                                     type_list='MOVIE', folder=settings.movie_folder,
    #                                     name_provider=settings.name_provider)
    #     else:
    #         if len(movie.titles) > 0:
    #             tools.int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.url_list, type_list='MOVIE',
    #                                     folder=settings.movie_folder, name_provider=settings.name_provider)
    #
    # elif ret == 2:  # Peliculas actualizadas
    #     movie = Movies()
    #     url_search = "%s/peliculas-actualizadas" % settings.url_address
    #
    #     optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
    #                                         nolabel="Todas")
    #     movie.searchMovie(url_search=url_search)
    #
    #     if optionUnica:
    #         rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
    #         if rep < len(movie.titles):
    #             tools.int_pelisalacarta(channel="hdfull", titles=[movie.titles[rep]], url=[movie.url_list[rep]],
    #                                     type_list='MOVIE', folder=settings.movie_folder,
    #                                     name_provider=settings.name_provider)
    #     else:
    #         if len(movie.titles) > 0:
    #             tools.int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.url_list, type_list='MOVIE',
    #                                     folder=settings.movie_folder, name_provider=settings.name_provider)
    #
    # elif ret == 3:  # Todas las peliculas
    #     movie = Movies()
    #     settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
    #     if settings.pages == '' or settings.pages == 0:
    #         settings.pages = "1"
    #     settings.pages = int(settings.pages)
    #
    #     optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
    #                                         nolabel="Todas")
    #     for page in range(1, settings.pages + 1):
    #         url_search = "%s/peliculas/date/%s" % (settings.url_address, page)
    #         movie.searchMovie(url_search=url_search)
    #         if page % 5 == 0: sleep(1)
    #
    #     if optionUnica:
    #         rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
    #         if rep < len(movie.titles):
    #             tools.int_pelisalacarta(channel="hdfull", titles=[movie.titles[rep]], url=[movie.url_list[rep]],
    #                                     type_list='MOVIE', folder=settings.movie_folder,
    #                                     name_provider=settings.name_provider)
    #     else:
    #         if len(movie.titles) > 0:
    #             tools.int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.url_list, type_list='MOVIE',
    #                                     folder=settings.movie_folder, name_provider=settings.name_provider)
    #
    # elif ret == 4:  # Peliculas por categoria
    #     list_categories = {"Acción": "action",
    #                        "Animación": "animation",
    #                        "Aventura": "adventure",
    #                        "Biografía": "biography",
    #                        "Bélico": "war",
    #                        "Ciencia Ficción": "science-fiction",
    #                        "Comedia": "comedy",
    #                        "Crimen": "crime",
    #                        "Deportes": "sport",
    #                        "Documental": "documentary",
    #                        "Drama": "drama",
    #                        "Familia": "family",
    #                        "Fantasía": "fantasy",
    #                        "Film-Noir": "film-noir",
    #                        "Historia": "history",
    #                        "indie": "Indie",
    #                        "Misterio": "mystery",
    #                        "Musical": "musical",
    #                        "Romance": "romance",
    #                        "Sci-Fi": "sci-fi",
    #                        "Suspenso": "thriller",
    #                        "Terror": "horror",
    #                        "Western": "western"}
    #     rep = settings.dialog.select('Categoria:', list_categories.keys())
    #     category = list_categories[list_categories.keys()[rep]]
    #
    #     rep = settings.dialog.select('Ordenadas por:', ['Fecha', 'Rating IMDB'])
    #     sortBy = ['date', 'imdb_rating'][rep]
    #
    #     movie = Movies()
    #     settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
    #     if settings.pages == '' or settings.pages == 0:
    #         settings.pages = "1"
    #     settings.pages = int(settings.pages)
    #
    #     optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
    #                                         nolabel="Todas")
    #     for page in range(1, settings.pages + 1):
    #         url_search = "%s/tags-peliculas/%s/%s/%s" % (settings.url_address, category, sortBy, page)
    #         movie.searchMovie(url_search=url_search)
    #         if page % 5 == 0: sleep(1)
    #
    #     if optionUnica:
    #         rep = settings.dialog.select('Seleccionar tu opción:', movie.titles + ['CANCEL'])
    #         if rep < len(movie.titles):
    #             tools.int_pelisalacarta(channel="hdfull", titles=[movie.titles[rep]], url=[movie.url_list[rep]],
    #                                     type_list='MOVIE', folder=settings.movie_folder,
    #                                     name_provider=settings.name_provider)
    #     else:
    #         if len(movie.titles) > 0:
    #             tools.int_pelisalacarta(channel="hdfull", titles=movie.titles, url=movie.url_list, type_list='MOVIE',
    #                                     folder=settings.movie_folder, name_provider=settings.name_provider)
    # elif ret == 5:  # Borrar una Película
    #     from os import listdir
    #
    #     list_movies = listdir(settings.movie_folder)
    #     rep = settings.dialog.select('Seleccionar la película a borrar:', list_movies + ['-CANCELAR'])
    #     if rep < len(list_movies):
    #         if settings.dialog.yesno("Atención!", "Desea borrar los archivos strm?", nolabel="No", yeslabel="Si"):
    #             tools.removeDirectory(folder=settings.movie_folder, title=list_movies[rep])
    # elif ret == 6:  # Todas las series
    #     show = Shows()
    #     settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
    #     if settings.pages == '' or settings.pages == 0:
    #         settings.pages = "1"
    #     settings.pages = int(settings.pages)
    #     optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
    #                                         nolabel="Todas")
    #     titles = []
    #     url_list = []
    #     list_item = []
    #     for page in range(1, settings.pages + 1):
    #         url_search = "%s/series/date" % settings.url_address
    #         settings.log(message=url_search)
    #         response = browser.open(url_search)
    #         if response.code == 200:
    #             info = re.findall('<a class="link" href="%s/serie/(.*?)" title="(.*?)"' % settings.url_address,
    #                               response.read())
    #             for itemdata in info:
    #                 if optionUnica:  # one selection
    #                     titles.append(tools.format_title(itemdata[0])['title'])
    #                     url_list.append(settings.url_address + '/serie/' + itemdata[0])
    #                     list_item.append(itemdata[0])
    #                 else:  # all series available
    #                     url_serie = settings.url_address + '/serie/' + itemdata[0]
    #                     show.searchSerie(url_serie)
    #                     storage.add(itemdata[0])
    #         else:
    #             settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
    #             settings.notification(message="HTTP %s" % response.code, force=True)
    #         if page % 5 == 0: sleep(1)
    #
    #     if optionUnica:
    #         rep = settings.dialog.select('Seleccionar tu opción:', titles + ['-CANCELAR'])
    #         if rep < len(titles):
    #             show = Shows()
    #             show.searchSerie(url_list[rep])
    #             storage.add(list_item[rep])
    #
    #     if len(show.titles) > 0:
    #         tools.int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.url_list, type_list='SHOW',
    #                                 folder=settings.show_folder, name_provider=settings.name_provider)
    # elif ret == 7:  # Series por categoria
    #     list_categories = {"Acción": "action",
    #                        "Animación": "animation",
    #                        "Anime": "anime",
    #                        "Aventura": "adventure",
    #                        "Ciencia Ficción": "science-fiction",
    #                        "Comedia": "comedy",
    #                        "Crimen": "crime",
    #                        "Deportes": "sport",
    #                        "Documental": "documentary",
    #                        "Drama": "drama",
    #                        "Fantasía": "fantasy",
    #                        "Infantil": "children",
    #                        "Miniseries": "miniserie",
    #                        "Misterio": "mistery",
    #                        "Noticias": "news",
    #                        "Novela": "soap",
    #                        "Reality Show": "reality",
    #                        "Talk Show": "talk-show",
    #                        "Western": "western"}
    #     rep = settings.dialog.select('Categoria:', list_categories.keys())
    #     category = list_categories[list_categories.keys()[rep]]
    #
    #     rep = settings.dialog.select('Ordenadas por:', ['Fecha', 'Rating IMDB'])
    #     sortBy = ['date', 'imdb_rating'][rep]
    #
    #     show = Shows()
    #     settings.pages = settings.dialog.numeric(0, 'Número de páginas a bajar:')
    #     if settings.pages == '' or settings.pages == 0:
    #         settings.pages = "1"
    #     settings.pages = int(settings.pages)
    #     optionUnica = settings.dialog.yesno("Selección", "Por favor escoga el tipo de selección", yeslabel="Individual",
    #                                         nolabel="Todas")
    #     titles = []
    #     url_list = []
    #     list_item = []
    #     for page in range(1, settings.pages + 1):
    #         url_search = "%s/tags-tv/%s/%s/%s" % (settings.url_address, category, sortBy, page)
    #         settings.log(message=url_search)
    #         response = browser.open(url_search)
    #         if response.code == 200:
    #             info = re.findall('<a class="link" href="%s/serie/(.*?)" title="(.*?)"' % settings.url_address,
    #                               response.read())
    #             for itemdata in info:
    #                 if optionUnica:  # one selection
    #                     titles.append(tools.format_title(itemdata[0])['title'])
    #                     url_list.append(settings.url_address + '/serie/' + itemdata[0])
    #                     list_item.append(itemdata[0])
    #                 else:  # all series available
    #                     url_serie = settings.url_address + '/serie/' + itemdata[0]
    #                     show.searchSerie(url_serie)
    #                     storage.add(itemdata[0])
    #         else:
    #             settings.log(">>>>>>>HTTP %s<<<<<<<" % response.code)
    #             settings.notification(message="HTTP %s" % response.code, force=True)
    #         if page % 5 == 0: sleep(1)
    #
    #     if optionUnica:
    #         rep = settings.dialog.select('Seleccionar tu opción:', titles + ['-CANCELAR'])
    #         if rep < len(titles):
    #             show = Shows()
    #             show.searchSerie(url_list[rep])
    #             storage.add(list_item[rep])
    #
    #     if len(show.titles) > 0:
    #         tools.int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.url_list, type_list='SHOW',
    #                                 folder=settings.show_folder, name_provider=settings.name_provider)
    # elif ret == 8:  # Borrar una serie
    #     rep = settings.dialog.select('Seleccionar la serie a borrar:', storage.database + ['-CANCELAR'])
    #     if rep < len(storage.database):
    #         if settings.dialog.yesno("Atención!", "Desea borrar los archivos strm también?", nolabel="No",
    #                                  yeslabel="Si"):
    #             tools.removeDirectory(folder=settings.show_folder, title=storage.database[rep])
    #         storage.remove(storage.database[rep])

    # common menu
    elif ret == len(option_list) - 3:  # Settings
        settings.settings.openSettings()
        settings = tools.Settings()

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
#     url_search = "%s/a/episodes" % settings.url_address
#     show.searchEpisode(url_episode=url_search, action="latest")
#     if len(show.titles) > 0:
#         tools.int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.url_list, type_list='SHOW',
#                                 folder=settings.show_folder, name_provider=settings.name_provider)
#
# elif ret == 6:  # Episodios Estreno
#     show = Shows()
#     url_search = "%s/a/episodes" % settings.url_address
#     show.searchEpisode(url_episode=url_search, action="premiere")
#     if len(show.titles) > 0:
#         tools.int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.url_list, type_list='SHOW',
#                                 folder=settings.show_folder, name_provider=settings.name_provider)
#
# elif ret == 7:  # Episodios Actualizados
#     show = Shows()
#     url_search = "%s/a/episodes" % settings.url_address
#     show.searchEpisode(url_episode=url_search, action="updated")
#     if len(show.titles) > 0:
#         tools.int_pelisalacarta(channel="hdfull", titles=show.titles, url=show.url_list, type_list='SHOW',
#                                 folder=settings.show_folder, name_provider=settings.name_provider)
