import time
from pulsar import provider

start = time.time()
def search(query):
    response = provider.GET("https://yts.to/api/listimdb.json?imdb_id=%s" % provider.quote_plus(query))
    print 'YIFI - Time: ' + str((time.time() - start))
    return provider.extract_magnets(response.data)

def search_movie(movie):
    return search("%(imdb_id)s" % movie)

def search_episode(episode):
    return []
    
provider.register(search, search_movie, search_episode)
