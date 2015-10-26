# coding: utf-8
# Main Addon
__author__ = 'mancuniancol'

from xbmcswift2 import Plugin
from tools import *

storage = Storage(settings.storageName, type="dict", eval=True)
plugin = Plugin()


###############################
###  MENU    ##################
###############################

@plugin.route('/')
def index():
    textViewer(plugin.get_string(32000), once=True)
    items = [
        {'label': plugin.get_string(32180),
         'path': plugin.url_for('add'),
         'thumbnail': "DefaultAddSource.png",
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Add releases...",
         'path': plugin.url_for('releases'),
         'thumbnail': "DefaultRecentlyAddedEpisodes.png",
         'properties': {'fanart_image': settings.fanart}
         }
    ]
    items.extend(read())
    return items


@plugin.route('/add')
def add():
    listName = searchAnime()
    if len(listName) > 0:
        selection = settings.dialog.select('Select One Show:', listName + ['CANCEL'])  # check the name
        if selection < len(listName):
            name = listName[selection]
            storage.database[name] = (name.replace(' ', '+'), False)  # url, isSubscribed
            storage.save()


@plugin.route('/remove/<name>')
def remove(name):
    if settings.dialog.yesno(settings.cleanName, plugin.get_string(32006) % name):
        storage.remove(name)
        storage.save()


@plugin.route('/releases')
def releases():
    listName = searchReleases()
    if len(listName) > 0:
        selection = settings.dialog.select('Select One Show:', listName + ['CANCEL'])  # check the name
        if selection < len(listName):
            name = listName[selection]
            storage.database[name] = (name.replace(' ', '+'), False)  # url, isSubscribed
            storage.save()


# read the information from url
@plugin.route('/readUrl/<url>/')
def readUrl(url):
    titles, magnets = _readUrl(url)
    settings.debug(titles)
    settings.debug(magnets)
    if __name__ == '__main__':
        plugin.set_content("tvshows")
    items = []
    for (title, magnet) in zip(titles, magnets):
        infoTitle = formatTitle(title)
        infoLabels = getInfoLabels(infoTitle)  # using script.module.metahandlers to the the infoLabels
        settings.debug(infoTitle)
        settings.debug(infoLabels)
        items.append({'label': infoLabels['label'],
                      'path': plugin.url_for('play', magnet=normalize(magnet)),
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
                                                                 magnet=normalize(magnet)))
                      ]
                      })
    return plugin.finish(items=items, view_mode=settings.value['viewMode'])


@plugin.route('/play/<magnet>')
def play(magnet):
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


@plugin.route('/importAll/<name>')
def importAll(name):
    url = storage.database[name][0]
    storage.database[name] = (url, True)
    storage.save()
    titles, magnets = _readUrl(url)
    settings.debug(titles)
    settings.debug(magnets)
    if len(titles) > 0:
        integration(titles=titles, magnets=magnets, typeList='ANIME', folder=settings.animeFolder, silence=True)


@plugin.route('/importOne/<title>/<magnet>')
def importOne(title, magnet):
    integration(titles=[title], magnets=[magnet], typeList='ANIME', folder=settings.animeFolder, silence=True)


@plugin.route('/unsubscribe/<name>')
def unsubscribe(name):
    storage.database[name] = (storage.database[name][0], False)
    storage.save()


@plugin.route('/rebuilt/<name>')
def rebuilt(name):
    overwrite = settings.value["overwrite"]  # save the user's value
    settings.value["overwrite"] = "true"  # force to overwrite
    importAll(name)
    settings.value["overwrite"] = overwrite  # return the user's value
    settings.log(name + " was rebuilt")


###############################
###  FONCTIONS    #############
###############################
# read the url list
def read():
    # list of rss available
    items = []
    for name in sorted(storage.database):  # sort the dictionnary
        (url, isIntegrated) = storage.database[name]
        settings.debug(url)
        settings.debug(isIntegrated)
        if isIntegrated:
            importInfo = (plugin.get_string(32001),
                          'XBMC.Container.Update(%s)' % plugin.url_for('unsubscribe', name=name))
        else:
            importInfo = (plugin.get_string(32002),
                          'XBMC.Container.Update(%s)' % plugin.url_for('importAll', name=name))
        infoTitle = formatTitle(name + ' S00E00')  # to force only TvShows
        infoLabels = getInfoLabels(infoTitle) if settings.value["infoLabels"] == "true" else {}
        items.append({'label': "- " + name,
                      'path': plugin.url_for('readUrl', url=url),
                      'thumbnail': infoLabels.get("cover_url", dirImages(name[0] + '.png')),
                      'properties': {'fanart_image': infoLabels.get("backdrop_url", settings.fanart)},
                      'info': infoLabels,
                      'context_menu': [importInfo,
                                       (plugin.get_string(32181),
                                        'XBMC.Container.Update(%s)' % plugin.url_for('remove', name=name)),
                                       (plugin.get_string(32045),
                                        'XBMC.Container.Update(%s)' % plugin.url_for('rebuilt', name=name))
                                       ]
                      })
    return items


def _readUrl(url):
    from socket import setdefaulttimeout
    setdefaulttimeout(10)
    magnetList = []
    titleList = []
    loop = True
    cm = 0
    while loop:
        # search for the anime
        urlSearch = '%s/lib/search.php?value=%s&nextid=%s' % (settings.value["urlAddress"], url, cm)
        settings.log(urlSearch)
        response = browser.get(urlSearch)
        data = response.text
        cm += 1
        goodSpider()
        if data is not None and len(data) > 0:
            zipList = zip(re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data), re.findall('<i>(.*?)<', data))
            for (magnet, fileName) in zipList:
                fileName = fileName.replace('_', ' ')
                info = formatTitle(fileName)
                if info["cleanTitle"].lower().replace(" ", "+") == url.lower():  # avoid sequels
                    magnetList.append(magnet)
                    pos = fileName.rfind('- ')
                    # insert EP to be identificated in kodi
                    fileName = fileName[:pos] + 'EP' + fileName[pos + 2:]
                    titleList.append(fileName)
        else:
            loop = False
    return titleList, magnetList


def searchAnime():
    name = settings.dialog.input('New Anime:')
    listNames = {}
    data = ""
    loop = True
    cm = 0
    settings.notification(settings.string(32044))
    while loop:
        url = '%s/lib/search.php?value=%s&nextid=%s' % (settings.value["urlAddress"], name.replace(' ', '+'), cm)
        response = browser.get(url)
        datatemp = response.text
        if datatemp is not None:
            data += datatemp
        cm += 1
        goodSpider()
        if datatemp is None or len(datatemp) == 0:
            loop = False
    names = [item[:item.rfind('-')].strip().replace(' -', '') for item in re.findall('\)(.*?)<', data)]
    for item in names:  # remove duplicates
        listNames[item] = 'Yes'
    return listNames.keys()


def searchReleases():
    listNames = {}
    data = ""
    loop = True
    cm = 0
    settings.notification(settings.string(32044))
    while loop:
        url = '%s/lib/latest.php?nextid=%s' % (settings.value["urlAddress"], cm)
        response = browser.get(url)
        datatemp = response.text
        if datatemp is not None:
            data += datatemp
        cm += 1
        goodSpider()
        if cm == 3 or datatemp is None or len(datatemp) == 0:
            loop = False
    names = [item[:item.rfind('-')].strip().replace(' -', '') for item in re.findall('\)(.*?)<', data)]
    for item in names:  # remove duplicates
        if item <> "":
            listNames[item] = 'Yes'
    return listNames.keys()


if __name__ == '__main__':
    plugin.run()
