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

#premium account
username = provider.ADDON.getSetting('username')  # username
password = provider.ADDON.getSetting('password')  # passsword
browser.open(settings.url + '/auth/login')
_token = re.search('_token" type="hidden" value="(.*?)"', browser.content).group(1) # hidden variable required to log in
# open premium account
if not browser.login(settings.url + '/auth/login', {'username_email': username, 'password': password, '_token': _token}, "These credentials do not match our records"):  # login
    provider.notify(message=browser.status, header='ERROR!!', time=5000, image=settings.icon)
    provider.log.error('******** %s ********' % browser.status)

# using function from Steeve to add Provider's name and search torrent
def extract_torrents(data):
    try:
        filters.information()  # print filters settings
        data = common.clean_html(data)
        data = data.replace("text-orange", "")
        size = re.findall('<td><span class="">(.*?)<', data)
        lname = re.findall('title="Download:(.*?)"', data)
        cont = 0
        results = []
        for cm, url_torrent in enumerate(re.findall('/download/torrent/(.*?)"', data)):
            name = size[cm] + ' - ' + lname[cm].strip() + ' - ' + settings.name_provider
            if filters.verify(name,size[cm]):
                # download the .torrent file
                torrent = settings.url + '/download/torrent/' + url_torrent
                header = ""
                for item in  browser.cookies:
                    header += item.name + '=' + item.value + '; '
                uri = provider.append_headers(torrent, {'cookie' : header})
                print uri
                # Send information to Pulsar
                results.append({"name": name, "uri": uri})  # return le torrent
                cont+= 1
            else:
                provider.log.warning(filters.reason)
            if cont == settings.max_magnets:  # limit magnets
                break
        provider.log.info('>>>>>>' + str(cont) + ' torrents sent to Pulsar<<<<<<<')
        return results
    except:
        provider.log.error('>>>>>>>ERROR parsing data<<<<<<<')
        provider.notify(message='ERROR parsing data', header=None, time=5000, image=settings.icon)
        results = []


def search(query):
    query += ' ' + settings.extra  # add the extra information
    query = filters.type_filtering(query, '+')  # check type filter and set-up filters.title
    query = re.sub('s..e...', '', query)
    url_search = "%s/torrents?in=1&search=%s&tags=&type=0&language=0&subtitle=0&discount=0&rip_type=0&video_quality=0&tv_type=0&uploader=" % (settings.url,query)
    provider.log.info(url_search)
    if browser.open(url_search):
        results = extract_torrents(browser.content)
    else:
        provider.log.error('>>>>>>>%s<<<<<<<' % browser.status)
        provider.notify(message=browser.status, header=None, time=5000, image=settings.icon)
        results = []
    return results


def search_movie(info):
    if settings.language == 'en':  # Title in english
        query = info['title'].encode('utf-8')  # convert from unicode
        if len(info['title']) == len(query):  # it is a english title
            query += ' ' + str(info['year'])  # Title + year
        else:
            query = common.IMDB_title(info['imdb_id'])  # Title + year
    else:  # Title en foreign language
        query = common.translator(info['imdb_id'],settings.language)  # Just title
    query += ' #MOVIE&FILTER'  #to use movie filters
    return search(query)


def search_episode(info):
    if info['absolute_number'] == 0:
        query = info['title'].encode('utf-8') + ' s%02de%02d' % (info['season'], info['episode'])  # define query
    else:
        query = info['title'].encode('utf-8') + ' %02d' % info['absolute_number']  # define query anime
    query += ' #TV&FILTER'  #to use TV filters
    return search(query)


# This registers your module for use
provider.register(search, search_movie, search_episode)

del settings
del browser
del filters