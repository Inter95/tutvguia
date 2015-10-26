# coding: utf-8
from pulsar import provider
import re
import common
from itertools import chain

# this read the settings
settings = common.Settings()
# define the browser
browser = common.Browser()
# create the filters
filters = common.Filtering()
# special settings
values2 = {"ALL": '1_0', "English translations": '1_37', "Non English translations": '1_38',
           "Raw": '1_11'}  # read category
category = values2[provider.ADDON.getSetting('category')]


# using function from Steeve to add Provider's name and search torrent
def extract_torrents(data):
    try:
        filters.information()  # print filters settings
        data = common.clean_html(data)
        name = re.findall(r'/.page=view&#..;tid=(.*?)>(.*?)</a></td>',data) # find all names
        size = re.findall(r'<td class="tlistsize">(.*?)</td>',data) # find all sizes
        cont = 0
        for cm, torrent in enumerate(re.findall(r'/.page=download&#..;tid=(.*?)"', data)):
            #find name in the torrent
            if re.search(r'Searching torrents',data) is not None:
                if filters.verify(name[cm][1], size[cm]):
                        yield { "name": size[cm] + ' - ' + name[cm][1] + ' - ' + settings.name_provider, "uri": settings.url + '/?page=download&tid=' + torrent}
                        cont += 1
                else:
                    provider.log.warning(filters.reason)
                if cont == settings.max_magnets:  # limit magnets
                    break
        provider.log.info('>>>>>>' + str(cont) + ' torrents sent to Pulsar<<<<<<<')
    except:
        provider.log.error('>>>>>>>ERROR parsing data<<<<<<<')
        provider.notify(message='ERROR parsing data', header=None, time=5000, image=settings.icon)


def get_titles(title, tvdb_id):
    url_tvdb = "http://www.thetvdb.com/api/GetSeries.php?seriesname=%s" % provider.quote_plus(title)
    provider.log.info(url_tvdb)
    if browser.open(url_tvdb):
        pat = re.compile('<seriesid>%d</seriesid>.*?<AliasNames>(.*?)</AliasNames>' % tvdb_id, re.I | re.S)
        show = pat.search(browser.content) # find all aliases
        if show:
            aliases = show.group(1).strip()
            provider.log.info("Aliases: " + aliases)
            return [ title ] + aliases.split('|')
    return [ title ]		


def search(query):
    query += ' ' + settings.extra  # add the extra information
    query = filters.type_filtering(query, '+')  # check type filter and set-up filters.title
    url_search = "%s/?page=search&cats=%s&term=%s&sort=2" % (settings.url, category, query)  # change in each provider
    provider.log.info(url_search)
    if browser.open(url_search):
        results = extract_torrents(browser.content)
    else:
        provider.log.error('>>>>>>>%s<<<<<<<' % browser.status)
        provider.notify(message=browser.status, header=None, time=5000, image=settings.icon)
        results = []
    return results


def search_movie(info):
    return []


def search_episode(info):
    if info['absolute_number'] == 0:
        return []
    else:
        iters = []
        titles = get_titles(info['title'].encode("utf-8"), info['tvdb_id'])
        for title in titles:
            query = title + ' %02d' % info['absolute_number']
            iters.append(search(query+ ' #TV&FILTER'))
        return chain.from_iterable(iters)

# This registers your module for use
provider.register(search, search_movie, search_episode)