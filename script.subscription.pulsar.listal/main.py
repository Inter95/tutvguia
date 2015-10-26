# coding: utf-8
import re
import subscription

# this read the settings
settings = subscription.Settings()
# define the browser
browser = subscription.Browser()

list = settings.dialog.input('www.listal.com/list/', 'listals-100-films-see-before-3479')
if list != '':
    url_search = "http://www.listal.com/list/%s" % list
    listing = []
    ID = []  # IMDB_ID or thetvdb ID
    settings.log('[%s]%s' % (settings.name_provider_clean, url_search))
    if browser.open(url_search):
        data = browser.content
        data = data.replace('</a></span>', '')
        for line in re.findall("style='font-weight:bold;font-size:110%;'>(.*?)>(.*?)</div>",data, re.S):
            listing.append(line[1].replace('\r', '').replace('\n', '').replace('\t', ''))
        subscription.integration(listing, ID,'MOVIE', settings.movie_folder, name_provider=settings.name_provider)
    else:
        settings.log('[%s]>>>>>>>%s<<<<<<<' % (settings.name_provider_clean, browser.status))
        settings.dialog.notification(settings.name_provider, browser.status, settings.icon, 1000)
else:
    settings.dialog.ok(settings.name_provider,'Empty List! Nothing added.')