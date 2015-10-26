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


#just get the cookies to avoid catpcha
#browser.login(settings.url + '/torrents.php', {'q': ''}, "None")
# #premium account
# username = provider.ADDON.getSetting('username')  # username
# password = provider.ADDON.getSetting('password')  # passsword
# # open premium account
# if not browser.login(settings.url + '/auth/login', {'username': username, 'password': password, '_token': _token}, "Forgot Password"):  # login
#     provider.notify(message=browser.status, header='ERROR!!', time=5000, image=settings.icon)
#     provider.log.error('******** %s ********' % browser.status)

# using function from Steeve to add Provider's name and search torrent
def extract_torrents(data):
    try:
        cont = 0
        results = []
        items = provider.parse_json(data)
        if not items.has_key("error"):
            for item in items["torrent_results"]:
                name = item["filename"] + ' - ' + settings.name_provider
                torrent = item["download"]
                if filters.verify(name, None):
                    results.append({"name": name, "uri": torrent})  # return le torrent)
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


def search(query):
    query += ' ' + settings.extra  # add the extra information
    query = filters.type_filtering(query, '+')  # check type filter and set-up filters.title
    browser.open("%s?get_token=get_token&app_id=script.pulsar.rarbg-mc" % settings.url)
    items = provider.parse_json(browser.content)
    url_search = "%s?mode=search&search_string=%s&app_id=script.pulsar.rarbg-mc&token=%s" % (settings.url, query, items["token"])  # change in each provider
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