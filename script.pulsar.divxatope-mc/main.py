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
        filters.information()  # print filters settings
        data = common.clean_html(data)
        size = re.findall(r'o</strong> .(.*?). &nbsp', data)  # find all sizes
        cont = 0
        results = []
        for cm, torrent in enumerate(re.findall(r'/descargar/(.*?)"', data)):
            sname = re.search("_(.*?).html", torrent)
            if sname is None:
                name = torrent
            else:
                name = sname.group(1)
            name = size[cm] + ' MB - ' + name.replace('-', ' ').title() + settings.name_provider
            torrent = settings.url + '/torrent/' + torrent  # create torrent to send Pulsar
            if filters.verify(name, size[cm] + ' MB'):
                results.append({"name": name, "uri": torrent})  # return le torrent
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
    query = common.normalize(query)
    filters.title = query  # to do filtering by name
    query += ' ' + settings.extra
    if settings.time_noti > 0: provider.notify(message="Searching: " + query.title() + '...', header=None,
                                               time=settings.time_noti, image=settings.icon)
    query = provider.quote_plus(query)
    url_search = "%s/newtemp/include/ajax/ajax.search.php?search=%s" % (
    settings.url, query.replace(' ', '%20'))  # change in each provider
    provider.log.info(url_search)
    if browser.open(url_search):
        results = extract_torrents(browser.content)
    else:
        provider.log.error('>>>>>>>%s<<<<<<<' % browser.status)
        provider.notify(message=browser.status, header=None, time=5000, image=settings.icon)
        results = []
    return results


def search(query):
    query += ' ' + settings.extra  # add the extra information
    query = filters.type_filtering(query, '%20')  # check type filter and set-up filters.title
    url_search = "%s/newtemp/include/ajax/ajax.search.php?search=%s" % (settings.url, query)  # change in each provider
    provider.log.info(url_search)
    if browser.open(url_search):
        results = extract_torrents(browser.content)
    else:
        provider.log.error('>>>>>>>%s<<<<<<<' % browser.status)
        provider.notify(message=browser.status, header=None, time=5000, image=settings.icon)
        results = []
    return results


def search_movie(info):
    query = common.translator(info['imdb_id'], 'es', False)  # Just title
    query += ' #MOVIE&FILTER'  # to use movie filters
    return search(query)


def search_episode(info):
    return []

# This registers your module for use
provider.register(search, search_movie, search_episode)

del settings
del browser
del filters
