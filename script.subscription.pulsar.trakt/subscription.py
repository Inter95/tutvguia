# library to access URL, translation title and filtering
__author__ = 'mancuniancol'
import re 
import xbmcaddon
import xbmc
import xbmcgui
import os
import time
from ast import literal_eval


class Settings:
    def __init__(self):
        self.dialog = xbmcgui.Dialog()
        self.settings = xbmcaddon.Addon()
        self.id_addon = self.settings.getAddonInfo('id')  # gets name
        self.icon = self.settings.getAddonInfo('icon')
        self.path = self.settings.getAddonInfo('path')
        self.name_provider = self.settings.getAddonInfo('name')  # gets name
        self.name_provider_clean = re.sub('.COLOR (.*?)]', '', self.name_provider.replace('[/COLOR]', ''))
        self.time_noti = int(self.settings.getSetting('time_noti'))
        self.log = xbmc.log
        type_library = self.settings.getSetting('type_library')
        if "Local"in type_library:
            self.settings.setSetting('library', self.name_provider_clean)
        else:
            self.settings.setSetting('library', 'global')
        self.movie_folder = self.settings.getSetting('movie_folder')
        self.show_folder = self.settings.getSetting('show_folder')
        if self.movie_folder == '':
            self.movie_folder = 'special://temp/movies/'
        if  self.show_folder == '':
            self.show_folder = 'special://temp/shows/'
        # remove .strm
        self.remove_strm = self.settings.getSetting('remove_strm')
        self.library = self.settings.getSetting('library')
        if self.remove_strm == 'true':
                self.dialog.notification(self.name_provider, 'Removing .strm files...', self.icon, 1000)
                path = xbmc.translatePath('special://temp')
                database = {}
                try:
                    with open(path + 'pulsar-subscription-%s.txt' % self.library, 'r') as fp:
                        for line in fp:
                            listedline = line.strip().split('::')  # split around the :: sign
                            if len(listedline) > 1:  # we have the : sign in there
                                database[listedline[0]] = listedline[1]
                except:
                    pass
                for item in database:
                    data = literal_eval(database[item])
                    if os.path.exists(data['path']):
                        if '.strm' in data['path']:
                                os.remove(data['path'])
                        else:
                            files = os.listdir(data['path'])
                            for file in files:
                                if '.strm' in file and os.path.exists(data['path'] + file):
                                    os.remove(data['path'] + file)
                xbmc.log('All .strm files removed!', xbmc.LOGINFO)
                self.dialog.notification(self.name_provider, 'All .strm files removed!', self.icon, 1000)
                self.settings.setSetting('remove_strm', 'false')
        # clear the database
        self.clear_database = self.settings.getSetting('clear_database')
        if self.clear_database == 'true':
            self.dialog.notification(self.name_provider, 'Erasing Database...', self.icon, 1000)
            path = xbmc.translatePath('special://temp')
            try:
                os.remove(path + 'pulsar-subscription-%s.txt' % self.library)
            except OSError:
                pass
            self.settings.setSetting('clear_database', 'false')
        # rest
        self.number_files = int('0%s' % self.settings.getSetting('number_files'))
        self.dialog = xbmcgui.Dialog()

class Browser:
    def __init__(self):
        import cookielib
        self._cookies = None
        self.cookies = cookielib.LWPCookieJar()
        self.content = None
        self.status = ''

    def create_cookies(self, payload):
        import urllib
        self._cookies = urllib.urlencode(payload)

    def open(self,url):
        import urllib2
        result = True
        if self._cookies is not None:
            req = urllib2.Request(url,self._cookies)
            self._cookies = None
        else:
            req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')
        req.add_header("Accept-Encoding", "gzip")
        req.add_header("Accept-Language", "en-us")
        req.add_header("Content-Language", "en-us")  # get information in english
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))#open cookie jar
        try:
            response = opener.open(req)  # send cookies and open url
            #borrow from provider.py Steeve
            if response.headers.get("Content-Encoding", "") == "gzip":
                import zlib
                self.content = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(response.read())
            else:
                self.content = response.read()
            response.close()
            self.status = "200"
        except urllib2.URLError as e:
            self.status = str(e.reason)
            result = False
        except urllib2.HTTPError as e:
            self.status = str(e.code)
            result = False
        except:
            self.status = 'URL unreachable'
            result = False
        return result

    def login(self, url, payload={}, word=None):
        result = False
        self.create_cookies(payload)
        if self.open(url):
            result = True
            data = self.content
            if word is not None:
                if word in data:
                    self.status = 'Wrong Username or Password'
                    result = False
        return result


