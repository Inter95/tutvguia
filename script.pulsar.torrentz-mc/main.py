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
        data = data[data.find('peers'):].replace('<b>', '').replace('</b>', '').replace('class="pe">Pending',
                                                                                        'class="s">0 MB')  # short
                                                                                        # the result
        size = re.findall('class="s">(.*?)</span>', data)  # list the size
        seeds = re.findall('class="u">(.*?)</span>', data)  # list the seeds
        peers = re.findall('class="d">(.*?)</span>', data)  # list the seeds
        cont = 0
        results = []
        for cm, (infohash, name) in enumerate(re.findall('<dl><dt><a href="/(.*?)">(.*?)<', data)):
            torrent = 'magnet:?xt=urn:btih:%s' % infohash
            name = size[cm] + ' - ' + name.replace('-', ' ').title() + ' - ' + settings.name_provider  # find name in
            #  the torrent
            if filters.verify(name, size[cm]):
                results.append({"name": name, "uri": torrent, "info_hash": infohash,
                                "size": common.size_int(size[cm]), "seeds": int(seeds[cm].replace(',', '')),
                                "peers": int(peers[cm].replace(',', '')),
                                "language": settings.language})  # return le torrent
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
    query += ' ' + settings.extra  # add the extra information
    query = filters.type_filtering(query, '+')  # check type filter and set-up filters.title
    url_search = "%s/search?f=%s" % (settings.url, query)
    provider.log.info(url_search)
    if browser.open(url_search):
        results = extract_torrents(browser.content)
    else:
        provider.log.error('>>>>>>>%s<<<<<<<' % browser.status)
        provider.notify(message=browser.status, header=None, time=5000, image=settings.icon)
        results = []
    return results


def search_movie(info):
    if settings.language == 'en':  # Title in english
        query = info['title'].encode('utf-8')  # convert from unicode
        if len(info['title']) == len(query):  # it is a english title
            query += ' ' + str(info['year'])  # Title + year
        else:
            query = common.IMDB_title(info['imdb_id'])  # Title + year
    else:  # Title en foreign language
        query = common.translator(info['imdb_id'], settings.language)  # Just title
    query += ' #MOVIE&FILTER'  # to use movie filters
    return search(query)


def search_episode(info):
    if info['absolute_number'] == 0:
        query = info['title'].encode('utf-8') + ' s%02de%02d' % (info['season'], info['episode'])  # define query
    else:
        query = info['title'].encode('utf-8') + ' %02d' % info['absolute_number']  # define query anime
    query += ' #TV&FILTER'  # to use TV filters
    return search(query)

# This registers your module for use
provider.register(search, search_movie, search_episode)

del settings
del browser
del filters
