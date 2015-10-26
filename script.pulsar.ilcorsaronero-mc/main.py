# coding: utf-8
from pulsar import provider
from urllib import unquote_plus
import re
import common

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
        data = common.clean_html(data).replace('n/a</td></TR>', "color='#0066CC'>0< ").replace('n/a', " color='#00CC00'>0")
        lname = re.findall('action="http://(.*?)/(.*?)/(.*?)/(.*?)"', data)  # list the name
        name = [item[3].replace('_', ' ') for item in lname]
        size = re.findall("color='#FF6600'>(.*?)<", data)  # list the size
        #seeds = re.findall("color='#00CC00'>(.*?)<", data)  # list the seeds
        #peers = re.findall("color='#0066CC'>(.*?)<", data)  # list the peers
        cont = 0
        results = []
        for cm, infohash in enumerate(re.findall('value="(.*?)"', data)):
            torrent = 'http://torcache.net/torrent/%s.torrent' % infohash
            name[cm] = size[cm] + ' - ' + name[cm] + ' - ' + settings.name_provider #find name in the torrent
            if filters.verify(name[cm],size[cm]):
                    results.append({"name": name[cm], "uri":  torrent, "info_hash": infohash})  # return le torrent
                    cont+= 1
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
    url_search = "%s/argh.php?search=%s" % (settings.url, query)  # change in each provider
    provider.log.info(url_search)
    if browser.open(url_search):
        results = extract_torrents(browser.content)
    else:
        provider.log.error('>>>>>>>%s<<<<<<<' % browser.status)
        provider.notify(message=browser.status, header=None, time=5000, image=settings.icon)
        results = []
    return results


def search_movie(info):
    query = common.translator(info['imdb_id'], 'it', False)  # Just title
    query += ' #MOVIE&FILTER'  #to use movie filters
    return search(query)


def search_episode(info):
    if info['absolute_number'] == 0:
        query = info['title'].encode('utf-8') + ' s%02de%02d' % (info['season'], info['episode'])  # define query
    else:
        query = info['title'].encode('utf-8') + ' %02d' % info['absolute_number']  # define query anime
    query += ' #TV&FILTER'  #to use TV filters
    return search(query)


# This registers your module for use
provider.register(search, search_movie, search_episode)

del settings
del browser
del filters