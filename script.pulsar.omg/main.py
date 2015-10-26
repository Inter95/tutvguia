import unicodedata
import re
from threading import Thread
import Queue
import CommonFunctions
from pulsar import provider

# Addon Script information
__baseUrl__ = provider.ADDON.getSetting("base_url")

# ParseDOM init
common = CommonFunctions
common.plugin = str(sys.argv[0])

tmdbUrl = 'http://api.themoviedb.org/3'
tmdbKey = '8d0e4dca86c779f4157fc2c469c372ca'    # mancuniancol's API Key.
ACTION_SEARCH = "recherche.php"
ACTION_FILMS = "films"
ACTION_SERIES = "series"
CATEGORY_FILMS = "<strong>Films</strong>"
CATEGORY_SERIES = "<strong>Series</strong>"

# Direct link - Use with Threading queue
def directLink(url, q):
    provider.log.debug('directLink URL : %s' % url)
    response = provider.GET(url)
    q.put([{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', response.data)])

# Default Search
def search(query):
    provider.log.debug("QUERY : %s" % query)
    if(query['query']) : 
        query = query['query']
    query_normalize = unicodedata.normalize('NFKD',query)
    query = ''.join(c for c in query_normalize if (not unicodedata.combining(c)))
    url = "%s/%s?query=%s" % (__baseUrl__, ACTION_SEARCH, provider.quote_plus(query))
    provider.log.info("SEARCH : %s" % url)
    response = provider.GET(url)
    if response.geturl() is not url:
        # Redirection 30x followed to individual page - Return the magnet link
        provider.log.info('Redirection 30x followed to individual page - Return the magnet link')
        return provider.extract_magnets(response.data)
        #return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', response.data)]
    else:
        # Multiple torrent page - Parse page to get individual page
        provider.log.info('Multiple torrent page - Parsing')
        # Parse the table result
        table = common.parseDOM(response.data, 'table', attrs = { "class": "table_corps" })
        liens = common.parseDOM(table, 'a', attrs = { "class": "torrent" }, ret = 'href')
        provider.log.debug('liens : %s' % liens)
        threads = []
        magnets = []
        q = Queue.Queue()

        # Call each individual page in parallel
        for lien in liens :
            thread = Thread(target=directLink, args = ('%s%s' % (__baseUrl__, lien), q))
            thread.start()
            threads.append(thread)

        # And get all the results
        for t in threads :
            t.join()
        while not q.empty():
            magnets.append(q.get()[0])

        provider.log.info('Magnets List : %s' % magnets)
        return magnets

def search_episode(episode): 
    provider.log.debug("Search episode : name %(title)s, season %(season)02d, episode %(episode)02d" % episode)
    # Pulsar 0.2 doesn't work well with foreing title.  Get the FRENCH title from TMDB
    provider.log.debug('Get FRENCH title from TMDB for %s' % episode['imdb_id'])
    response = provider.GET("%s/find/%s?api_key=%s&language=fr&external_source=imdb_id" % (tmdbUrl, episode['imdb_id'], tmdbKey))
    provider.log.debug(response)
    if response != (None, None):
        name_normalize = unicodedata.normalize('NFKD',response.json()['tv_results'][0]['name'])
        episode['title'] = ''.join(c for c in name_normalize if (not unicodedata.combining(c)))
        provider.log.info('FRENCH title :  %s' % episode['title'])
    else :
        provider.log.error('Error when calling TMDB. Use Pulsar movie data.')
    resp = provider.GET("%s/%s?ajax&query=%s" % (__baseUrl__, ACTION_SEARCH, provider.quote_plus(episode['title'])))
    for result in resp.json():
        if result["category"] == CATEGORY_SERIES :
            # Get show's individual url
            url = "%s/%s?query=%s" % (__baseUrl__, ACTION_SEARCH, provider.quote_plus(result["label"]))
            if episode['season'] is not 1 :
                # Get model url for requested season
                provider.log.debug('Season URL: %s' % url)
                response = provider.HEAD(url)
                # Replace "season" data in url.  Ex.  :
                # http://www.omgtorrent.com/series/true-blood_saison_7_53.html
                url = response.geturl().replace("_1_","_%s_" % episode['season'])
            # Parse season specific page
            return parse_season(url,episode['episode'])

def search_movie(movie):
    # Pulsar 0.2 doesn't work well with foreing title.  Get the FRENCH title from TMDB
    provider.log.debug('Get FRENCH title from TMDB for %s' % movie['imdb_id'])
    response = provider.GET("%s/movie/%s?api_key=%s&language=fr&external_source=imdb_id&append_to_response=alternative_titles" % (tmdbUrl, movie['imdb_id'], tmdbKey))
    if response != (None, None):
        title_normalize = unicodedata.normalize('NFKD',response.json()['title'])
        movie['title'] = ''.join(c for c in title_normalize if (not unicodedata.combining(c)))
        provider.log.info('FRENCH title :  %s' % movie['title'])
    else :
        provider.log.error('Error when calling TMDB. Use Pulsar movie data.')
    resp = provider.GET("%s/%s?ajax&query=%s" % (__baseUrl__, ACTION_SEARCH, provider.quote_plus(movie['title'])))
    for result in resp.json():
        if result["category"] == CATEGORY_FILMS:
            # Get movie's page
            return search({'query':result["label"]})
    # If no result
    return []

def parse_season(url, episode):
    result = []
    response = provider.GET(url)
    # Get torrent (if any) from table - 1 line per episode
    table = common.parseDOM(response.data, 'table', attrs = { "class": "table_corps" })
    liens = common.parseDOM(table, 'tr', attrs = { "class": "bords" })
    provider.log.info(liens)
    if liens :
        # Get the first known episode
        start = int(common.parseDOM(liens[0], 'td')[0].rstrip('.'))
        try:
            return [{"uri": '%s%s' % (__baseUrl__, torrent) for torrent in common.parseDOM(liens[episode - start], 'a', ret = 'href')}]
        except IndexError:
            # Pulsar show episode that aren't published yet, so not present in OMG results.
            # If this future episode is selected, return Notification instead of IndexError
            provider.notify("Episode actuellement indisponible.")
    return result

# Registers the module in Pulsar
provider.register(search, search_movie, search_episode)
