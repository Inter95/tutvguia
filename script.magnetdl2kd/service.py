# coding: utf-8
import re
import tools
from urllib import unquote_plus

from time import time
from time import asctime
from time import localtime
from time import strftime
from time import gmtime
from xbmc import log
from xbmc import sleep
from xbmc import abortRequested
from xbmcaddon import Addon


def update_service():
    # this read the settings
    settings = tools.Settings()
    browser = tools.Browser()
    filters = tools.Filtering()

    def extract_torrents(data):
        try:
            filters.information()  # print filters settings
            data = tools.clean_html(data)
            size = re.findall('</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)B</td>', data)  # list the size
            cont = 0
            results = []
            for cm, magnet in enumerate(re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)):
                name = re.search('dn=(.*?)&amp;tr=', magnet).group(1)  # find name in the magnet
                name = unquote_plus(name).replace('.', ' ') + ' - ' + settings.name_provider
                if filters.verify(size[cm][2] + 'B' + ' - ' + name, size[cm][2]):
                    results.append({"name": name, "uri": magnet})  # return le torrent
                    cont += 1
                else:
                    settings.log('[%s]%s' % (settings.name_provider_clean, filters.reason))
                if cont == settings.max_magnets:  # limit magnets
                    break
            return results
        except:
            settings.log('[%s]%s' % (settings.name_provider_clean, '>>>>>>>ERROR parsing data<<<<<<<'))
            settings.dialog.notification(settings.name_provider, '>>>>>>>>ERROR parsing data<<<<<<<<', settings.icon,
                                         1000)


    def search(query='', type='', silence=False):
        results = []
        if type == 'MOVIE':
            folder = settings.movie_folder
        else:
            folder = settings.show_folder
        # start to search
        if settings.pages == 0:  # manual pages if the parameter is zero
            settings.pages = settings.dialog.numeric(0, 'Number of pages:')
            if settings.pages == '' or settings.pages == 0:
                settings.pages = "1"
            settings.pages = int(settings.pages)
        for page in range(settings.pages):
            url_search = query % (settings.url_address, page)
            settings.log('[%s]%s' % (settings.name_provider_clean, url_search))
            if settings.time_noti > 0: settings.dialog.notification(settings.name_provider,
                                                                    'Checking Page %s...' % page,
                                                                    settings.icon, settings.time_noti)
            if browser.open(url_search):
                results.extend(extract_torrents(browser.content))
                if int(page) % 10 == 0: sleep(3000)  # to avoid too many connections
            else:
                settings.log('[%s]%s' % (settings.name_provider_clean, '>>>>>>>%s<<<<<<<' % browser.status))
                settings.dialog.notification(settings.name_provider, browser.status, settings.icon, 1000)
        if len(results) > 0:
            title = []
            magnet = []
            for item in results:
                info = tools.format_title(item['name'])
                if info['type'] == type:
                    title.append(item['name'])
                    magnet.append(item['uri'])
            tools.integration(filename=title, magnet=magnet, type_list=type, folder=folder, silence=silence,
                              name_provider=settings.name_provider)

    # define the browser
    if Addon().getSetting('movies')== 'true':  # Movies
        query = '%s/download/movies/se/desc/%s'
        search(query, 'MOVIE', True)
    if Addon().getSetting('tvshows') == 'true':  # TV shows
        query = '%s/download/tv/se/desc/%s'


if Addon().getSetting('service') == 'true':
    persistent = Addon().getSetting('persistent')
    name_provider = re.sub('.COLOR (.*?)]', '', Addon().getAddonInfo('name').replace('[/COLOR]', ''))
    every = 28800  # seconds
    previous_time = time()
    log("[%s] Persistent Update Service starting..." % name_provider)
    update_service()
    while (not abortRequested) and persistent == 'true':
        if time() >= previous_time + every:  # verification
            previous_time = time()
            update_service()
            log('[%s] Update List at %s' % (name_provider, asctime(localtime(previous_time))))
            log('[%s] Next Update in %s' % (name_provider, strftime("%H:%M:%S", gmtime(every))))
            update_service()
        sleep(500)
