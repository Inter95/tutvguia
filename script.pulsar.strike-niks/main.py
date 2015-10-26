from pulsar import provider


icon = provider.ADDON.getAddonInfo('icon')
notificationTime = int(provider.get_setting('time_noti'))

def search(query):
	query = query.replace(' ', '%20')
	url_search = "https://getstrike.net/api/v2/torrents/search/?phrase=%s" % (query)
	provider.log.info(url_search)
	response = provider.GET(url_search)
	results=[]
	if response != (None, None):
		items = provider.parse_json(response.data)
		nbrTorrents = items['results']
		for torrent in range(0, nbrTorrents):
			hash = items['torrents'][torrent]['torrent_hash']
			name = items['torrents'][torrent]['torrent_title']
			magnet = items['torrents'][torrent]['magnet_uri']
			results.append({'name': name, 'uri': magnet, 'info_hash': hash})
	return results
		
def search_episode(info):
	title = info['title'].encode('utf-8') + ' S%02dE%02d' % (info['season'],info['episode'])
	if notificationTime > 0:
		provider.notify(message='Searching: ' + title +'...', header=None, time=notificationTime, image=icon)
	return search(title)

def search_movie(info):
	title = info['title'].encode('utf-8') + ' %s' % (info['year'])
	if notificationTime > 0:
		provider.notify(message='Searching: ' + title +'...', header=None, time=notificationTime, image=icon)
	return search(title)

#This registers your module for use
provider.register(search, search_movie, search_episode)