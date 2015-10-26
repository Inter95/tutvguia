# coding: utf-8
from tools import *
from time import time
from time import asctime
from time import localtime
from time import strftime
from time import gmtime


def update_service():
    if settings.value['service'] == 'true':
        xbmc.executebuiltin('XBMC.Runaddon(script.subscription.pulsar.favourites)')


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