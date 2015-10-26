import sys
import os
import urllib2
import hashlib
import time
import re
import xbmcaddon
import xbmcplugin
from pulsar import provider
import shelve
import thread

begin = time.time()
__addon__ = xbmcaddon.Addon(str(sys.argv[0]))
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
sys.path.append(os.path.join(addon_dir, 'resources', 'lib' ))
from fuzzywuzzy import fuzz

base_url = __addon__.getSetting("base_url")
use_fuzzy = __addon__.getSetting("use_fuzzy")
fuzzy_threshold = __addon__.getSetting("fuzzy_threshold")

PREFIX_LOG = 'EZTV - '
HEADERS = { 'Referer' : base_url,
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
}
cache_prefix = xbmc.translatePath('special://temp') + __addon__.getAddonInfo('name').lower().replace(' ','_') + '_cache_'

def search_episode(ep):
    name = ep['title']
    season = ep['season']
    episode = ep['episode']
    show_list = get_cached_func('get_eztv_shows')
    episode_string = '(?:S' + str(season).zfill(2) + 'E' + str(episode).zfill(2) + '|' + str(season) + 'x' + str(episode).zfill(2) + ')'
    print PREFIX_LOG + 'Seaching for: ' + name + ' (S' + str(season).zfill(2) + 'E' + str(episode).zfill(2) + ')'
    result = []
    show_found = ''
    for item in show_list:
        if ((name == item['name1']) | (name == item['name2']) | (name == item['name3']) | (name == item['name4'])):
            url_show = base_url + '/shows/' + item['id'] + '/'
            mag_list = get_cached_func('get_magnet_list' ,(url_show,))
            result = search_in_list(episode_string, mag_list)
            show_found = name
            break
    if(show_found):
        print PREFIX_LOG + 'Show found: ' + show_found
    else:
        print PREFIX_LOG + 'Show found: none'
        if(use_fuzzy):
            print PREFIX_LOG + 'Trying Fuzzy'
            fuzy_list = []
            for item in show_list:
                fuzy_list.append({'score': int(fuzz.ratio(name,item['name1'])), 'id': item['id'], 'name': item['name1']})
                fuzy_list.append({'score': int(fuzz.ratio(name,item['name2'])), 'id': item['id'], 'name': item['name2']})
                fuzy_list.append({'score': int(fuzz.ratio(name,item['name3'])), 'id': item['id'], 'name': item['name3']})
                fuzy_list.append({'score': int(fuzz.ratio(name,item['name4'])), 'id': item['id'], 'name': item['name4']})
            def getKey(obj):
                return obj['score']
            sorted_showlist = sorted(fuzy_list, key=getKey)
            item = sorted_showlist[-1]
            if(item['score'] >= fuzzy_threshold ):
                print PREFIX_LOG + 'Fuzzy found: ' + item['name'] + ' (score: ' + str(item['score']) + ')'
                url_show = base_url + '/shows/' + item['id'] + '/'
                mag_list = get_cached_func('get_magnet_list' ,(url_show,))
                result = search_in_list(episode_string, mag_list)
            else:
                print PREFIX_LOG + 'Fuzzy ignored: ' + sorted_showlist[-1]['name'] + ' (score: ' + str(sorted_showlist[-1]['score'])+ ')'

    print PREFIX_LOG + 'Result: ' + str(result)
    print PREFIX_LOG + 'Time: ' + str((time.time() - begin))
    return result

def get_eztv_shows():
    data = ''
    url_show_list = base_url + '/showlist/'
    data = get_url(url_show_list)
    eztv_shows = []
    for show_id, show_named_id, show_name in re.findall(r'<a href="/shows/([0-9][0-9]*)/(.*)/" class="thread_link">(.*)</a></td>', data):
        name1 = re.sub('[-]', ' ', show_named_id)
        t1 = re.sub('[&]', 'and', show_name)
        s1 = re.sub('\([^)A-Z]*\)|[\(\)\':]', '', t1)
        s2 = re.sub('\([^)]*\)|[\(\)\':]', '', t1)
        s3 = re.sub('[\(\)\':]', '', t1)
        f1 = re.findall(r'(.*),(.*)', s1, re.IGNORECASE)
        f2 = re.findall(r'(.*),(.*)', s2, re.IGNORECASE)
        f3 = re.findall(r'(.*),(.*)', s3, re.IGNORECASE)
        if(len(f1) > 0):
            name2 = f1[0][1] + ' ' + f1[0][0]
            name3 = f2[0][1] + ' ' + f2[0][0]
            name4 = f3[0][1] + ' ' + f3[0][0]
        else:
            name2 = s1
            name3 = s2
            name4 = s3
        eztv_shows.append({
            "id": show_id,
            "name1": name1.lower().strip(),
            "name2": name2.lower().strip(),
            "name3": name3.lower().strip(),
            "name4": name4.lower().strip(),
        })
    return eztv_shows

def get_cached_func(funcName,funcParm=(False,)):
    m = hashlib.md5()
    m.update(funcName + str(funcParm))
    key = m.hexdigest()
    cache_file = cache_prefix + key + '.db'
    f = globals()[funcName]
    d = shelve.open(cache_file)
    if (d.has_key(key)):
        value = d[key]
        d.close()
        thread.start_new_thread(update_cache, (key,funcName,funcParm, ))
        return value
    else:
        if(funcParm[0] == False):
            d[key] = f()
        else:
            d[key] = f(*funcParm)
        return d[key]
        
def get_magnet_list(url):
    data = get_url(url)
    result = []
    for magnet in re.findall(r'(magnet.*)" class="magnet"', data, re.IGNORECASE):
        result.append({'uri': magnet})
    return result

def search_in_list(string, list):
    result = []
    regex = re.compile(r'.*' + string + '.*')
    for element in list:
        m = re.match(regex, str(element))
        if m:
            result.append(element)
    return result
    
def get_url(url):
    print PREFIX_LOG + 'Downloading ' + url
    req = urllib2.Request(url, headers=HEADERS)
    data = urllib2.urlopen(req).read()
    return data

def update_cache(key,funcName,funcParm):
    m = hashlib.md5()
    m.update(funcName + str(funcParm))
    key = m.hexdigest()
    cache_file = cache_prefix + key + '.db'
    f = globals()[funcName]
    d = shelve.open(cache_file)
    if(funcParm[0] == False):
        d[key] = f()
    else:
        d[key] = f(*funcParm)
    print PREFIX_LOG + 'Cache key: ' + key + ' updated!'
    d.close()

def search_movie(movie):
    return []

def search(query):
    return []

provider.register(search, search_movie, search_episode)
