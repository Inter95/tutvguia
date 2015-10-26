# coding: utf-8
# https://github.com/steeve/plugin.video.pulsar/blob/master/resources/site-packages/pulsar/provider.py
from pulsar import provider
import re

CATEGORY_MOVIES = "1"
CATEGORY_HDMOVIES = "2"
CATEGORY_EPISODES = "3"

# Raw search
# query is always a string
def search(query, category=""):
  
  resp = provider.GET("http://www.tankafetast.com/search/", params={
    "search": query,
    "category": category
  })
  
  pmagnet = re.compile(r'magnet:\?[^\'"\s<>\[\]]+')
  ptorrent = re.compile(r'http[s]?://.*\.torrent')
  sections = (resp.data.split("<td"))
  results = []
 
  # a section (<td) could contain a magnet link, torrent or both
  # prioritize magnets
  for section in sections:
    magnet = pmagnet.search(section)
    if magnet == None:
      torrent = ptorrent.search(section)
      if torrent != None:
        results.append({"uri": torrent.group(0)})
        provider.log.info("Found torrent: " + torrent.group(0))
    else:
      provider.log.info("Found magnet: " + magnet.group(0))
      results.append({"uri": magnet.group(0)})
      
  return results
  
def search_episode(episode):
  return search("%(title)s S%(season)02dE%(episode)02d" % episode, CATEGORY_EPISODES)

def search_movie(movie):
  return search("%(title)s %(year)d" % movie, CATEGORY_MOVIES)

provider.register(search, search_movie, search_episode)