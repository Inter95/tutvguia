# coding: utf-8
import re
import tools
import shelve
from xbmc import translatePath
from xbmc import sleep


def search_tvshow():
    import json
    name = settings.dialog.input('New TV Show:')
    url = '%s/shows.json?q=%s' % (settings.url_address, name.replace(' ', '+'))
    if settings.time_noti > 0: settings.dialog.notification(settings.name_provider,
                                'Checking Online...', settings.icon, settings.time_noti)
    browser.open(url)
    data = browser.content
    list_names = {}
    for item in json.loads(data):
        list_names[item['title']] = item['value']
    return list_names


# main
path = translatePath('special://temp')
#get the Dictionary
Dict_tvshows = {}
try:
    with open(path + 'addertv2PULSAR.txt', 'r') as fp:
        for line in fp:
            listedline = line.strip().split('::')  # split around the :: sign
            if len(listedline) > 1:  # we have the : sign in there
                Dict_tvshows[listedline[0]] = listedline[1]
except:
    pass

# this read the settings
settings = tools.Settings()
# define the browser
browser = tools.Browser()

rep = 0
List_name = []
while rep is not 7:
    rep = settings.dialog.select('Choose an Option:', ['Add a New Show', 'Remove a Show', 'View The List', 'ReBuild All Episodes', 'Sync .strm Files', '-SETTINGS', '-HELP', 'Exit'])
    if rep == 0:  # Add a New Show
        list_name = search_tvshow()
        if len(list_name.keys()) > 0:
            selection = settings.dialog.select('Select One Show:', list_name.keys() + ['CANCEL']) # check the name
            if  selection < len (list_name.keys()):
                name = list_name.keys()[selection]
                value = list_name[name]
                Dict_tvshows[name] = value
                if settings.dialog.yesno(settings.name_provider, 'Do you want to add ALL the episodes available for %s' % name):
                    magnet_list = []
                    file_list = []
                    title_list = []
                    url_search = '%s/watch/%s' % (settings.url_address, value) # search for the episodes
                    if settings.time_noti > 0: settings.dialog.notification(settings.name_provider,
                                                'Checking Online...', settings.icon, settings.time_noti)
                    browser.open(url_search)
                    settings.log('[%s]%s' % (settings.name_provider_clean, url_search))
                    data = browser.content
                    if data is not None and len(data) > 0:
                        for item in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data):
                            info = tools.Magnet(item)
                            magnet_list.append(item)
                            file_list.append(info.name)
                            title_list.append(name)
                    if len(file_list)>0:
                        tools.integration(title=title_list, filename=file_list, magnet=magnet_list, type_list='SHOW',
                                        folder=settings.show_folder, name_provider=settings.name_provider)
    if rep == 1 and len(Dict_tvshows.keys()) > 0:  # Remove
        list_rep = settings.dialog.select('Choose Show to Remove', Dict_tvshows.keys() + ['CANCEL'])
        if list_rep < len(Dict_tvshows.keys()):
            if settings.dialog.yesno('', 'Do you want Remove %s?' % Dict_tvshows.keys()[list_rep]):
                print Dict_tvshows.keys()[list_rep]
                del Dict_tvshows[Dict_tvshows.keys()[list_rep]]
    if rep == 2:  # List
        settings.dialog.select('Shows', Dict_tvshows.keys())
    if rep == 3:  # Rebuild
        if settings.dialog.yesno("AdderTV2PULSAR", "Do you want to rebuild the all the episodes?"):
            magnet_list = []
            file_list = []
            title_list = []
            for (show, value) in Dict_tvshows.items():
                if settings.time_noti > 0: settings.dialog.notification(settings.name_provider,
                                            'Checking Online for %s...' % show, settings.icon, settings.time_noti)
                url_search = '%s/watch/%s' % (settings.url_address, value)  # search for the tvshow
                settings.log('[%s]%s' % (settings.name_provider_clean, url_search))
                browser.open(url_search)
                data = browser.content
                if data is not None and len(data) > 0:
                    for item in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data):
                        info = tools.Magnet(item)
                        magnet_list.append(item)
                        file_list.append(info.name)
                        title_list.append(show)
            if len(file_list) > 0:
                tools.integration(title=title_list, filename=file_list, magnet=magnet_list, type_list='SHOW',
                              folder=settings.show_folder, name_provider=settings.name_provider)
    if rep == 4:  # Update
        if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Checking Online...', settings.icon, settings.time_noti)
        if len(Dict_tvshows.keys()) > 0:
            magnet_list = []
            file_list = []
            title_list = []
            for (show, value) in Dict_tvshows.items():
                if settings.time_noti > 0: settings.dialog.notification(settings.name_provider,
                                            'Checking Online for %s...' % show, settings.icon, settings.time_noti)
                url_search = '%s/watch/%s' % (settings.url_address, value)  # search for the tvshow
                settings.log('[%s]%s' % (settings.name_provider_clean, url_search))
                browser.open(url_search)
                data = browser.content
                if data is not None and len(data) > 0:
                    for item in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data):
                        info = tools.Magnet(item)
                        magnet_list.append(item)
                        file_list.append(info.name)
                        title_list.append(show)
            if len(file_list) > 0:
                tools.integration(title=title_list, filename=file_list, magnet=magnet_list, type_list='SHOW',
                              folder=settings.show_folder, name_provider=settings.name_provider)
        else:
            if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Empty List', settings.icon, settings.time_noti)
    if rep == 5:  # Settings
        settings.settings.openSettings()
        settings = tools.Settings(anime=True)
    if rep == 6:  # Help
            settings.dialog.ok("Help", "Please, check this address to find the user's operation:\n[B]http://goo.gl/8nYU6R[/B]")

# save the dictionary
with open(path + 'Addertv2PULSAR.txt', 'w') as fp:
    for p in Dict_tvshows.items():
        fp.write("%s::%s\n" % p)
del settings
del browser
