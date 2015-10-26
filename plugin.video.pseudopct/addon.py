import sys
from os import path
import urllib
import urlparse
import json

from xbmc import log
from xbmcaddon import Addon
import xbmcplugin
from common import *


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


def width(quality="480p"):
    result = 720
    if '480p' in quality:
        result = 720
    elif '720p' in quality:
        result = 1280
    elif '1080p' in quality:
        result = 1920
    elif '3D' in quality:
        result = 1920
    return result


def getEpisode(query=""):
    query = query.replace('_', ' ').replace('- ', '-')
    result = re.findall('-[0-9]+', query)
    if len(result) > 0:
        result = result[0].replace('-', '')
    return result


def uncode_name(name):  # convert all the &# codes to char, remove extra-space and normalize
    from HTMLParser import HTMLParser

    name = name.replace('<![CDATA[', '').replace(']]', '')
    name = HTMLParser().unescape(name.lower())
    return name


def link(uri_string):
    from urllib import quote_plus

    uri_string = quote_plus(uncode_name(uri_string))
    if plugin == 'Pulsar':
        link = 'plugin://plugin.video.pulsar/play?uri=%s' % uri_string
    elif plugin == 'KmediaTorrent':
        link = 'plugin://plugin.video.kmediatorrent/play/%s' % uri_string
    elif plugin == "Torrenter":
        link = 'plugin://plugin.video.torrenter/?action=playSTRM&url=' + uri_string + '&not_download_only=True'
    else:
        link = 'plugin://plugin.video.xbmctorrent/play/%s' % uri_string
    return link


#################################################################################################################
#################################################################################################################
#################################################################################################################

# getting arguments
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
# reading arguments values
mode = args.get('mode', [None])[0]
page = args.get('page', ['1'])[0]
quality = args.get('quality', [None])[0]
IMDB = args.get('IMDB', [None])[0]
seasons = args.get('seasons', [0])[0]
season = args.get('season', [0])[0]
poster = args.get('poster', [None])[0]
fanart = args.get('fanart', [Addon().getAddonInfo('fanart')])[0]
query = args.get('query', ['None'])[0]


# initialisation browser
browser = Browser()

# initialisation variables
qua = {'0': '', '480p': '480p', '720p': '720p', '1080p': '1080p'}
name_addon = re.sub('.COLOR (.*?)]', '', Addon().getAddonInfo('name').replace('[/COLOR]', ''))
icon = Addon().getAddonInfo('icon')
url_movies = Addon().getSetting('url_movies')
url_tvshows = Addon().getSetting('url_tvshows')
url_anime = Addon().getSetting('url_anime')
plugin = Addon().getSetting('plugin')
root = Addon().getAddonInfo('path')
# movies
genre = Addon().getSetting('genre').replace(' ', '-')
minimum_rating = Addon().getSetting('minimum_rating')
sort_by = Addon().getSetting('sort_by')
order_by = Addon().getSetting('order_by')


# Settings
if mode == 'settings':
    Addon().openSettings()
    mode = None

# Trailer
if mode == 'trailer':
    lib_path = path.abspath(path.join(root, '..', 'script.extendedinfo', 'resources', 'lib'))
    sys.path.append(lib_path)
    from TheMovieDB import *

    xbmc.executebuiltin('XBMC.RunPlugin("plugin://script.extendedinfo/?info=youtubevideo&&id=%s")' % get_trailer(IMDB))

