# coding: utf-8
from tools import *
from time import time
from time import asctime
from time import localtime
from time import strftime
from time import gmtime


def update_service():
    if settings.value['service'] == 'true':
        # main
        storage = Storage(settings.storageName)
        listShows = storage.database
        settings.notification('Checking Online')
        settings.debug(listShows)
        if len(listShows) > 0:
            qualityKeys = settings.value['quality'].lower().split(":")
            number = int(settings.value['number'])
            settings.debug(qualityKeys)
            settings.debug(number)
            magnetsList = []
            filenameList = []
            if number == 0: number = 1  # manual pages if the parameter is zero
            for page in range(number + 1):
                if page == 0:
                    urlSearch = settings.value["urlAddress"]
                else:
                    urlSearch = '%s/page_%s' % (settings.value["urlAddress"], str(page))
                settings.notification('Checking online... %s' % urlSearch)
                settings.debug(urlSearch)
                response = browser.get(urlSearch, verify=False)
                settings.debug(response.status_code)
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
                        if int(page) % 10 == 0: sleep(3)  # to avoid too many connections
                else:
                    settings.log(">>>>>>>HTTP %s<<<<<<<" % response.status_code)
                    settings.notification(message="HTTP %s" % response.status_code, force=True)
            settings.debug(filenameList)
            settings.debug(magnetsList)
            settings.debug(settings.showFolder)
            integration(titles=filenameList, magnets=magnetsList, typeList='SHOW', folder=settings.showFolder,
                        silence=True)
        del storage


if settings.value['service'] == 'true':
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