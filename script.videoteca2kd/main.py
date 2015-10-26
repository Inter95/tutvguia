# coding: utf-8

from xbmc import sleep
from videoteca import *
from urllib import quote_plus

######################################
#############  MAIN MENU  ############
######################################
option_list = ['Busqueda Manual [COLOR FF2107a2]Película[/COLOR]',  # 0
               '[COLOR FF2107a2]Películas[/COLOR]',  # 1
               'Borrar una [COLOR FF2107a2]Película[/COLOR]',  # 2
               'Busqueda Manual [COLOR FF07a221]Serie o Novela[/COLOR]',  # 3
               '[COLOR FF07a221]Series[/COLOR]',  # 4
               '[COLOR FF07a221]Novela[/COLOR]',  # 5
               'Borrar una [COLOR FF07a221]Serie o Novela[/COLOR]',  # 6
               'Busqueda Manual [COLOR FFa20721]Anime[/COLOR]',  # 7
               '[COLOR FFa20721]Anime[/COLOR]',  # 8
               'Borrar un [COLOR FFa20721]Anime[/COLOR]',  # 9
               ]
option_list.extend(['-CONFIGURACIÓN', '-AYUDA', 'Salir'])

ret = 0
while ret < len(option_list) - 1:
    ret = settings.dialog.select('Opción:', option_list)

    if ret == 0:  # Busqueda Manual #0
        search = settings.dialog.input('Palabras clave a buscar:')
        if search is not '':
            menu = Menu(type="movie", url="URL/es/peliculas/custom/?search=%s" % quote_plus(search),
                        channel="yaske")
            menu.play(silence=True)

    elif ret == 1:  # Peliculas #1
        # peliculaDict = {'Audio Latino': 'la', 'Audio Español': 'es', 'Subtitulada': 'sub'}
        # pelicula = settings.dialog.select('Audio:', peliculaDict.keys())
        yearsDict, genresDict  = readOptions(settings.url_address)
        genresDict.pop("Adultos", None)
        yearsList =yearsDict.keys()
        yearsList.sort()
        genresList =genresDict.keys()
        genresList.sort()
        genre = settings.dialog.select('Género:', genresList)
        #year = settings.dialog.select('Año:', yearsList)
        if genre==0:
            menu = Menu(type="movie", url="URL/es/peliculas/page/PAGE", channel="yaske")
        else:
            menu = Menu(type="movie", url="URL/es/peliculas/page/PAGE/genero/%s" % (
            #peliculaDict[peliculaDict.keys()[pelicula]], yearsDict[yearsList[year]],
            genresDict[genresList[genre]]), channel="yaske")
        menu.play()

    elif ret == 2:  # Borrar una Película  #2
        menu = Menu(type="erase-movie")
        menu.play()

    elif ret == 3:  # Buscar una serie #3
        search = settings.dialog.input('Palabras clave a buscar:')
        if search is not '':
            menu = Menu(type="show", url="URL/api/search/?q=%s" % quote_plus(search), channel="seriesflv",
                        type2="search")
            menu.play(silence=True)

    elif ret == 4:  # Series #4
        seriesDict = {'Mas Vistas': 'hits', 'Fecha': 'fecha', 'Ranking': 'rating'}
        serie = settings.dialog.select('Ordenado por:', seriesDict.keys())
        menu = Menu(type="show", url="URL/ajax/lista.php", channel="seriesflv", type2='series',
                    order=seriesDict[seriesDict.keys()[serie]])
        menu.play()

    elif ret == 5:  # Novelas #5
        menu = Menu(type="show", url="URL/ajax/lista.php", channel="seriesflv", type2='generos', order="novelas")
        menu.play()

    elif ret == 6:  # Borrar una serie
        rep = settings.dialog.select('Seleccionar la serie a borrar:', storage.database.keys() + ['-CANCELAR'])
        if rep < len(storage.database):
            if settings.dialog.yesno("Atención!", "Desea borrar los archivos strm también?", nolabel="No",
                                     yeslabel="Si"):
                tools.removeDirectory(folder=settings.show_folder, title=storage.database.keys()[rep])
            storage.remove(storage.database.keys()[rep])

    elif ret == 7:  # Buscar una anime #7
        search = settings.dialog.input('Palabras clave a buscar:')
        if search is not '':
            menu = Menu(type="anime", url="URL/api/search/?q=%s" % quote_plus(search), channel="seriesflv",
                        type2="search")
            menu.play()

    elif ret == 8:  # Anime #8
        menu = Menu(type="anime", url="URL/ajax/lista.php", channel="seriesflv", type2='generos', order="animes")
        menu.play()

    elif ret == 9:  # Borrar un Anime #9
        rep = settings.dialog.select('Seleccionar el Anime a borrar:', storageAnime.database.keys() + ['-CANCELAR'])
        if rep < len(storageAnime.database):
            if settings.dialog.yesno("Atención!", "Desea borrar los archivos strm también?", nolabel="No",
                                     yeslabel="Si"):
                tools.removeDirectory(folder=settings.anime_folder, title=storageAnime.database.keys()[rep])
            storageAnime.remove(storageAnime.database.keys()[rep])

    # common menu
    elif ret == len(option_list) - 3:  # Settings
        settings.settings.openSettings()
        settings = tools.Settings()

    elif ret == len(option_list) - 2:  # Help
        settings.dialog.ok("Ayuda",
                           "El manual de operacion se encuentra en esta dirección:\n[B]http://goo.gl/0b44BY[/B]")


# save the database
storage.save()
storageAnime.save()
# del storage
del settings
del browser