# first level
if mode is None:
    xbmcplugin.setContent(addon_handle, 'tvshows')
    url = build_url({'mode': 'movies', 'page': '1'})
    li = xbmcgui.ListItem('Movies', iconImage=path.join(root, 'images', '1.png'))
    li.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'tvshows', 'page': '1'})
    li = xbmcgui.ListItem('TV Shows', iconImage=path.join(root, 'images', '2.png'))
    li.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'anime', 'page': '1'})
    li = xbmcgui.ListItem('Anime', iconImage=path.join(root, 'images', '3.png'))
    li.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'space': 'space'})
    li = xbmcgui.ListItem(' ', iconImage=path.join(root, 'images', '4.png'))
    li.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)

    url = build_url({'mode': 'search-movie'})
    li = xbmcgui.ListItem('Search Movie', iconImage=path.join(root, 'images', '5.png'))
    li.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'search-tvshows'})
    li = xbmcgui.ListItem('Search TV Show', iconImage=path.join(root, 'images', '6.png'))
    li.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'search-anime'})
    li = xbmcgui.ListItem('Search Anime', iconImage=path.join(root, 'images', '3.png'))
    li.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'space': 'space'})
    li = xbmcgui.ListItem(' ', iconImage=path.join(root, 'images', '4.png'))
    li.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)

    url = build_url({'mode': 'settings'})
    li = xbmcgui.ListItem('Settings', iconImage=path.join(root, 'images', '5.png'))
    li.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

