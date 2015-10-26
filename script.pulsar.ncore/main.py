from pulsar import provider
from urllib import unquote_plus

import re

# this read the settings
url = provider.ADDON.getSetting('url_address')
icon = provider.ADDON.getAddonInfo('icon')
name_provider = provider.ADDON.getAddonInfo('name') # gets name
language = provider.ADDON.getSetting('language')

movie_min_size = float(provider.ADDON.getSetting('movie_min_size'))
movie_max_size = float(provider.ADDON.getSetting('movie_max_size'))
TV_min_size = float(provider.ADDON.getSetting('TV_min_size'))
TV_max_size = float(provider.ADDON.getSetting('TV_max_size'))
max_magnets = int(provider.ADDON.getSetting('max_magnets'))  #max_magnets

#premium account
username = provider.ADDON.getSetting('username') # username
password = provider.ADDON.getSetting('password') # passsword

# open premium account
def login():
  import requests
  result = False
  if username!="":
    payload = {'nev': username, 'pass': password, 'ne_leptessen_ki' : True}
    with requests.Session() as c:
      c.post(url + '/login.php',data = payload)
      response = c.get(url + '/user/account/')
      #print response.status_code
    result = True if 'My account details' in response.content else False
  return result

account = login() # login

#define quality variables
quality_allow = ['Xvid/HU', 'Xvid/EN', 'DVDR/HU', 'DVDR/EN','DVD9/HU', 'DVD9/EN' , 'HD/HU', 'HD/EN']
quality_deny = []
max_size = 10.00 #10 it is not limit
min_size = 0.00

#quality_movie
movie_q1 = provider.ADDON.getSetting('movie_q1') #480p
movie_q2 = provider.ADDON.getSetting('movie_q2') #DVD
movie_q3 = provider.ADDON.getSetting('movie_q3') #HDTV
movie_q4 = provider.ADDON.getSetting('movie_q4') #720p
movie_q5 = provider.ADDON.getSetting('movie_q5') #1080p
movie_q6 = provider.ADDON.getSetting('movie_q6') #3D
movie_q7 = provider.ADDON.getSetting('movie_q7') #WEB
movie_q8 = provider.ADDON.getSetting('movie_q8') #Bluray
movie_q9 = provider.ADDON.getSetting('movie_q9') #BRRip
movie_q10 = provider.ADDON.getSetting('movie_q10') #HDRip
movie_q11 = provider.ADDON.getSetting('movie_q11') #MicroHD
movie_q12 = provider.ADDON.getSetting('movie_q12') #x264
movie_q13 = provider.ADDON.getSetting('movie_q13') #AC3
movie_q14 = provider.ADDON.getSetting('movie_q14') #AAC
movie_q15 = provider.ADDON.getSetting('movie_q15') #HEVC
movie_q16 = provider.ADDON.getSetting('movie_q16') #CAM
movie_q17 = provider.ADDON.getSetting('movie_q17') #TeleSync
movie_q18 = provider.ADDON.getSetting('movie_q18') #DTS
movie_allow = re.split('\s',movie_key_allowed)
movie_deny = re.split('\s',movie_key_denied)
movie_allow.append('480p') if movie_q1 == 'true' else movie_deny.append('480p')
movie_allow.append('DVD') if movie_q2 == 'true' else movie_deny.append('DVD')
movie_allow.append('HDTV') if movie_q3 == 'true' else movie_deny.append('HDTV')
movie_allow.append('720p') if movie_q4 == 'true' else movie_deny.append('720p')
if movie_q5 == 'true':
  movie_allow.append('1080p')
else:
  if movie_q6 == 'false': movie_deny.append('1080p')
movie_allow.append('3D') if movie_q6 == 'true' else movie_deny.append('3D')
movie_allow.append('WEB') if movie_q7 == 'true' else movie_deny.append('WEB')
movie_allow.append('Bluray') if movie_q8 == 'true' else movie_deny.append('Bluray')
movie_allow.append('BRRip') if movie_q9 == 'true' else movie_deny.append('BRRip')
movie_allow.append('HDRip') if movie_q10 == 'true' else movie_deny.append('HDRip')
movie_allow.append('MicroHD') if movie_q11 == 'true' else movie_deny.append('MicroHD')
movie_allow.append('x264') if movie_q12 == 'true' else movie_deny.append('x264')
movie_allow.append('AC3') if movie_q13 == 'true' else movie_deny.append('AC3')
movie_allow.append('AAC') if movie_q14 == 'true' else movie_deny.append('AAC')
movie_allow.append('HEVC') if movie_q15 == 'true' else movie_deny.append('HEVC')
movie_allow.append('CAM') if movie_q16 == 'true' else movie_deny.append('CAM')
movie_allow.append('TeleSync') if movie_q17 == 'true' else movie_deny.extend(['TeleSync', ' TS '])
movie_allow.append('DTS') if movie_q18 == 'true' else movie_deny.append('DTS')
if '' in movie_allow: movie_allow.remove('')
if '' in movie_deny: movie_deny.remove('')

