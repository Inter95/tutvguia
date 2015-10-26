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
        data = data[data.find('Search in :'):]
        data = data.replace('<strong>', '').replace('</strong>', '').replace('\n', '').replace('\t', '').replace(
            '<font color="#008000">', '').replace('<font color="#000080">', '').replace('</font>', '')
        rows = re.findall('<td class="trow" align="center">(.*?)</td>', data, re.S)
        size = rows[3::6]
        seeds = rows[4::6]
        peers = rows[5::6]
        cont = 0
        results = []
        for cm, line in enumerate(re.findall('/download/(.*?)\.torrent', data)):
            torrent = '%s/torrent_download/%s.torrent' % (settings.url, line.replace(' ', '+'))
            name = size[cm] + ' - ' + line.split('/')[-1].split('_')[0] + ' - ' + settings.name_provider
            if filters.verify(name, size[cm]):
                results.append({"name": name, "uri": torrent,
                                "size": common.size_int(size[cm]),
                                "seeds": int(seeds[cm]), "peers": int(peers[cm]),
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
        results = []


def search(query):
    query += ' ' + settings.extra  # add the extra information
    query = filters.type_filtering(query, '-')  # check type filter and set-up filters.title
    url_search = "%s/en/search/%s?order=seeders&by=down" % (settings.url, query)  # change in each provider
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
