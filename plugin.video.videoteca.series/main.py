# coding: utf-8
# Main Addon
__author__ = 'mancuniancol'

from xbmcswift2 import Plugin
from tools import *


##INITIALISATION
storage = Storage(settings.storageName, type="dict")
plugin = Plugin()


###############################
###  MENU    ##################
###############################
@plugin.route('/')
def index():
    textViewer(settings.string(32000), once=True)
    items = [
        {'label': "Busqueda Manual",
         'path': plugin.url_for('search'),
         'thumbnail': dirImages("busqueda-manual.png"),
         'properties': {'fanart_image': settings.fanart}
         }]
    listTypes = ['Series Más Vistas',
                 'Series Más recientes',
                 'Series Más Populares',
                 'Animes',
                 'Novelas',
                 ]
    listType2 = ['series',
                 'series',
                 'series',
                 'generos',
                 'generos',
                 ]
    listOrder = ['hits',
                 'fecha',
                 'rating',
                 'animes',
                 'novelas',
                 ]
    listIcons = [dirImages("series.png"),
                 dirImages("series.png"),
                 dirImages("estrenos.png"),
                 dirImages("series.png"),
                 dirImages("series.png"),
                 ]
    for type, type2, order, icon in zip(listTypes, listType2, listOrder, listIcons):
        if type in storage.database.keys():
            importInfo = (settings.string(32001),
                          'XBMC.Container.Update(%s)' % plugin.url_for('unsubscribe', key=type))
        else:
            importInfo = (settings.string(32002),
                          'XBMC.Container.Update(%s)' % plugin.url_for('subscribe', key=type, type2=type2, order=order))
        items.append({'label': type,
                      'path': plugin.url_for('readItems', type2=type2, order=order),
                      'thumbnail': icon,
                      'properties': {'fanart_image': settings.fanart},
                      'context_menu': [importInfo, (plugin.get_string(32009),
                                                    'XBMC.RunPlugin(%s)' % plugin.url_for('importAll', key=type,
                                                                                          type2=type2, order=order))]
                      })
    items.append({'label': "Ayuda",
                  'path': plugin.url_for('help'),
                  'thumbnail': dirImages("ayuda.png"),
                  'properties': {'fanart_image': settings.fanart}
                  })
    return items


@plugin.route('/help/')
def help():
    textViewer(plugin.get_string(32000), once=False)


@plugin.route('/search/')
def search():
    query = settings.dialog.input("Cual película buscar?")
    url = "/busqueda/%s/pag:" % query
    return readItems(url)


@plugin.route('/play/<url>')
def play(url):
    uri_string = quote_plus(url)
    # Set-up the plugin
    channel = "seriesflv"
    link = "plugin://plugin.video.pelisalacarta/?channel=%s&action=play_from_library&url=%s" % (channel, uri_string)
    # play media
    settings.debug("PlayMedia(%s)" % link)
    xbmc.executebuiltin("PlayMedia(%s)" % link)


@plugin.route('/importOne/<title>/<magnet>/<id>')
def importOne(title="", magnet="", id=""):
    info = formatTitle(title)
    if 'MOVIE' in info['type']:
        integration(titles=[title], magnets=[magnet], id=[id], typeList='MOVIE', folder=settings.movieFolder,
                    silence=True)
    if 'SHOW' in info['type']:
        integration(titles=[title], magnets=[magnet], id=[id], typeList='SHOW', folder=settings.showFolder,
                    silence=True)
    if 'ANIME' in info['type']:
        integration(titles=[title], magnets=[magnet], id=[id], typeList='ANIME', folder=settings.animeFolder,
                    silence=True)


@plugin.route('/unsubscribe/<key>')
def unsubscribe(key=""):
    storage.remove(key)
    storage.save()


@plugin.route('/subscribe/<key>/<type2>/<order>')
def subscribe(key="", type2="", order=""):
    storage.add(key, (type2, order))
    storage.save()
    importAll(key, type2, order)


@plugin.route('/importAll/<key>/<type2>/<order>')
def importAll(key="", type2="", order=""):
    items = readItems(type2, order)
    titles = []
    magnets = []
    id = []
    for item in items:
        if item.has_key('info'):
            titles.append(item['info']['title'])
            id.append(item['info']['tvdb_id'])
            magnets.append(getMagnet(item['path']))
    settings.debug("***************************************")
    settings.debug(titles)
    settings.debug(magnets)
    settings.debug(id)
    settings.debug("***************************************")
    integration(titles=titles, magnets=magnets, typeList="SHOW",
                folder=settings.showFolder, silence=True)
    # if len(titlesAnime) > 0:
    #     integration(titles=titlesAnime, magnets=magnetsAnime, typeList='ANIME',
    #                 folder=settings.animeFolder, silence=True)