#quality_TV
TV_q1 = provider.ADDON.getSetting('TV_q1') #480p
TV_q2 = provider.ADDON.getSetting('TV_q2') #DVD
TV_q3 = provider.ADDON.getSetting('TV_q3') #HDTV
TV_q4 = provider.ADDON.getSetting('TV_q4') #720p
TV_q5 = provider.ADDON.getSetting('TV_q5') #1080p
TV_q7 = provider.ADDON.getSetting('TV_q7') #WEB
TV_q8 = provider.ADDON.getSetting('TV_q8') #Bluray
TV_q9 = provider.ADDON.getSetting('TV_q9') #BRRip
TV_q10 = provider.ADDON.getSetting('TV_q10') #HDRip
TV_q12 = provider.ADDON.getSetting('TV_q12') #x264
TV_q15 = provider.ADDON.getSetting('TV_q15') #HEVC
TV_allow = re.split('\s',TV_key_allowed)
TV_deny = re.split('\s',TV_key_denied)
TV_allow.append('480p') if TV_q1 == 'true' else TV_deny.append('480p')
TV_allow.append('DVD') if TV_q2 == 'true' else TV_deny.append('DVD')
TV_allow.append('HDTV') if TV_q3 == 'true' else TV_deny.append('HDTV')
TV_allow.append('720p') if TV_q4 == 'true' else TV_deny.append('720p')
TV_allow.append('1080p') if TV_q5 == 'true' else TV_deny.append('1080p')
TV_allow.append('WEB') if TV_q7 == 'true' else TV_deny.append('WEB')
TV_allow.append('Bluray') if TV_q8 == 'true' else TV_deny.append('Bluray')
TV_allow.append('BRRip') if TV_q9 == 'true' else TV_deny.append('BRRip')
TV_allow.append('HDRip') if TV_q10 == 'true' else TV_deny.append('HDRip')
TV_allow.append('x264') if TV_q12 == 'true' else TV_deny.append('x264')
TV_allow.append('HEVC') if TV_q15 == 'true' else TV_deny.append('HEVC')
if '' in TV_allow: TV_allow.remove('')
if '' in TV_deny: TV_deny.remove('')

# validate keywords
def included(value, keys):
  value = value.replace('-',' ')
  res = False
  for item in keys:
    if item.upper() in value.upper():
      res = True
      break
  return res

# validate size
def size_clearance(size):
  global max_size
  max_size = 100 if max_size == 10 else max_size
  res = False
  value = float(re.split('\s', size.replace(',',''))[0])
  value *= 0.001 if 'M' in size else 1
  if min_size <= value and value <= max_size:
    res = True
  return res

# clean_html
def clean_html(data):
  lines = re.findall('<!--(.*?)-->',data)
  for line in lines:
    data = data.replace(line,'')
  return data

# using function from Steeve to add Provider's name and search torrent
def extract_torrents(data):
  try:
    data = clean_html(data)
    value_search = 'total <b style="color: #ff0000;">0</b> torrents found on your search query' in data
    size = re.findall('</span></td><td>(.*?)B</td>', data) # list the size
    provider.log.info('Keywords allowed: ' + str(quality_allow))
    provider.log.info('Keywords denied: ' + str(quality_deny))
    provider.log.info('min Size: ' + str(min_size) + ' GB')
    provider.log.info('max Size: ' + str(max_size)  + ' GB' if max_size != 10 else 'max Size: MAX')
    cont = 0
    for cm, torrent in  enumerate(re.findall(r'/torrent_download(.*?).torrent', data)):
      name = torrent[len(re.search("/*[0-9]*/",torrent).group()):len(torrent)]
      name = unquote_plus(name) + ' - ' + size[cm].replace('&nbsp;',' ') + 'B' + ' - ' + name_provider #find name in the torrent
      torrent = url + '/download' + torrent + '.torrent' # torrent to send to Pulsar
      if included(name, quality_allow) and not included(name, quality_deny) and not value_search and size_clearance(size[cm].replace('&nbsp;',' ')):
        yield {"name": name, "uri": torrent}
        cont+= 1
      else:
        provider.log.warning(name + '   ***Not Included for keyword filtering or size***')
      if cont == max_magnets: #limit torrents
        break
    provider.log.info('>>>>>>' + str(cont) + ' torrents sent to Pulsar<<<<<<<')
  except:
    provider.log.error('>>>>>>>ERROR parsing data<<<<<<<')

def search(info):
  query = info['query'] + ' ' + extra
  provider.notify(message = "Searching: " + query.title() + '...', header = None, time = 1500, image=icon)
  query = provider.quote_plus(query)
  url_search = "%s/search/?search=%s&srt=seeds&order=desc" % (url,query)
  provider.log.info(url_search)
  response = provider.GET(url_search)
  if response == (None, None):
    provider.log.error('404 Page not found')
    return []
  else:
    return extract_torrents(response.data)

def search_movie(info):
  global quality_allow, quality_deny, min_size, max_size
  quality_allow = movie_allow
  quality_deny = movie_deny
  min_size = movie_min_size
  max_size = movie_max_size
  query = info['title'] + ' ' + str(info['year']) #define query
  return search({'query': query})

def search_episode(info):
  global quality_allow, quality_deny, min_size, max_size
  quality_allow = TV_allow
  quality_deny = TV_deny
  min_size = TV_min_size
  max_size = TV_max_size
  query =  info['title'].replace(' s ','s ') + ' S%02dE%02d '% (info['season'],info['episode'])  #define query
  return search({'query': query})

# This registers your module for use
provider.register(search, search_movie, search_episode)
