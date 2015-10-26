import re

import common

from pulsar import provider


# this read the settings
settings = common.Settings()
# create the filters
filters = common.Filtering()

values3 = {'ALL': 0, 'HDTV': 1, '480p': 1, 'DVD': 1, '720p': 2, '1080p': 3, '3D': 3, "1440p": 4, "2K": 5,
           "4K": 5}  # code_resolution steeve


def extract_magnets_json(data):
    results = []
    items = provider.parse_json(data)
    if items['data']['movie_count'] > 0:
        filters.information()
        for movie in items['data']['movies'][0]['torrents']:
            resASCII = movie['quality'].encode('utf-8')
            name = movie['size'] + ' - ' + items['data']['movies'][0][
                'title'] + ' - ' + resASCII + ' - ' + settings.name_provider
            filters.title = items['data']['movies'][0]['title']
            if filters.verify(name, movie['size']):
                results.append({'name': name, 'uri': movie['url'], 'info_hash': movie['hash']})
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
    url_search = "%s/v2/list_movies.json?query_term=%s" % (settings.url, info['imdb_id'])
    provider.log.info(url_search)
    response = provider.GET(url_search)
    return extract_magnets_json(response.data)


def search_episode(info):
    # just movies site
    return []

# This registers your module for use
provider.register(search, search_movie, search_episode)
