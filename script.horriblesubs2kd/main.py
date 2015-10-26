# coding: utf-8
import re
import tools
import shelve
from xbmc import translatePath
from xbmc import sleep


def search_anime():
    name = settings.dialog.input('New Anime:')
    list_names = {}
    data = ""
    loop = True
    cm = 0
    while loop:
        url = '%s/lib/search.php?value=%s&nextid=%s' % (settings.url_address, name.replace(' ', '+'), cm)
        if settings.time_noti > 0: settings.dialog.notification(settings.name_provider,
                                                                'Checking Online, page %s...' % cm,
                                                                settings.icon, settings.time_noti)
        browser.open(url)
        datatemp = browser.content
        if datatemp is not None:
            data += datatemp
        cm += 1
        if cm % 5: sleep(500)
        if datatemp is None or len(datatemp) == 0:

            loop = False
    names = [item[:item.rfind('-')].strip().replace(' -', '') for item in re.findall('\)(.*?)<', data)]
    for item in names:  # remove duplicates
        list_names[item] = 'Yes'
    return list_names.keys()


# main
path = translatePath('special://temp')
#get the list
try:
    with open(path + 'HorribleSubs2PULSAR.txt', "r") as text_file:  # create .strm
        List_shows = [line.strip() for line in text_file]
        text_file.close()
except:
    #convert from the old version
    database = shelve.open(path + 'HorribleSubs2PULSAR.db')
    List_shows = []
    if database.has_key('list'):
       List_shows = database['list']
    else:
       List_shows = []

# this read the settings
settings = tools.Settings(anime=True)
# define the browser
browser = tools.Browser()

