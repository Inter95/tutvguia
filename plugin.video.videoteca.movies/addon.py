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
    genresDict = readOptions(settings.value["urlAddress"])
    items = [
        {'label': " Busqueda Manual",
         'path': plugin.url_for('search'),
         'thumbnail': dirImages("busqueda-manual.png"),
         'properties': {'fanart_image': settings.fanart}
         }]

    for type, url in genresDict.iteritems():
        if type in storage.database.keys():
            importInfo = (settings.string(32001),
                          'XBMC.Container.Update(%s)' % plugin.url_for('unsubscribe', key=type))
        else:
            importInfo = (settings.string(32002),
                          'XBMC.Container.Update(%s)' % plugin.url_for('subscribe', key=type, url=url))
        items.append({'label': type,
                      'path': plugin.url_for('readItems', url=url),
                      'thumbnail': dirImages(type + ".png"),
                      'properties': {'fanart_image': settings.fanart},
                      'context_menu': [importInfo, (plugin.get_string(32009),
                                                    'XBMC.RunPlugin(%s)' % plugin.url_for('importAll', key=type,
                                                                                          url=url))]
                      })
    return plugin.finish(items, sort_methods=['date'])


@plugin.route('/search/')
def search():
    query = settings.dialog.input("Cual película buscar?")
    url = "%s/es/peliculas/custom/?search=%s" % (settings.value["urlAddress"], query)
    return readItems(url)


@plugin.route('/play/<url>')
def play(url):
    uri_string = quote_plus(url)
    # Set-up the plugin
    channel = "yaske"
    link = "plugin://plugin.video.pelisalacarta/?channel=%s&action=play_from_library&url=%s" % (channel, uri_string)
    # play media
    settings.debug("PlayMedia(%s)" % link)
    xbmc.executebuiltin("PlayMedia(%s)" % link)


@plugin.route('/importOne/<title>/<magnet>/<id>')
def importOne(title="", magnet="", id=""):
    integration(titles=[title], magnets=[magnet], id=[id], typeList='MOVIE', folder=settings.movieFolder, silence=True)


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
    integration(titles=titles, magnets=magnets, id=id, typeList='MOVIE',
                folder=settings.movieFolder, silence=True)


@plugin.route('/readItems/<url>', name="readItems")
@plugin.route('/nextPage/<url>/<page>', name="nextPage")
def readItems(url="", page="1"):
    # read from URL
    settings.log(url)
    response = browser.get(url)
    soup = bs4.BeautifulSoup(response.text)
    links = soup.select("li.item-movies a.image-block")

    # Items Menu Creation
    if __name__ == '__main__':
        plugin.set_content("movies")
    items = []
    for a in links:
        title = a.get("title", "")
        urlSource = a["href"]
        settings.debug(title)
        infoTitle = formatTitle(title, urlSource)
        settings.debug(infoTitle)
        infoLabels = getInfoLabels(infoTitle)  # collect the TheMovieDB and TheTVDB info from the title
        settings.debug(infoLabels)
        if settings.value["infoLabels"] == "true" and len(infoLabels) > 0:  # there is information from TheMovieDB
            title = (normalize(infoLabels.get("title", ""), onlyDecode=True) if type == "Movie" else infoTitle[
                "title"]) + infoTitle.get("textQuality", "") + " " + infoTitle["language"]
            items.append({'label': title,
                          'path': plugin.url_for('play', url=urlSource),
                          'thumbnail': infoLabels.get("cover_url", ""),
                          'properties': {'fanart_image': infoLabels.get("backdrop_url", "")},
                          'info': infoLabels,
                          'stream_info': {'width': infoTitle["width"],
                                          'height': infoTitle["height"]
                                          },
                          'is_playable': True,
                          'context_menu': [
                              (plugin.get_string(32009),
                               'XBMC.RunPlugin(%s)' % plugin.url_for('importOne', title=title, magnet=urlSource,
                                                                     id=infoLabels["imdb_id"]))
                          ]
                          })
        else:  # Not information found
            title = infoTitle["title"] + ' - ' + infoTitle.get("quality", "")
            try:
                items.append({'label': title,
                              'path': plugin.url_for('play', url=urlSource),
                              'thumbnail': settings.icon,
                              'properties': {'fanart_image': settings.fanart},
                              'context_menu': [
                                  (plugin.get_string(32009),
                                   'XBMC.RunPlugin(%s)' % plugin.url_for('importOne', title=title, url=urlSource,
                                                                         id=infoLabels["imdb_id"]))
                              ]
                              })
            except:
                pass
    # next page
    items.append({'label': "Página Siguiente..",
                  'path': plugin.url_for('nextPage',
                                         url=changeUrl(url) % (int(page) + 1), page=int(page) + 1),
                  'thumbnail': settings.icon,
                  'properties': {'fanart_image': settings.fanart}
                  })
    return items


def changeUrl(url):
    if url == "http://www.yaske.cc":
        url += "/es/peliculas/page/%s"
    elif 'page' in url:
        url = re.sub("[0-9]+", "%s", url)
    else:
        url = url.replace("/peliculas/", "/peliculas/page/%s/")
    return url


def readOptions(url=""):
    result = None
    goodSpider()
    response = browser.get(url)  # open the serie
    if response.status_code == requests.codes.ok:
        soup = bs4.BeautifulSoup(response.text)
        genres = {" TODAS": "http://www.yaske.cc"}
        links = soup.select('form#form_custom select#genres option')
        links.pop(0)
        for link in links:
            genres[link.text] = "%s/es/peliculas/genero/%s" % (settings.value["urlAddress"], link.attrs.get("value"))
        result = genres
    else:
        settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
        settings.notification(message="HTTP %s" % response.status_code, force=True)
    return result


if __name__ == '__main__':
    plugin.run()
