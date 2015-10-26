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
    listTypes = ['Peliculas Castellano',
                 'Peliculas Latino',
                 'Estrenos de Cine',
                 'Peliculas HD',
                 'Peliculas en 3D',
                 'Otras Peliculas',
                 'Peliculas Subtituladas',
                 ]
    listUrl = ['/index.php?page=categorias&url=peliculas&letter=&pg=',
               '/index.php?page=categorias&url=peliculas-latino&letter=&pg=',
               '/index.php?page=categorias&url=estrenos-de-cine&letter=&pg=',
               '/index.php?page=categorias&url=peliculas-hd&letter=&pg=',
               '/index.php?page=categorias&url=peliculas-3d&letter=&pg=',
               '/index.php?page=categorias&url=otras-peliculas&letter=&pg=',
               '/index.php?page=categorias&url=peliculas-vo&letter=&pg=',
               ]
    listIcons = [dirImages("peliculas-castellano.png"),
                 dirImages("peliculas-latino.png"),
                 dirImages("estrenos-de-cine.png"),
                 dirImages("peliculas-hd.png"),
                 dirImages("peliculas-en-3d.png"),
                 dirImages("otras-peliculas.png"),
                 dirImages('peliculas-subtituladas.png'),
                 ]
    for type, url, icon in zip(listTypes, listUrl, listIcons):
        if type in storage.database.keys():
            importInfo = (settings.string(32001),
                          'XBMC.Container.Update(%s)' % plugin.url_for('unsubscribe', key=type))
        else:
            importInfo = (settings.string(32002),
                          'XBMC.Container.Update(%s)' % plugin.url_for('subscribe', key=type, url=url))
        items.append({'label': type,
                      'path': plugin.url_for('readItems', url=url),
                      'thumbnail': icon,
                      'properties': {'fanart_image': settings.fanart},
                      'context_menu': [importInfo, (plugin.get_string(32009),
                                                    'XBMC.RunPlugin(%s)' % plugin.url_for('importAll', key=type,
                                                                                          url=url))]
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
    url = "/buscar"
    # read from URL
    settings.log(settings.value["urlAddress"] + url)
    response = browser.post(settings.value["urlAddress"] + url, data={'q': query})
    soup = bs4.BeautifulSoup(response.text)
    links = soup.select("ul.buscar-list li")
    return readHtml(links)


@plugin.route('/play/<url>')
def play(url):
    pos = url.find('/', len(settings.value["urlAddress"]))
    url = settings.value["urlAddress"] + "/descarga-torrent" + url[pos:]
    settings.log(url)
    response = browser.get(url)
    soup = bs4.BeautifulSoup(response.text)
    links = soup.select("div#tab1 a.btn-torrent")
    magnet = links[0].get("href", "")
    # Set-up the plugin
    uri_string = quote_plus(getPlayableLink(uncodeName(magnet)))
    if settings.value["plugin"] == 'Pulsar':
        link = 'plugin://plugin.video.pulsar/play?uri=%s' % uri_string
    elif settings.value["plugin"] == 'KmediaTorrent':
        link = 'plugin://plugin.video.kmediatorrent/play/%s' % uri_string
    elif settings.value["plugin"] == "Torrenter":
        link = 'plugin://plugin.video.torrenter/?action=playSTRM&url=' + uri_string + \
               '&not_download_only=True'
    elif settings.value["plugin"] == "YATP":
        link = 'plugin://plugin.video.yatp/?action=play&torrent=' + uri_string
    else:
        link = 'plugin://plugin.video.xbmctorrent/play/%s' % uri_string
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


@plugin.route('/subscribe/<key>/<url>')
def subscribe(key="", url=""):
    storage.add(key, url)
    storage.save()
    importAll(key, url)


@plugin.route('/importAll/<key>/<url>')
def importAll(key="", url=""):
    items = readItems(url)
    titles = []
    magnets = []
    id = []
    for item in items:
        if item.has_key('info'):
            titles.append(item['info']['title'])
            id.append(item['info']['imdb_id'])
            magnets.append(getMagnet(item['path']))
    settings.debug("***************************************")
    settings.debug(titles)
    settings.debug(magnets)
    settings.debug(id)
    settings.debug("***************************************")
    if key in ['Peliculas Castellano',
               'Peliculas Latino',
               'Estrenos de Cine',
               'Peliculas HD',
               'Peliculas en 3D',
               'Otras Peliculas',
               'Peliculas Subtituladas']:
        integration(titles=titles, magnets=magnets, id=id, typeList='MOVIE',
                    folder=settings.movieFolder, silence=True)
    if key in ['Series', 'Series VOSE']:
        integration(titles=titles, magnets=magnets, typeList='SHOW',
                    folder=settings.showFolder, silence=True)
    if key in ['Anime']:
        integration(titles=titlesAnime, magnets=magnetsAnime, typeList='ANIME',
                    folder=settings.animeFolder, silence=True)


@plugin.route('/readItems/<url>', name="readItems")
@plugin.route('/nextPage/<url>/<page>', name="nextPage")
def readItems(url="", page="1"):
    # read from URL
    settings.log(settings.value["urlAddress"] + url + page)
    response = browser.get(settings.value["urlAddress"] + url + page)
    soup = bs4.BeautifulSoup(response.text)
    links = soup.select("ul.pelilist li")
    items = readHtml(links)
    # next page
    items.append({'label': "Página Siguiente..",
                  'path': plugin.url_for('nextPage', url=url, page=int(page) + 1),
                  'thumbnail': settings.icon,
                  'properties': {'fanart_image': settings.fanart}
                  })
    return items


def readHtml(links):
    # Items Menu Creation
    if __name__ == '__main__':
        plugin.set_content("movies")
    items = []
    for link in links:
        if link.h2 is not None:
            title = link.a.get("title", "").replace("Descargar", "")
            urlSource = link.a.get("href", "")
            settings.debug(title)
            infoTitle = formatTitle(title, urlSource)
            infoLabels = getInfoLabels(infoTitle)  # using script.module.metahandlers to the the infoLabels
            settings.debug(infoTitle)
            settings.debug(infoLabels)
            items.append({'label': infoLabels['label'],
                          'path': plugin.url_for('play', url=urlSource),
                          'thumbnail': infoLabels["cover_url"],
                          'properties': {'fanart_image': infoLabels["backdrop_url"]},
                          'info': infoLabels,
                          'stream_info': {'width': infoTitle["width"],
                                          'height': infoTitle["height"],
                                          'duration': infoLabels["duration"],
                                          },
                          'is_playable': True,
                          'context_menu': [
                              (plugin.get_string(32009),
                               'XBMC.RunPlugin(%s)' % plugin.url_for('importOne', title=infoLabels['label'],
                                                                     magnet=urlSource, id=infoLabels["imdb_id"]))
                          ]
                          })
    return plugin.finish(items=items, view_mode=settings.value['viewMode'])


if __name__ == '__main__':
    plugin.run()