# find the name in different language
def translator(imdb_id, language):
    import unicodedata
    import json
    browser1 = Browser()
    keywords = {'en': '', 'de': '', 'es': 'espa', 'fr': 'french', 'it': 'italian', 'pt': 'portug'}
    url_themoviedb = "http://api.themoviedb.org/3/find/%s?api_key=8d0e4dca86c779f4157fc2c469c372ca&language=%s&external_source=imdb_id" % (imdb_id, language)
    if browser1.open(url_themoviedb):
        movie = json.loads(browser1.content)
        title0 = movie['movie_results'][0]['title'].replace(u'\xf1', '*')
        title_normalize = unicodedata.normalize('NFKD', title0)
        title = title_normalize.encode('ascii', 'ignore').replace(':', '')
        title = title.decode('utf-8').replace('*', u'\xf1').encode('utf-8')
        original_title = movie['movie_results'][0]['original_title']
        if title == original_title:
            title += ' ' + keywords[language]
    else:
        title = 'Pas de communication avec le themoviedb.org'
    return title.rstrip()


class TV_Show():
    def __init__(self, name):
        import json
        import urllib

        browser = Browser()
        if browser.open('http://localhost:65251/shows/search?q=%s' % urllib.quote(name)):
            data = json.loads(browser.content)
            if len(data['items']) > 0:
                self.code = data['items'][0]['path'].replace('plugin://plugin.video.pulsar/show/','').replace('/seasons','')
                time.sleep(0.002)
                browser.open('http://localhost:65251/show/%s/seasons' % self.code)
                try:
                    data = json.loads(browser.content)
                except:
                    data = {}
                    data['items'] = []
                seasons =[]
                for item in data['items']:
                    seasons.append(int(item['label'].replace('Season ','').replace('Specials', '0')))
                seasons.sort()
                episodes = {}
                for season in seasons:
                    time.sleep(0.002)
                    browser.open('http://localhost:65251/show/%s/season/%s/episodes' % (self.code, season))
                    data = json.loads(browser.content)
                    episodes[season] = len(data['items'])
                if len(seasons) > 0:
                    self.first_season = seasons[0]
                    self.last_season = seasons[-1]
                else:
                    self.first_season = 0
                    self.last_season = 0
                self.last_episode = episodes
            else:
                self.code = None
        else:
            self.code =None
        del browser

class TV_Show_code():
    def __init__(self, code, episodes = {}, last_season=0):
        import json

        browser = Browser()
        self.code = code
        browser.open('http://localhost:65251/show/%s/seasons' % self.code)
        try:
            data = json.loads(browser.content)
        except:
            data = {}
            data['items'] = []
        seasons =[]
        for item in data['items']:
            seasons.append(int(item['label'].replace('Season ','').replace('Specials', '0')))
        seasons.sort()
        if episodes.has_key(0):
            del episodes[0]
        if last_season is not 0:
            del episodes[last_season]
        for season in seasons:
            if not episodes.has_key(season):
                time.sleep(0.002)
                browser.open('http://localhost:65251/show/%s/season/%s/episodes' % (self.code, season))
                data = json.loads(browser.content)
                episodes[season] = len(data['items'])
        if len(seasons) > 0:
            self.first_season = seasons[0]
            self.last_season = seasons[-1]
        else:
            self.first_season = 0
            self.last_season = 0
        self.last_episode = episodes
        del browser


class Movie():
    def __init__(self, name):
        import json
        import urllib

        if ')' in name and '(' in name:
            try:
                year_movie = int(name[name.find("(")+1:name.find(")")])
                name = name.replace('(%s)' % year_movie, '').rstrip()
            except:
                year_movie = None
        else:
            year_movie = None
        browser = Browser()
        time.sleep(0.002)
        if browser.open('http://localhost:65251/movies/search?q=%s' % urllib.quote(name)):
            data = json.loads(browser.content)
            if len(data['items']) > 0:
                if year_movie is not None:
                    for movie in data['items']:
                        label = movie['label']
                        path = movie['path']
                        if movie['info'].has_key('year'):
                            year = movie['info']['year']
                        else:
                            year = 0000
                        if year == year_movie:
                            break
                else:
                    label = data['items'][0]['label']
                    path = data['items'][0]['path']
                    year = data['items'][0]['info']['year']
                self.code = path.replace('plugin://plugin.video.pulsar/movie/', '').replace('/play', '')
                self.label = label
            else:
                self.code = None
                self.label = name
        else:
            self.code = None
            self.label = name
        del browser