@plugin.route('/readItems/<type2>/<order>', name="readItems")
@plugin.route('/nextPage/<type2>/<order>/<page>', name="nextPage")
def readItems(type2="", order="", page="1"):
    # read from URL
    url = settings.value["urlAddress"] + '/ajax/lista.php'
    settings.log(url)
    if type2 == "search":
        parameters = ""
    else:
        parameters = {'grupo_no': page, 'type': type2, 'order': order}

    response = browser.post(url=url, data=parameters)
    soup = bs4.BeautifulSoup(response.text)
    links = soup.select("a")

    # Items Menu Creation
    if __name__ == '__main__':
        plugin.set_content("movies")
    items = []
    for a in links:
        if parameters == "":
            title = a.span.text
        else:
            title = a.div.text.strip()
        urlSource = a["href"]
        settings.debug(title)
        infoTitle = formatTitle(a["href"], urlSource, "SHOW")  # organize the title information
        infoLabels = getInfoLabels(infoTitle)  # using script.module.metahandlers to the the infoLabels
        settings.debug(infoTitle)
        settings.debug(infoLabels)
        items.append({'label': infoLabels['label'],
                      'path': plugin.url_for('seasons', url=urlSource, thumbnail=infoLabels["cover_url"],
                                             fanart=infoLabels["backdrop_url"]),
                      'thumbnail': infoLabels["cover_url"],
                      'properties': {'fanart_image': infoLabels["backdrop_url"]},
                      'context_menu': [
                          (plugin.get_string(32009),
                           'XBMC.RunPlugin(%s)' % plugin.url_for('importOne', title=infoLabels['label'],
                                                                 magnet=urlSource, id=infoLabels["tvdb_id"]))
                      ]
                      })
    # next page
    items.append({'label': "Página Siguiente..",
                  'path': plugin.url_for('nextPage', type2=type2, order=order, page=int(page) + 1),
                  'thumbnail': settings.icon,
                  'properties': {'fanart_image': settings.fanart}
                  })
    return plugin.finish(items=items, view_mode=settings.value['viewMode'])


@plugin.route('/seasons/<url>/<thumbnail>/<fanart>')
def seasons(url, thumbnail, fanart=settings.fanart):
    urlDict = plugin.get_storage('urlDict')
    urlDict.clear()
    urlDict.sync()
    titleDict = plugin.get_storage('titleDict')
    titleDict.clear()
    titleDict.sync()
    response = browser.get(url)  # open the serie
    if response.status_code == requests.codes.ok:
        soup = bs4.BeautifulSoup(response.text)
        infoTitle = ''
        if soup.select('tr.mainInfoClass a')[0].text:
            links = soup.select('td.sape a')
            for link in links:
                infoTitle = formatTitle(link.text, typeVideo="SHOW")
                season = infoTitle.get("season", 0)
                if titleDict.get(season, "") == "":
                    titleDict[season] = []
                titleDict[season].append(infoTitle)
                if urlDict.get(season, "") == "":
                    urlDict[season] = []
                urlDict[season].append(link.attrs.get('href'))
        # creating season items
        items = []
        infoLabels = getInfoLabels(infoTitle)  # using script.module.metahandlers to the the infoLabels
        settings.debug(infoTitle)
        settings.debug(infoLabels)
        infoSeason = getInfoSeason(infoLabels, titleDict.keys())
        settings.debug(infoSeason)
        for season, images in zip(titleDict.keys(), infoSeason):
            items.append({'label': "Temporada %s" % season,
                          'path': plugin.url_for('episodes', season=season),
                          'thumbnail': images["cover_url"],
                          'properties': {'fanart_image': images["backdrop_url"]},
                          'info': infoLabels,
                          })
        return items
    else:
        settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
        settings.notification(message="HTTP %s" % response.status_code, force=True)


@plugin.route('/episodes/<season>')
def episodes(season="0"):
    urlDict = plugin.get_storage('urlDict')
    titleDict = plugin.get_storage('titleDict')
    items = []
    season = int(season)
    for urlSource, infoTitle in zip(urlDict[season], titleDict[season]):
        infoLabels = getInfoLabels(infoTitle)  # using script.module.metahandlers to the the infoLabels
        infoStream = getInfoStream(infoTitle, infoLabels)
        infoEpisode = getInfoEpisode(infoLabels)
        settings.debug(infoTitle)
        settings.debug(infoLabels)
        settings.debug(infoStream)
        settings.debug(infoEpisode)
        items.append({'label': "%02d. %s" % (infoEpisode['episode'], infoEpisode['title']),
                      'path': plugin.url_for('play', url=urlSource),
                      'thumbnail': infoEpisode["cover_url"],
                      'properties': {'fanart_image': infoEpisode["backdrop_url"]},
                      'info': infoEpisode,
                      'stream_info': infoStream,
                      'is_playable': True,
                      'context_menu': [
                          (plugin.get_string(32009),
                           'XBMC.RunPlugin(%s)' % plugin.url_for('importOne', title=infoLabels['label'],
                                                                 magnet=urlSource, id=infoLabels["tvdb_id"]))
                      ]
                      })
    return items


# main
if __name__ == '__main__':
    plugin.run()
