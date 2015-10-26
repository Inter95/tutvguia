# coding: utf-8
from pulsar import provider
from urllib import unquote_plus
import re
import common

# this read the settings
settings = common.Settings()
# define the browser
browser = common.Browser()
# create the filters
filters = common.Filtering()

# this read the settings
values3 = {'ALL': 0, 'HDTV': 1,'480p': 1,'DVD': 1,'720p': 2 ,'1080p': 3, '3D': 3, "1440p": 4 ,"2K": 5,"4K": 5} #code_resolution steeve

#premium account
username = provider.ADDON.getSetting('username')  # username
password = provider.ADDON.getSetting('password')  # passsword
browser.open(settings.url + '/auth/login')
# open login_check
browser.login(settings.url + '/ajax/login_check_user.php', {'user': username}, "true")
browser.login(settings.url + '/ajax/login_check_pass.php', {'user': username, 'password': password}, "true")

# open login_check
browser.login(settings.url + '/ajax/login_check.php', {'user': username, 'password': password}, "true")
if browser.content != 'true' :  # login
    provider.notify(message=browser.status, header='ERROR!!', time=5000, image=settings.icon)
    provider.log.error('******** Wrong Password or Username ********' % browser.status)


def get_url(scd_link): # find url from adf.ly
    browser1 = common.Browser()
    url = 'http://www.bypassshorturl.com/get.php'
    values = {'url': scd_link }
    browser1.login(url,values,'true')
    return browser1.content


def get_torrent(torrent):
    url_code = '%s/movie/%s.html' % (settings.url,torrent)
    browser.open(url_code)
    data = browser.content
    code = re.search('{id:(.*?),',data).group(1)
    browser.open('%s/ajax/download.html?id=%s&code=1' % (settings.url,code))
    url_adfly = browser.content
    return get_url(url_adfly)


def extract_torrents(data):
    try:
        filters.information()
        size = re.findall('(.*?)&nbsp;<span class="icon-hdd">',data)
        cont = 0
        results = []
        for cm,(temp,torrent) in enumerate(re.findall('class="thumbnail"(.*?)/movie/(.*?).html',data, re.S)):
            if '3D' in torrent: resASCII = '3D'
            if '1080p' in torrent: resASCII = '1080p'
            if '720p' in torrent: resASCII = '720p'
            name = size[cm].lstrip() + ' - ' + torrent.replace('-',' ').title() + ' - ' +  settings.name_provider
            if filters.verify(name + ' ' + filters.title, size[cm]):
                results.append({'name' : name, 'uri' : get_torrent(torrent) , 'resolution' : values3[resASCII], 'filesize' : size[cm].lstrip()})
                cont += 1
            else:
                provider.log.warning(filters.reason)
            if cont == settings.max_magnets:  # limit magnets
                break
        provider.log.info('>>>>>>' + str(cont) + ' torrents sent to Pulsar<<<<<<<')
        return results
    except:
        provider.log.error('>>>>>>>ERROR parsing data<<<<<<<')
        provider.notify(message='ERROR parsing data', header=None, time=5000, image=settings.icon)
        return  []


def search(query):
    query += ' ' + settings.extra  # add the extra information
    query = filters.type_filtering(query, '+')  # check type filter and set-up filters.title
    url_search = "%s?q=%s" % (settings.url, query)  # change in each provider
    provider.log.info(url_search)
    if browser.open(url_search):
        results = extract_torrents(browser.content)
    else:
        provider.log.error('>>>>>>>%s<<<<<<<' % browser.status)
        provider.notify(message=browser.status, header=None, time=5000, image=settings.icon)
        results = []
    return results


def search_movie(info):
    query = info['imdb_id']  # Just IMDB_id
    query += ' #MOVIE&FILTER'  #to use movie filters
    return search(query)


def search_episode(info):
    # just movies site
    return []


# This registers your module for use
provider.register(search, search_movie, search_episode)

del settings
del browser
del filters