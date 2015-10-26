# coding: utf-8
from tools import *
from time import time
from time import asctime
from time import localtime
from time import strftime
from time import gmtime


def update_service():
    if settings.value['service'] == 'true':
        # watchlist
        if settings.value["watchlist"] == 'true' and settings.value["user"] is not '':  # watchlist
            urlSearch = "http://www.imdb.com/user/%s/watchlist" % settings.value["user"]
            settings.notification(settings.string(32044))  # Checking Online
            response = browser.get(urlSearch)
            if response.status_code == requests.codes.ok:
                data = response.text
                list = re.findall('/list/export.list_id=(.*?)&', data)
                if list != []:
                    start = 1
                    movieListing = []
                    showListing = []
                    movieID = []  # IMDB_ID or thetvdb ID
                    TV_ID = []  # IMDB_ID or thetvdb ID
                    while True:
                        urlSearch = "http://www.imdb.com/list/%s/?start=%d&view=detail&sort=listorian:asc" % (
                            list[0], start)
                        settings.notification(settings.string(32044))  # Checking Online
                        settings.log(urlSearch)
                        response = browser.get(urlSearch)
                        if response.status_code == requests.codes.ok:
                            data = response.text
                            lines = re.findall('<div class="info">(.*?)</div>', data, re.S)
                            if len(lines) > 0:
                                for line in re.findall('<div class="info">(.*?)</div>', data, re.S):
                                    if 'This title is no longer available' not in line:  # prevent the error with not info
                                        items = re.search('/title/(.*?)/(.*?)>(.*?)<', line)
                                        year = re.search('<span class="year_type">(.*?)<', line)
                                        if 'TV Series' in year.group(1) or 'Mini-Series' in year.group(1):
                                            showListing.append(items.group(3))  # without year
                                            TV_ID.append(items.group(1))
                                        else:
                                            movieListing.append(items.group(3) + ' ' + year.group(1))
                                            movieID.append(items.group(1))
                                start += 100
                            else:
                                break
                        else:
                            settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
                            settings.notification(message="HTTP %s" % response.status_code, force=True)
                            break
                    if len(movieListing) > 0:
                        subscription(movieListing, movieID, 'MOVIE', settings.movieFolder, message="Watchlist",
                                     silence=True)
                    if len(showListing) > 0:
                        subscription(showListing, [], 'SHOW', settings.showFolder, message="Watchlist",
                                     silence=True)
        # List
        if settings.value["imdblist"] == 'true' and settings.value["list"] is not '':  # list
            start = 1
            movieListing = []
            showListing = []
            movieID = []  # IMDB_ID or thetvdb ID
            TV_ID = []  # IMDB_ID or thetvdb ID
            while True:
                urlSearch = "http://www.imdb.com/list/%s/?start=%d&view=detail&sort=listorian:asc" % (
                settings.value["list"], start)
                settings.notification(settings.string(32044))  # Checking Online
                settings.log(urlSearch)
                response = browser.get(urlSearch)
                if response.status_code == requests.codes.ok:
                    data = response.text
                    lines = re.findall('<div class="info">(.*?)</div>', data, re.S)
                    if len(lines) > 0:
                        for line in re.findall('<div class="info">(.*?)</div>', data, re.S):
                            if 'This title is no longer available' not in line:  # prevent the error with not info
                                items = re.search('/title/(.*?)/(.*?)>(.*?)<', line)
                                year = re.search('<span class="year_type">(.*?)<', line)
                                if 'TV Series' in year.group(1):
                                    showListing.append(items.group(3))  # without year
                                    TV_ID.append(items.group(1))
                                else:
                                    movieListing.append(items.group(3) + ' ' + year.group(1))
                                    movieID.append(items.group(1))
                        start += 100
                    else:
                        break
                else:
                    settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
                    settings.notification(message="HTTP %s" % response.status_code, force=True)
                    break
            if len(movieListing) > 0:
                subscription(movieListing, movieID, 'MOVIE', settings.movieFolder, silence=True, message="List")
            if len(showListing) > 0:
                subscription(showListing, [], 'SHOW', settings.show_folder, silence=True,message="List")


if settings.value['service'] == 'true':
    sleep(int(settings.value['delayTime']))  # get the delay to allow pulsar starts
    every = 28800  # seconds
    previous_time = time()
    settings.log("Persistent Update Service starting...")
    update_service()
    while (not xbmc.abortRequested) and settings.value["persistent"] == 'true':
        if time() >= previous_time + every:  # verification
            previous_time = time()
            update_service()
            settings.log('Update List at %s' % asctime(localtime(previous_time)))
            settings.log('Next Update in %s' % strftime("%H:%M:%S", gmtime(every)))
            update_service()
        sleep(1)

del settings
del browser
