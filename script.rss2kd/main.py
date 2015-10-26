# coding: utf-8
# Main
__author__ = 'mancuniancol'

from tools import *
import feedparser

storage = Storage(settings.storageName, type="dict")

# this read the settings
list_url_search = []
rep = 0

while rep < 7:
    rep = settings.dialog.select('Choose an Option:', ['Add a New [COLOR ffff9900]RSS[/COLOR]',
                                                       'Modify Saved [COLOR ffff9900]RSS[/COLOR]',
                                                       'Remove a [COLOR ffff9900]RSS[/COLOR]',
                                                       'View Saved [COLOR ffff9900]RSS[/COLOR] list',
                                                       'Read [COLOR ffff9900]RSS[/COLOR] list and create .strm Files in',
                                                       'Erase Folders',
                                                       '-SETTINGS',
                                                       '-HELP',
                                                       'Exit'])
    if rep == 0:  # Add a New RSS
        selection = settings.dialog.input('URL RSS:')
        name = ''
        while name is '':
            name = settings.dialog.input('Name to this RSS:').title()
        storage.database[name] = selection

    if rep == 1:  # Modify RSS list
        List = [name + ": " + RSS for (name, RSS) in zip(storage.database.keys(), storage.database.values())]
        list_rep = settings.dialog.select('Shows', List + ['CANCEL'])
        if list_rep < len(List):
            name = storage.database.keys()[list_rep]
            storage.database[name] = settings.dialog.input('URL RSS:', storage.database[name])

    if rep == 2 and len(storage.database.keys()) > 0:  # Remove a RSS
        List = [name + ": " + RSS for (name, RSS) in zip(storage.database.keys(), storage.database.values())]
        list_rep = settings.dialog.select('Choose RSS to Remove', List + ['CANCEL'])
        if list_rep < len(List):
            if settings.dialog.yesno('', 'Do you want Remove %s?' % List[list_rep]):
                storage.remove(storage.database.keys()[list_rep])

    if rep == 3:  # View Saved RSS list
        List = [name + ": " + RSS for (name, RSS) in zip(storage.database.keys(), storage.database.values())]
        settings.dialog.select('Shows', List)

    if rep ==4:  # Read RSS list and create .strm Files
        list_url_search = storage.database.values()
        # Begin reading
        magnetsMovie = []
        titlesMovie = []
        magnetsShow = []
        titlesShow = []
        magnetsAnime = []
        titlesAnime = []
        for url_search in list_url_search:
            if url_search is not '':
                settings.notification('Checking Online\n%s...' % url_search)
                settings.log(url_search)
                response = feedparser.parse(url_search)
                for entry in response.entries:
                    isMagnet = False
                    for key in entry.keys():
                        if "magnet" in key:
                            isMagnet = True
                            tag = key
                            break
                    if isMagnet:
                        value = entry[tag]
                    else:
                        for link in entry.links:
                            value = link.href  # Taking the last link
                    info = format_title(entry.title)
                    if 'MOVIE' in info['type']:
                        titlesMovie.append(entry.title)
                        magnetsMovie.append(value)
                    if 'SHOW' in info['type']:
                        titlesShow.append(entry.title)
                        magnetsShow.append(value)
                    if 'ANIME' in info['type']:
                        titlesAnime.append(entry.title)
                        magnetsAnime.append(value)
        if len(titlesMovie) > 0:
            integration(filenames=titlesMovie, magnets=magnetsMovie, typeList='MOVIE',
                        folder=settings.movieFolder, silence=True)
        if len(titlesShow) > 0:
            integration(filenames=titlesShow, magnets=magnetsShow, typeList='SHOW',
                        folder=settings.showFolder, silence=True)
        if len(titlesAnime) > 0:
            integration(filenames=titlesAnime, magnets=magnetsAnime, typeList='ANIME',
                        folder=settings.animeFolder, silence=True)

    if rep == 5:  # Erase Folders
        selectionRemove = settings.dialog.select('Choose an Option:', ['Movies', 'TV Shows', 'Animes'])
        if selectionRemove == 0:
            removeDirectory(settings.movieFolder)
        elif selectionRemove == 1:
            removeDirectory(settings.showFolder)
        else:
            removeDirectory(settings.animeFolder)

    if rep == 6:  # Settings
        settings.settings.openSettings()
        del settings
        settings = Settings()

    if rep == 7:  # Help
        settings.dialog.ok("Help",
                           "Please, check this address to find the user's operation:\n[B]http://goo.gl/8nYU6R[/B]")
# save the dictionary
storage.save()

del settings
del storage
del browser
