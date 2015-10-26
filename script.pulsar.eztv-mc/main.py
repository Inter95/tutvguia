from pulsar import provider
import common

# this read the settings
settings = common.Settings()
# create the filters
filters = common.Filtering()

values3 = {'0': 0, 'HDTV': 1,'480p': 1,'DVD': 1,'720p': 2 ,'1080p': 3, '3D': 3, "1440p": 4 ,"2K": 5,"4K": 5} #code_resolution steeve


def search(query):
    return []


def search_episode(info):
    title= ' S%02dE%02d' % (info['season'], info['episode'])
    if settings.time_noti > 0 : provider.notify(message='Searching: ' + info['title'].encode("utf-8").title() +
                                 title +'...', header=None, time=settings.time_noti, image=settings.icon)
    url_search = "%s/show/%s" % (settings.url ,info['imdb_id'])
    provider.log.info(url_search)
    response = provider.GET(url_search)
    results=[]
    if  str(response.data)!='':
        filters.use_TV()
        filters.information()
        items = provider.parse_json(response.data)
        for episode in items['episodes']:
            if (episode['episode']==info['episode'] and episode['season']==info['season']):
                for resolution in episode['torrents']:
                    resASCII =resolution.encode('utf-8')
                    name = resASCII + ' - ' + items['title'] + ' - ' + filters.safe_name(episode['title']) + ' - ' + 'S%02dE%02d'% (info['season'], info['episode'])
                    if filters.included(resASCII, filters.quality_allow) and not filters.included(resASCII, filters.quality_deny):
                        res_val=values3[resASCII]
                        magnet = episode['torrents'][resolution]['url']
                        info_magnet = common.Magnet(magnet)
                        results.append({'name': name + ' - ' + settings.name_provider,
                                        'uri': magnet})
                    else:
                        provider.log.warning(name + ' ***Blocked File by Keyword, Name or Size***')
    return results

def search_movie(info):
    # not info
    return []

# This registers your module for use
provider.register(search, search_movie, search_episode)