def normalize(name):
    from unicodedata import normalize
    import types
    if type(name) == types.StringType:
        unicode_name = name.decode('unicode-escape')
    else:
        unicode_name = name
    normalize_name = normalize('NFKD', unicode_name)
    return normalize_name.encode('ascii', 'ignore')


def uncode_name(name):  # convert all the &# codes to char, remove extra-space and normalize
    from HTMLParser import HTMLParser
    name = name.replace('<![CDATA[', '').replace(']]', '')
    name = HTMLParser().unescape(name.lower())
    return name


def safe_name(value):  # make the name directory and filename safe
    value = uncode_name(value)
    value = normalize(value)
    keys = {'"': ' ', '*': ' ', '/': ' ', ':': ' ', '<': ' ', '>': ' ', '?': ' ', '|': ' '}
    for key in keys.keys():
        value = value.replace(key, keys[key])
    value = ' '.join(value.split())
    return value


def format_title(value=''):
    import re
    value = value.replace('.', ' ').replace(')', ' ').replace('(', ' ').replace('[', ' ').replace(']', ' ').replace('-', ' ')
    value = safe_name(value)
    formats = ['ep[0-9]+', 's[0-9]+e[0-9]+', 's[0-9]+ e[0-9]+', '[0-9]+x[0-9]+', '[0-9][0-9][0-9][0-9] [0-9][0-9] [0-9][0-9]',
               '[0-9][0-9] [0-9][0-9] [0-9][0-9]', 'season [0-9]+', 'season[0-9]+', 's[0-9][0-9]', 'temporada [0-9]+', 'temporada[0-9]+']
    for format in formats:
        sshow = re.search(format, value) # format shows
        if sshow is not None:
            break
    if sshow is None:
        # it is a movie
        value += ' 0000 '  # checking year
        syear = re.search(' [0-9][0-9][0-9][0-9] ', value)
        year = syear.group(0).strip()
        pos = value.find(year)
        if pos > 0:
            title = value[:pos].strip()
            rest =  value[pos + 5:].strip().replace('0000', '')
        else:
            title = value.replace('0000', '')
            rest = ''
        keywords = ['en 1080p', 'en 720p', 'en dvd', 'en dvdrip', 'en hdtv', 'en bluray', 'en blurayrip',
                     'en web', 'en rip', 'en ts screener', 'en screener','en cam', 'en camrip',
                     'en ts-screener', 'en hdrip', 'en microhd']
        keywords += ['1080p', '720p', 'dvd', 'dvdrip', 'hdtv', 'bluray', 'blurayrip', 'web',
                     'rip', 'ts screener', 'screener', 'cam', 'camrip', 'ts-screener', 'hdrip', 'microhd',
                     'brrip', 'blu', 'webrip', 'hdrip', 'bdrip', 'ita', 'eng', 'esp']
        while pos != -1:  # loop until doesn't have any keyword in the title
            value = title + ' '
            for keyword in keywords:  # checking keywords
                pos = value.find(' ' + keyword + ' ')
                if pos > 0:
                    title = value[:pos].strip()
                    rest = value[pos:].strip() + ' ' + rest
                    break
        #title = title.strip()
        clean_title = title
        if '0000' not in year:
            title += ' (' + year.strip() + ')'
        title = title.title().replace('Of', 'of').replace('De', 'de')
        clean_title = clean_title.title().replace('Of', 'of').replace('De', 'de')
        folder = title
        return {'title': title, 'folder': folder, 'rest': rest.strip(), 'type': 'MOVIE', 'clean_title': clean_title, 'year': year}
    else:
        # it is a show
        episode = sshow.group(0)
        title = value[:value.find(episode)].strip()
        rest = value[value.find(episode) + len(episode):].strip()
        title = title.strip()
        if 'x' in episode:
            episode = 's' + episode.replace('x', 'e')
        if 's' not in episode and 'e' not in episode:  # date format
            date = episode.split()
            if len(date[0]) == 4:  # yyyy-mm-dd format
                episode = episode.replace(' ', '-')  # date style episode talk shows
            else:  # dd mm yy format
                if int(date[2]) > 50:
                    date[2] = '19' + date[2]
                else:
                    date[2] = '20' + date[2]
                episode = date[2] + '-' + date[1] + '-' + date[0]
        episode = episode.replace(' ', '')  # remove spaces in the episode format
        folder = title.title().replace('Of', 'of')
        clean_title = folder
        title = folder + ' ' + episode.upper()
        year = 0000
        return {'title': title, 'folder': folder, 'rest': rest, 'type': 'SHOW', 'clean_title': clean_title, 'year': year}