# second level
else:
    if mode == "search-movie":
        query = xbmcgui.Dialog().input('Search:', type=xbmcgui.INPUT_ALPHANUM).replace(' ', '+')
        mode = 'movies'

    if mode == "search-tvshows":
        query = xbmcgui.Dialog().input('Search:', type=xbmcgui.INPUT_ALPHANUM).replace(' ', '+')
        mode = 'tvshows'

    if mode == "search-anime":
        query = xbmcgui.Dialog().input('Search:', type=xbmcgui.INPUT_ALPHANUM).replace(' ', '+')
        mode = 'anime'

    if mode == 'movies':
        if quality is None:
            # Setting Content
            xbmcplugin.setContent(addon_handle, 'tvshows')
            url = build_url({'mode': mode, 'page': page, 'quality': '720p', 'query': query})
            li = xbmcgui.ListItem('720p', iconImage=path.join(root, 'images', '4.png'))
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

            url = build_url({'mode': mode, 'page': page, 'quality': '1080p', 'query': query})
            li = xbmcgui.ListItem('1080p', iconImage=path.join(root, 'images', '5.png'))
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

            url = build_url({'mode': mode, 'page': page, 'quality': '3D', 'query': query})
            li = xbmcgui.ListItem('3D', iconImage=path.join(root, 'images', '6.png'))
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

        else:
            # build menu with the movies
            # Setting Content
            xbmcplugin.setContent(addon_handle, 'movies')
            if 'None' in query:
                url_search = "%s/api/v2/list_movies.json?quality=%s&page=%s&genre=%s&minimum_rating=%s&sort_by=%s" \
                             "&order_by=%s" % (
                                 url_movies, quality, page, genre, minimum_rating, sort_by, order_by)
            else:
                url_search = '%s/api/v2/list_movies.json?page=1&query_term=%s' % (url_movies, query)

            log('[%s] %s' % (name_addon, url_search))
            browser.open(url_search)
            data = json.loads(browser.content)
            for item in data['data']['movies']:
                for torrent in item['torrents']:
                    if torrent['quality'] == quality:
                        url = link(torrent['url'])
                        li = xbmcgui.ListItem(label=item['title'] + ' - ' + torrent['quality'],
                                              iconImage=item['medium_cover_image'],
                                              thumbnailImage=item['medium_cover_image'])
                        li.setInfo(type='Video',
                                   infoLabels={'title': item['title_long'], 'sorttitle': item['title'],
                                               'year': item['year'],
                                               'code': item['imdb_code'], 'mpaa': item['mpa_rating'],
                                               'rating': item['rating'],
                                               'genre': ' / '.join(item['genres']), 'duration': item['runtime']*60
                                               })
                        li.addStreamInfo('Video',
                                         {'language': item['language'], 'duration': item['runtime'],
                                          'width': width(quality),
                                          'height': quality.replace('p', '').replace('3D', '1080')
                                          })
                        li.addContextMenuItems([('Movie Info',
                                                 'XBMC.RunScript(script.extendedinfo,info=extendedinfo,imdb_id=%s)' %
                                                 item['imdb_code']),
                                                ('Trailer',
                                                 'XBMC.RunScript(plugin.video.pseudopct, %s, '
                                                 '"?mode=trailer&IMDB=%s")' % (
                                                 addon_handle, item['imdb_code']))
                                                ])
                        li.setProperty('fanart_image', item['background_image'])
                        li.setProperty('IsPlayable', 'true')
                        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
            if 'None' in query:
                url = build_url({'mode': 'movies', 'quality': quality, 'page': int(page) + 1})
                li = xbmcgui.ListItem('Next Page...')
                li.setProperty('fanart_image', fanart)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    elif mode == 'tvshows':
        # Setting Content
        xbmcplugin.setContent(addon_handle, 'tvshows')

        if quality is None:
            url = build_url({'mode': mode, 'page': page, 'quality': '0', 'query': query})
            li = xbmcgui.ListItem('HDTV', iconImage=path.join(root, 'images', '4.png'))
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

            url = build_url({'mode': mode, 'page': page, 'quality': '480p', 'query': query})
            li = xbmcgui.ListItem('480p', iconImage=path.join(root, 'images', '5.png'))
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

            url = build_url({'mode': mode, 'page': page, 'quality': '720p', 'query': query})
            li = xbmcgui.ListItem('720p', iconImage=path.join(root, 'images', '6.png'))
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

        else:
            # build menu with the tv shows
            if 'None' in query:
                url_search = "%s/shows/%s" % (url_tvshows, page)
            else:
                url_search = "%s/shows/1?sort=seeds&limit=50&keywords=%s&order=-1" % (url_tvshows, query)
            log('[%s] %s' % (name_addon, url_search))
            browser.open(url_search)
            data = json.loads(browser.content)
            for item in data:
                url = build_url({'mode': 'seasons', 'quality': quality, 'page': page, 'IMDB': item['imdb_id'],
                                 'seasons': item['num_seasons'], 'poster': item['images']['poster'],
                                 'fanart': item['images']['fanart']})
                li = xbmcgui.ListItem(label=item['title'], iconImage=item['images']['poster'],
                                      thumbnailImage=item['images']['poster'])
                li.setInfo(type='Video', infoLabels={'title': item['title'], 'year': item['year']})
                li.setProperty('fanart_image', item['images']['fanart'])
                li.setProperty('IsPlayable', 'false')
                li.addContextMenuItems([('TV Show Info',
                                         'XBMC.RunScript(script.extendedinfo,info=extendedtvinfo,imdb_id=%s)' %
                                         item['imdb_id'])
                                        ])
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
            if 'None' in query:
                url = build_url(
                    {'mode': 'tvshows', 'quality': quality, 'page': int(page) + 1, 'IMDB': item['imdb_id']})
                li = xbmcgui.ListItem('Next Page...')
                li.setProperty('fanart_image', fanart)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    elif mode == 'seasons':
        # Setting Content
        xbmcplugin.setContent(addon_handle, 'tvshows')

        # build menu with the seasons
        for season in range(1, int(seasons)):
            url = build_url(
                {'mode': 'tvshow', 'quality': quality, 'page': page, 'IMDB': IMDB, 'season': season,
                 'poster': poster,
                 'fanart': fanart})
            li = xbmcgui.ListItem(label='Season %s' % season, iconImage=poster, thumbnailImage=poster)
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    elif mode == 'tvshow':
        # Setting Content
        xbmcplugin.setContent(addon_handle, 'episodes')

        # build menu with the episode tv shows
        url_search = "%s/show/%s" % (url_tvshows, IMDB)
        log('[%s] %s' % (name_addon, url_search))
        browser.open(url_search)
        data = json.loads(browser.content)
        for episode in data['episodes']:
            if int(season) == int(episode['season']):
                if episode['torrents'].has_key(quality):
                    value_quality = quality
                else:
                    value_quality = '0'
                url = link(episode['torrents'][value_quality]['url'])
                li = xbmcgui.ListItem(
                    label=str(episode['episode']) + ' - ' + episode['title'] + ' - ' + qua[value_quality],
                    iconImage=poster, thumbnailImage=poster)
                li.setInfo(type='Video',
                           infoLabels={'title': episode['title'], 'sorttitle': episode['title'],
                                       'year': data['year'],
                                       'code': IMDB,
                                       'episode': episode['episode'],
                                       'season': episode['season'],
                                       'studio': data['network'],
                                       'plot': data['synopsis'],
                                       'rating': float(data['rating']['percentage']) / 10,
                                       'genre': ' / '.join(data['genres']), 'duration': data['runtime']})
                li.addStreamInfo('Video',
                                 {'language': data['country'], 'duration': data['runtime'],
                                  'width': width(quality), 'height': quality.replace('p', '')
                                  })
                li.setProperty('fanart_image', fanart)
                li.setProperty('IsPlayable', 'true')
                xbmcplugin.addSortMethod(handle=addon_handle, sortMethod=xbmcplugin.SORT_METHOD_EPISODE)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

    elif mode == 'anime':
        # Setting Content
        xbmcplugin.setContent(addon_handle, 'tvshows')

        if quality is None:
            url = build_url({'mode': mode, 'page': page, 'quality': '480p', 'query': query})
            li = xbmcgui.ListItem('480p', iconImage=path.join(root, 'images', '4.png'))
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

            url = build_url({'mode': mode, 'page': page, 'quality': '720p', 'query': query})
            li = xbmcgui.ListItem('720p', iconImage=path.join(root, 'images', '5.png'))
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

            url = build_url({'mode': mode, 'page': page, 'quality': '1080p', 'query': query})
            li = xbmcgui.ListItem('1080p', iconImage=path.join(root, 'images', '6.png'))
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

        else:
            # build menu with the anime
            # Setting Content
            xbmcplugin.setContent(addon_handle, 'tvshows')
            if 'None' in query:
                url_search = "%s/list.php?sort=popularity&limit=50&type=All&page=%s&order=asc" \
                             % (url_anime, str(int(page) - 1))
            else:
                url_search = "%s/list.php?sort=popularity&limit=50&type=All&page=0&search=%s" \
                             "&order=asc" % (url_anime, query)
            log('[%s] %s' % (name_addon, url_search))
            browser.open(url_search)
            data = json.loads(browser.content)
            for item in data:
                url = build_url(
                    {'mode': 'anime-ep', 'quality': quality, 'page': page, 'IMDB': item['id']})
                li = xbmcgui.ListItem(label=item['name'], iconImage=item['malimg'],
                                      thumbnailImage=item['malimg'])
                li.setProperty('fanart_image', fanart)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
            if 'None' in query:
                url = build_url({'mode': 'anime', 'quality': quality, 'page': int(page) + 1, 'IMDB': item['id']})
                li = xbmcgui.ListItem('Next Page...')
                li.setProperty('fanart_image', fanart)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    elif mode == 'anime-ep':
        # Setting Content
        xbmcplugin.setContent(addon_handle, 'episodes')
        # build menu with the episodes from anime
        url_search = "%s/anime.php?id=%s" % (url_anime, IMDB)
        log('[%s] %s' % (name_addon, url_search))
        browser.open(url_search)
        data = json.loads(browser.content)
        for episode in data['episodes']:
            if quality in episode['quality']:
                url = link(episode['magnet'])
                li = xbmcgui.ListItem(label=episode['name'],
                                      iconImage=data['malimg'],
                                      thumbnailImage=data['malimg'])
                li.setInfo(type='Video',
                           infoLabels={'title': episode['name'], 'sorttitle': episode['name'],
                                       'episode': getEpisode(episode['name']),
                                       'rating': data['score'],
                                       'genre': data['genres']})
                # Container.SetSortMethod(21)
                li.addStreamInfo('Video', {'width': width(quality), 'height': quality.replace('p', '')})
                li.setProperty('IsPlayable', 'true')
                li.setProperty('fanart_image', fanart)
                xbmcplugin.addSortMethod(handle=addon_handle, sortMethod=xbmcplugin.SORT_METHOD_EPISODE)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

# end of the directory
xbmcplugin.endOfDirectory(addon_handle)
