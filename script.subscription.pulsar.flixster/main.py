# coding: utf-8
import re
import subscription

# this read the settings
settings = subscription.Settings()
# define the browser
browser = subscription.Browser()

url_search = "http://www.flixster.com"
listing = []
ID = []  # IMDB_ID or thetvdb ID
if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Checking Online...', settings.icon, settings.time_noti)
settings.log('[%s]%s' % (settings.name_provider_clean, url_search))
if browser.open(url_search):
    data = browser.content
    data = data[data.find('Top DVD Rentals'):]  # narrow the file
    listing = re.findall('<div class="movie-title">(.*?)</div>',data)
    subscription.integration(listing, ID,'MOVIE', settings.movie_folder, name_provider=settings.name_provider)
else:
    settings.log('[%s]>>>>>>>%s<<<<<<<' % (settings.name_provider_clean, browser.status))
    settings.dialog.notification(settings.name_provider, browser.status, settings.icon, 1000)
del settings
del browser
