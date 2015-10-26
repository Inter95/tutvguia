# coding: utf-8
from urllib import unquote_plus
import re

import common

from pulsar import provider


# this read the settings
settings = common.Settings()
# define the browser
browser = common.Browser()
# create the filters
filters = common.Filtering()


# using function from Steeve to add Provider's name and search torrent
def extract_torrents(data):
    try:
        cont = 0
        results = []
        for cm, (ntorrent, name) in enumerate(re.findall('/torrent/(.*?)/(.*?)/', data)):
            torrent = '%s/download.php?id=%s' % (settings.url, ntorrent)
            name = name.replace('-', ' ').title() + ' - ' + settings.name_provider  # find name in the torrent
            if filters.verify(name, None):
                results.append({"name": name, "uri": torrent, "seeds": 10000, "peers": 5000})  # return le torrent
                cont += 1
            else:
                provider.log.warning(filters.reason)
            if cont == settings.max_magnets:  # limit magnets
                break
        provider.log.info('>>>>>>' + str(cont) + ' torrents sent to Pulsar<<<<<<<')
        return results
    except:
        provider.log.error('>>>>>>>ERROR parsing data<<<<<<<')
        provider.notify(message='ERROR parsing data', header=None, time=5000, image=settings.icon)
        return []


def search(query):
    global filters
    filters.title = query  # to do filtering by name
    if settings.time_noti > 0: provider.notify(message="Searching: " + query.title() + '...', header=None,
                                               time=settings.time_noti, image=settings.icon)
    query = provider.quote_plus(query)
    url_search = "%s/buscar.php?busqueda=%s" % (settings.url, query)
    provider.log.info(url_search)
    if browser.open(url_search):
        results = extract_torrents(browser.content)
    else:
        provider.log.error('>>>>>>>%s<<<<<<<' % browser.status)
        provider.notify(message=browser.status, header=None, time=5000, image=settings.icon)
        results = []
    return results


def search_movie(info):
    query = common.translator(info['imdb_id'], 'es', False)
    return search(query)


def search_episode(info):
    info['title'] = common.exception(info['title'])
    if info['absolute_number'] == 0:
        query = info['title'] + ' %sx%02d' % (info['season'], info['episode'])  # define query
    else:
        query = info['title'] + ' %02d' % info['absolute_number']  # define query anime
    query = query.encode('utf-8')
    filters.title = query
    if settings.time_noti > 0: provider.notify(message="Searching: " + query.title() + '...', header=None,
                                               time=settings.time_noti, image=settings.icon)
    query = provider.quote_plus(query)
    url_search = "%s/buscar.php?busqueda=%s" % (settings.url, query)
    provider.log.info(url_search)
    if browser.open(url_search):
        results = []
        data = browser.content
        search_serie = re.search('/series/(.*?)/" title', data)
        if search_serie is not None:
            url_search = '%s/series/%s/' % (settings.url, search_serie.group(1))
            browser.open(url_search)
            data = browser.content
            cont = 0
            lname = re.search(filters.title.replace(' ', '.') + '(.*?).torrent', data, re.IGNORECASE)
            if lname is not None:
                torrent = '%s/torrents_tor/%s' % (settings.url, lname.group())
                name = lname.group().replace('.torrent', '') + ' S%02dE%02d' % (
                info['season'], info['episode']) + ' - ' + settings.name_provider  # find name in the torrent
                results.append({"name": name, "uri": torrent, "seeds": 10000, "peers": 5000})  # return le torrent
                cont = 1
            provider.log.info('>>>>>> ' + str(cont) + ' torrents sent to Pulsar<<<<<<<')
    else:
        provider.log.error('>>>>>>>%s<<<<<<<' % browser.status)
        provider.notify(message=browser.status, header=None, time=5000, image=settings.icon)
    return results

# This registers your module for use
provider.register(search, search_movie, search_episode)
