import re

import common

from pulsar import provider


# this read the settings
settings = common.Settings()
# create the filters
filters = common.Filtering()


# function to findID
def findID(query="", year=""):
    response = provider.GET("%s/search?q=%s" % (settings.url, query))
    answer = provider.parse_json(response.data)
    result = "0"
    if len(answer) > 0:
        for item in answer["data"]:
            result = item["id"]
            if item["year"] == year:
                break
    return result


def extract_magnets_json(data):
    results = []
    items = provider.parse_json(data)
    if len(items['sources']) > 0:
        filters.information()
        for item in items['sources']:
            resASCII = item['def']
            name = items['name'] + filters.title + ' - ' + resASCII + 'p - ' + settings.name_provider
            filters.title = items['name']
            if filters.verify(name, None):
                results.append({'name': name, 'uri': item['url']})
            else:
                provider.log.warning(filters.reason)
    return results


def search(query):
    return []


def search_movie(info):
    filters.use_movie()
    if settings.time_noti > 0: provider.notify(message='Searching: ' + info['title'].title().encode("utf-8") + '...',
                                               header=None,
                                               time=settings.time_noti, image=settings.icon)
    id = findID(info["title"], info["year"])
    if id == "0":
        return []
    else:
        url_search = "%s/movies/%s" % (settings.url, id)
        provider.log.info(url_search)
        response = provider.GET(url_search)
        return extract_magnets_json(response.data)


def search_episode(info):
    filters.use_TV()
    filters.title = ' S%02dE%02d' % (info['season'], info['episode'])
    if settings.time_noti > 0: provider.notify(message='Searching: ' + info['title'].encode("utf-8").title() +
                                                       filters.title + '...', header=None, time=settings.time_noti,
                                               image=settings.icon)
    id = findID(info["title"])
    if id == "0":
        return []
    else:
        url_search = "%s/tvshows/%s" % (settings.url, id)
        provider.log.info(url_search)
        response = provider.GET(url_search)
        try:
            id = provider.parse_json(response.data)["seasons"][info['season'] - 1]['episodes'][info['episode'] - 1]['id']
            url_search = "%s/episodes/%s" % (settings.url, id)
            provider.log.info(url_search)
            response = provider.GET(url_search)
            return extract_magnets_json(response.data)
        except:
            provider.log.info("No episode available")
            return []

# This registers your module for use
provider.register(search, search_movie, search_episode)