def integration(listing=[], ID=[], type_list='', folder='', silence=False, message='', name_provider=''):
    folder = folder.replace('special://temp/', xbmc.translatePath('special://temp'))
    message_type = {'MOVIE': 'MOVIES', 'SHOW': 'EPISODES'}
    dialog = xbmcgui.Dialog()
    action = xbmcaddon.Addon().getSetting('action')  # gets action
    specials = xbmcaddon.Addon().getSetting('specials')  # gets specials
    detailed_log = xbmcaddon.Addon().getSetting('detailed_log')
    library = xbmcaddon.Addon().getSetting('library')
    time_noti = int(xbmcaddon.Addon().getSetting('time_noti'))
    if name_provider!='':
        name_provider_clean= re.sub('.COLOR (.*?)]', '', name_provider.replace('[/COLOR]', ''))
    total = len(listing)
    if total > 0:
        if not silence:
            answer = dialog.yesno('%s: %s items\nDo you want to subscribe this list?' % (name_provider, total), '%s' % listing)
        else:
            answer = True
        if answer:
            pDialog = xbmcgui.DialogProgress()
            if not silence:
                pDialog.create(name_provider, 'Checking for %s\n%s' % (message_type[type_list], message))
            else:
                if time_noti > 0: dialog.notification(name_provider, 'Checking for %s\n%s' % (message_type[type_list], message), xbmcgui.NOTIFICATION_INFO, time_noti)
            #get the database
            database = {}
            path = xbmc.translatePath('special://temp')
            try:
                with open(path + 'pulsar-subscription-%s.txt' % library, 'r') as fp:
                    for line in fp:
                        listedline = line.strip().split('::')  # split around the :: sign
                        if len(listedline) > 1:  # we have the : sign in there
                            database[listedline[0]] = listedline[1]
            except:
                pass
            cont = 0
            directory = ''
            for cm, item_list in enumerate(listing):
                info = format_title(item_list)
                if type_list == 'MOVIE':
                    item = info['title']
                else:
                    item = info['clean_title']
                if database.has_key(item):
                    data = literal_eval(database[item])
                    if type_list == 'SHOW':  # update the database to find new episodes
                        tv_show = TV_Show_code(data['ID'], data['last_episode'], data['last_season'])
                        data['first_season'] = tv_show.first_season
                        data['last_season'] = tv_show.last_season
                        data['last_episode'] = tv_show.last_episode
                else:
                    # create the item
                    data = {}
                    if len(ID) > 0:
                        data['ID'] = ID[cm]
                        if type_list == 'SHOW':
                            tv_show = TV_Show_code(ID[cm])
                            data['first_season'] = tv_show.first_season
                            data['last_season'] = tv_show.last_season
                            data['last_episode'] = tv_show.last_episode
                    else:
                        if type_list == 'MOVIE':
                            movie = Movie(item)  # name of the movie with (year) format: Frozen (2013)
                            data['ID'] = movie.code  # search the IMDB id
                        elif type_list == 'SHOW':
                            tv_show = TV_Show(info['clean_title']) # search the name without year
                            data['ID'] = tv_show.code
                            if data['ID'] is not None:
                                data['first_season'] = tv_show.first_season
                                data['last_season'] = tv_show.last_season
                                data['last_episode'] = tv_show.last_episode
                    data['type'] = type_list
                    data['season'] = 0
                    data['episode'] = 0
                #start to create strm files
                if type_list == 'MOVIE' and data['type'] == 'MOVIE' and data['episode'] == 0 and data['ID'] is not None:  # add movies
                    cont += 1
                    directory = folder + item + folder[-1]
                    data['path'] = directory
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    if detailed_log == 'true':
                        xbmc.log('[%s] Code %s=%s' % (name_provider_clean,type_list, data['ID']))
                    link = 'plugin://plugin.video.pulsar/movie/%s/%s' % (data['ID'], action)
                    with open("%s%s.strm" % (directory, item), "w") as text_file:  # create .strm
                        text_file.write(link)
                    data['path'] = '%s%s.strm' % (directory, item)
                    data['episode'] = 1
                    if not silence: pDialog.update(int(float(cm) / total * 100), 'Creating %s%s.strm...' % (directory, item))
                    if cont % 100 == 0 and time_noti > 0:
                        dialog.notification(name_provider, '%s %s found - Still working...\n%s'
                                            % (cont, message_type[type_list], message), xbmcgui.NOTIFICATION_INFO, time_noti)
                    xbmc.log('[%s]%s%s.strm added' % (name_provider_clean, directory, item))
                elif type_list == 'SHOW' and data['type'] == 'SHOW' and data['ID'] is not None:  # add shows
                    if specials == 'false' and data['first_season'] == 0:
                        data['first_season'] = 1
                    directory = folder + item + folder[-1]
                    data['path'] = directory
                    if not os.path.exists(directory):
                        try:
                            os.makedirs(directory)
                        except:
                            pass
                    if detailed_log == 'true':
                        xbmc.log('[%s] Code %s=%s\n%s' % (name_provider_clean, type_list, data['ID'], message))
                        xbmc.log('[%s] %s %s-%s: %s' % (name_provider_clean, item, data['first_season'], data['last_season'], data['last_episode']))
                    for season in range(max(data['season'], data['first_season']), data['last_season'] + 1):
                        for episode in range(data['episode'] + 1, data['last_episode'][season] + 1):
                            cont += 1
                            link = 'plugin://plugin.video.pulsar/show/%s/season/%s/episode/%s/%s' % (data['ID'], season, episode, action)
                            if not silence: pDialog.update(int(float(cm) / total * 100), "%s%s S%02dE%02d.strm" % (directory, item, season, episode))
                            if cont % 100 == 0 and time_noti > 0:
                                dialog.notification(name_provider, '%s %s found - Still working...\n%s'
                                                    % (cont, message_type[type_list], message), xbmcgui.NOTIFICATION_INFO, time_noti)
                            with open("%s%s S%02dE%02d.strm" % (directory, item, season, episode), "w") as text_file:  # create .strm
                                text_file.write(link)
                                xbmc.log('[%s] %s S%02dE%02d.strm added' % (name_provider_clean, item, season, episode))
                                if not silence:
                                    if pDialog.iscanceled():
                                        break
                        data['episode'] = 0 # change to new season and reset the episode to 1
                        if not silence:
                            if pDialog.iscanceled():
                                break
                    data['season'] = data['last_season']
                    if data['last_episode'].has_key(data['last_season']):
                        data['episode'] = data['last_episode'][data['last_season']]
                    if not silence: pDialog.update(int(float(cm) / total * 100), 'Creating %s%s.strm...' % (directory, item))
                    xbmc.log('[%s]%s%s.strm added' % (name_provider_clean, directory, item))
                # update database
                if data['ID'] is not None:
                    database[item] = data
                if not silence:
                    if pDialog.iscanceled():
                        break
            # confirmation and close database
            with open(path + 'pulsar-subscription-%s.txt' % library, 'w') as fp:
                for p in database.items():
                    fp.write("%s::%s\n" % p)
            if not silence: pDialog.close()
            del pDialog
            if cont > 0:
                if not xbmc.getCondVisibility('Library.IsScanningVideo'):
                    xbmc.executebuiltin('XBMC.UpdateLibrary(video)')  # update the library with the new information
                xbmc.log('[%s]%s %s added./n%s' % (name_provider_clean, cont, message_type[type_list], message))
                if not silence:
                    dialog.ok(name_provider, '%s %s added.\n%s' % (cont, message_type[type_list], message))
                else:
                    if time_noti > 0: dialog.notification(name_provider, '%s %s added.\n%s' % (cont, message_type[type_list], message), xbmcgui.NOTIFICATION_INFO, time_noti)
            else:
                xbmc.log('[%s] No new %s\n%s' % (name_provider_clean, message_type[type_list], message))
                if not silence:
                    dialog.ok(name_provider, 'No new %s\n%s' % (message_type[type_list], message))
                else:
                    if time_noti > 0: dialog.notification(name_provider, 'No new %s\n%s' % (message_type[type_list], message), xbmcgui.NOTIFICATION_INFO, time_noti)
    else:
        xbmc.log('[%s] Empty List' % name_provider_clean)
        if not silence: dialog.ok(name_provider, 'Empty List! Try another one, please')
    del dialog