rep = 0
List_name = []
while rep is not 7:
    rep = settings.dialog.select('Choose an Option:', ['Add a New Anime', 'Remove a Anime', 'View The List', 'ReBuild All Episodes', 'Sync .strm Files', '-SETTINGS', '-HELP', 'Exit'])
    if rep == 0:  # Add a New Anime
        list_name = search_anime()
        if len(list_name) > 0:
            selection = settings.dialog.select('Select One Show:', list_name + ['CANCEL']) # check the name
            if  selection < len (list_name):
                name = list_name[selection]
                if name not in List_shows:
                    List_shows.append(name)
                    List_shows.sort()
                if settings.dialog.yesno(settings.name_provider, 'Do you want to add ALL the episodes available for %s' % name):
                    quality_options = ['720p:1080p', '1080p:720p', '480p:720p:1080p', '1080p:720p:480p', '480p', '720p',
                                       '1080p']
                    quality_ret = settings.dialog.select('Quality:', quality_options)
                    quality_keys = quality_options[quality_ret].lower().split(":")
                    magnet_list = []
                    file_list = []
                    loop = True
                    cm = 0
                    while loop:
                        url_search = '%s/lib/search.php?value=%s&nextid=%s' % (settings.url_address, name.replace(' ', '+'), cm) # search for the anime
                        if settings.time_noti > 0: settings.dialog.notification(settings.name_provider,
                                                                                'Checking Online, page %s...' % cm,
                                                                                settings.icon, settings.time_noti)
                        browser.open(url_search)
                        settings.log('[%s]%s' % (settings.name_provider_clean, url_search))
                        data = browser.content
                        cm += 1
                        if cm % 5: sleep(500)
                        if data is not None and len(data) > 0:
                            zip_list = zip(re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data), re.findall('<i>(.*?)<', data))
                            for quality in quality_keys:
                                for (magnet, name_file) in zip_list:
                                    if quality.lower() in name_file.lower():
                                        name_file = name_file.replace('_', ' ')
                                        magnet_list.append(magnet)
                                        pos = name_file.rfind('- ')
                                        name_file = name_file[:pos] + 'EP' + name_file[pos + 2:] # insert EP to be identificated in kodi
                                        file_list.append(name_file)
                        else:
                            loop = False
                    if len(file_list)>0:
                        tools.integration(filename=file_list, magnet=magnet_list, type_list='SHOW',
                                        folder=settings.show_folder, name_provider=settings.name_provider)
    if rep == 1 and len(List_shows) > 0:  # Remove
        list_rep = settings.dialog.select('Choose Show to Remove', List_shows + ['CANCEL'])
        if list_rep < len(List_shows):
            if settings.dialog.yesno('', 'Do you want Remove %s?' % List_shows[list_rep]):
                del List_shows[list_rep]
    if rep == 2:  # List
        settings.dialog.select('Shows', List_shows)
    if rep == 3:  # Rebuild
        if settings.dialog.yesno("Horriblesubs2PULSAR", "Do you want to rebuild the all the episodes?"):
            quality_options = ['720p:1080p', '1080p:720p', '480p:720p:1080p', '1080p:720p:480p', '480p', '720p', '1080p']
            quality_ret = settings.dialog.select('Quality:', quality_options)
            quality_keys = quality_options[quality_ret].lower().split(":")
            magnet_list = []
            file_list = []
            for show in List_shows:
                loop = True
                cm = 0
                while loop:
                    if settings.time_noti > 0: settings.dialog.notification(settings.name_provider,
                                                'Checking Online for %s...' % show, settings.icon, settings.time_noti)
                    url_search = '%s/lib/search.php?value=%s&nextid=%s' % (
                        settings.url_address, show.replace(' ', '+'), cm)  # search for the anime
                    settings.log('[%s]%s' % (settings.name_provider_clean, url_search))
                    browser.open(url_search)
                    data = browser.content
                    cm += 1
                    if cm % 5: sleep(500)
                    if data is not None and len(data) > 0:
                        zip_list = zip(re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data), re.findall('<i>(.*?)<', data))
                        for quality in quality_keys:
                            for (magnet, name_file) in zip_list:
                                if quality.lower() in name_file.lower():
                                    magnet_list.append(magnet)
                                    name_file = name_file.replace('_', ' ')
                                    pos = name_file.rfind('- ')
                                    name_file = name_file[:pos] + 'EP' + name_file[pos + 2:]  # insert EP to be identificated in kodi
                                    file_list.append(name_file)
                    else:
                        loop = False
            if len(file_list) > 0:
                tools.integration(filename=file_list, magnet=magnet_list, type_list='SHOW',
                              folder=settings.show_folder, name_provider=settings.name_provider)
    if rep == 4:  # Update
        if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Checking Online...', settings.icon, settings.time_noti)
        if len(List_shows) > 0:
            quality_options = ['720p:1080p', '1080p:720p', '480p:720p:1080p', '1080p:720p:480p', '480p', '720p', '1080p']
            quality_ret = settings.dialog.select('Quality:', quality_options)
            quality_keys = quality_options[quality_ret].lower().split(":")
            magnet_list = []
            file_list = []
            url_search = '%s/lib/latest.php' % settings.url_address
            if browser.open(url_search):
                data = browser.content
                zip_list = zip(re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data), re.findall('<i>(.*?)<', data))
                for quality in quality_keys:
                    for (magnet, name_file) in zip_list:
                        for show in List_shows:
                            if show.lower() in name_file.lower() and quality.lower() in name_file.lower():
                                name_file = name_file.replace('_', ' ')
                                magnet_list.append(magnet)
                                pos = name_file.rfind('- ')
                                name_file = name_file[:pos] + 'EP' + name_file[
                                                                     pos + 2:]  # insert EP to be identificated in kodi
                                file_list.append(name_file)
                tools.integration(filename=file_list, magnet=magnet_list, type_list='ANIME', folder=settings.show_folder, name_provider=settings.name_provider)
            else:
                settings.log('[%s]>>>>>>>%s<<<<<<<' % (settings.name_provider_clean, browser.status))
                settings.dialog.notification(settings.name_provider, browser.status, settings.icon, 1000)
        else:
            if settings.time_noti > 0: settings.dialog.notification(settings.name_provider, 'Empty List', settings.icon, settings.time_noti)
    if rep == 5:  # Settings
        settings.settings.openSettings()
        settings = tools.Settings(anime=True)
    if rep == 6:  # Help
            settings.dialog.ok("Help", "Please, check this address to find the user's operation:\n[B]http://goo.gl/8nYU6R[/B]")

#save the list
with open(path + 'HorribleSubs2PULSAR.txt', "w") as text_file:  # create .strm
    text_file.writelines(list("%s\n" % item for item in List_shows))
    text_file.close()
del settings
del browser
