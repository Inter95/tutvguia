# coding: utf-8
from tools import *


def changeTitle(name=''):
    pos = name.find(',')  # CHANGE TITLE
    if pos > 0:
        name = name[pos + 1:].lstrip() + ' ' + name[:pos]  # change Simpsons, The = The Simpsons
    name = name.replace(')', '').replace('(', '')  # change (2015) = 2015
    return name.replace("'", '')  # replace Grey's = Greys


# main
storage = Storage(settings.storageName)
listShows = storage.database

rep = 0
ListName = []
ListNameId = []
while rep is not 7:
    rep = settings.dialog.select('Choose an Option:',
                                 ['Add a New Show', 'Remove a Show', 'View The List', 'ReBuild All Episodes',
                                  'Sync .strm Files', '-SETTINGS', '-HELP', 'Exit'])
    if rep == 0:  # Add new Show
        if len(ListName) == 0:
            settings.notification("Checking Online")
            urlSearch = settings.value["urlAddress"]
            settings.log(urlSearch)
            response = browser.get(urlSearch, verify=False)
            if response.status_code == requests.codes.ok:  # create the list of shows
                data = response.text
                data = data[data.find('</option>'):]
                results = re.findall('<option value="(.*?)">(.*?)</option>', data)
                ListName = [result[1] for result in results]  # list of shows
                ListNameId = [result[0] for result in results]  # list of IDs
        name = settings.dialog.input('New Show:')
        if name == '':
            optionList = ListName
            optionID = ListNameId
        else:
            optionList = []
            optionID = []
            for (itemID, item) in zip(ListNameId, ListName):
                if name.lower() in item.lower():
                    optionList.append(item)
                    optionID.append(itemID)
            if len(optionList) == 0:
                optionList = ListName
                optionID = ListNameId
        selection = settings.dialog.select('New Show', optionList + ['CANCEL'])
        if selection < len(optionList):
            name = changeTitle(optionList[selection])
            if name not in listShows:
                listShows.append(name)
                listShows.sort()
            ID = optionID[selection]
            if settings.dialog.yesno(settings.cleanName, 'Do you want to add episodes available for %s' % name):
                urlSearch = settings.value["urlAddress"]  # search for the show
                payload = {'SearchString1': '', 'SearchString': ID, 'search': 'Search'}
                settings.notification('Checking Online for %s...' % name)
                settings.log(urlSearch)
                response = browser.post(urlSearch, data=payload)
                qualityOptions = ['HDTV:720p:1080p', '1080p:720p:HDTV', '720p:1080p', '1080p:720p', 'HDTV:720p',
                                  '720p:HDTV', 'HDTV', '720p', '1080p']
                qualityRet = settings.dialog.select('Quality:', qualityOptions)
                qualityKeys = qualityOptions[qualityRet].lower().split(":")
                magnetsList = []
                filenameList = []
                titlesList = []
                data = response.text
                seasons = list(set(re.findall('S[0-9]+E', data.upper()))) + ['ALL']
                seasons.sort()
                season = settings.dialog.select('Season:', seasons)
                print seasons[season]
                magnets = re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)
                for quality in qualityKeys:
                    for magnet in magnets:
                        name_file = magnet.lower() + ' hdtv'  # take any file as hdtv by default
                        if seasons[season].lower() in name_file or seasons[
                            season] == 'ALL':  # check for the right season to add
                            if quality == 'hdtv' and ('720p' in name_file or '1080p' in name_file):
                                name_file = name_file.replace('hdtv', '')
                            if quality in name_file:
                                magnetsList.append(magnet)
                                info = Magnet(magnet)
                                filenameList.append(info.name)
                integration(magnets=magnetsList, titles=filenameList, typeList='SHOW', folder=settings.showFolder)
    if rep == 1 and len(listShows) > 0:  # Remove Show
        list_rep = settings.dialog.select('Choose Show to Remove', listShows + ['CANCEL'])
        if list_rep < len(listShows):
            if settings.dialog.yesno(settings.cleanName, 'Do you want Remove %s?' % listShows[list_rep]):
                del listShows[list_rep]
    if rep == 2:  # View Show
        settings.dialog.select('Shows', listShows)
    if rep == 3:  # Rebuild Strm files
        if settings.dialog.yesno("EZTV2KD", "Do you want to rebuild the all the episodes?"):
            qualityOptions = ['HDTV:720p:1080p', '1080p:720p:HDTV', '720p:1080p', '1080p:720p', 'HDTV:720p',
                              '720p:HDTV', 'HDTV',
                              '720p', '1080p']
            qualityRet = settings.dialog.select('Quality:', qualityOptions)
            qualityKeys = qualityOptions[qualityRet].lower().split(":")
            number = int(settings.settings.getSetting('number'))
            if len(ListName) == 0:
                settings.notification('Checking Online')
                urlSearch = settings.value["urlAddress"]
                settings.log(urlSearch)
                response = browser.get(urlSearch, verify=False)
                if response.status_code == requests.codes.ok:  # create the list of shows
                    data = response.text
                    data = data[data.find('</option>'):]
                    results = re.findall('<option value="(.*?)">(.*?)</option>', data)
                    ListName = [changeTitle(result[1]) for result in results]  # list of shows
                    ListNameId = [result[0] for result in results]  # list of IDs
            magnetsList = []
            filenameList = []
            ID = dict(zip(ListName, ListNameId))
            printer(ID)
            for show in listShows:
                settings.notification('Checking Online for %s...' % show)
                urlSearch = settings.value["urlAddress"]  # search for the show
                payload = {'SearchString1': '', 'SearchString': ID[show], 'search': 'Search'}
                settings.notification('Checking Online...')
                settings.log(urlSearch)
                response = browser.post(urlSearch, data=payload)
                data = response.text
                magnets = re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)
                for quality in qualityKeys:
                    for magnet in magnets:
                        name_file = magnet.lower() + ' hdtv'  # take any file as hdtv by default
                        if quality == 'hdtv' and ('720p' in name_file or '1080p' in name_file):
                            name_file = name_file.replace('hdtv', '')
                        if quality in name_file:
                            magnetsList.append(magnet)
                            info = Magnet(magnet)
                            filenameList.append(info.name)
            integration(titles=filenameList, magnets=magnetsList, typeList='SHOW', folder=settings.showFolder)
    if rep == 4:  # Update strm
        settings.notification('Checking Online...')
        if len(listShows) > 0:
            qualityOptions = ['HDTV:720p:1080p', '1080p:720p:HDTV', '720p:1080p', '1080p:720p', 'HDTV:720p',
                              '720p:HDTV', 'HDTV', '720p', '1080p']
            qualityRet = settings.dialog.select('Quality:', qualityOptions)
            qualityKeys = qualityOptions[qualityRet].lower().split(":")
            number = int(settings.settings.getSetting('number'))
            magnetsList = []
            filenameList = []
            if number == 0:  # manual pages if the parameter is zero
                number = settings.dialog.numeric(0, 'Number of pages:')
                if number == '' or number == 0:
                    number = "1"
                number = int(number)
            for page in range(number + 1):
                if page == 0:
                    urlSearch = settings.value["urlAddress"]
                else:
                    urlSearch = '%s/page_%s' % (settings.value["urlAddress"], str(page))
                settings.notification('Still working...')
                response = browser.get(urlSearch, verify=False)
                if response.status_code == requests.codes.ok:
                    data = response.text
                    for quality in qualityKeys:
                        for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data):
                            for show in listShows:
                                name_file = magnet.lower()
                                if quality == 'hdtv' and ('720p' in name_file or '1080p' in name_file):
                                    name_file = name_file.replace('hdtv', '')
                                if show.replace(' ', '.').lower() in name_file and quality in name_file:
                                    magnetsList.append(magnet)
                                    info = Magnet(magnet)
                                    filenameList.append(info.name)
                        if int(page) % 10 == 0: sleep(3000)  # to avoid too many connections
                else:
                    settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
                    settings.notification(message="HTTP %s" % response.status_code, force=True)
            integration(titles=filenameList, magnets=magnetsList, typeList='SHOW', folder=settings.showFolder)
    if rep == 5:  # settings
        settings.settings.openSettings()
        settings = Settings()
    if rep == 6:  # help
        settings.dialog.ok("Help",
                           "Please, check this address to find the user's operation:\n[B]http://goo.gl/8nYU6R[/B]")
# save the list
storage.save()
del settings
del browser
del storage
