# coding: utf-8
import re
import tools
from urllib import unquote_plus
from xbmc import sleep

# this read the settings
settings = tools.Settings()
browser = tools.Browser()
filters = tools.Filtering()


def extract_torrents(data):
    try:
        filters.information()  # print filters settings
        data = tools.clean_html(data)
        size = re.findall('</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)B</td>', data) # list the size
        cont = 0
        results = []
        for cm, magnet in enumerate(re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)):
            name = re.search('dn=(.*?)&amp;tr=',magnet).group(1) #find name in the magnet
            name = unquote_plus(name).replace('.', ' ')
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
        settings.dialog.notification(settings.name_provider, '>>>>>>>>ERROR parsing data<<<<<<<<', settings.icon, 1000)


def search(query='', type='', silence=False):
    results = []
    if type == 'MOVIE':
        folder = settings.movie_folder
    else:
        folder = settings.show_folder
    # start to search
    settings.pages = settings.dialog.numeric(0, 'Number of pages:')
    if settings.pages == '' or settings.pages == 0:
        settings.pages = "1"
    settings.pages = int(settings.pages)
    for page in range(settings.pages):
        url_search = query % (settings.url_address, page)
        settings.log('[%s]%s' % (settings.name_provider_clean, url_search))
        if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Checking Page %s...' % page,
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
rep = 0

list = ['Movies', 'TV shows']
while rep < len(list):
    rep = settings.dialog.select('Choose an Option:', list + ['-SETTINGS', '-HELP', 'Exit'])
    if rep == 0:  # Movies
        query = '%s/download/movies/se/desc/%s'
        search(query, 'MOVIE')
    if rep == 1:  # TV shows
        query = '%s/download/tv/se/desc/%s'
        search(query, 'SHOW')
    if rep == len(list):  # Settings
        settings.settings.openSettings()
        settings = tools.Settings()
    if rep == len(list) + 1:  # Help
            settings.dialog.ok("Help", "Please, check this address to find the user's operation:\n[B]http://goo.gl/8nYU6R[/B]")

del browser
del settings
del filters