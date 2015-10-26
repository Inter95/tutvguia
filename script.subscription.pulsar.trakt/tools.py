# coding: utf-8
# library to access URL, translation title and filtering
__author__ = 'mancuniancol'

import os
import bs4
import requests
import re
import xbmcaddon
import xbmc
import xbmcgui
from os import path
from urllib import quote_plus
from time import sleep
from ast import literal_eval


################################
#### SCRAPER TITLES ############
################################
def normalize(name, onlyDecode=False):
    from unicodedata import normalize
    import types
    if type(name) == types.StringType:
        unicode_name = name.decode('unicode-escape')
    else:
        try:
            unicode_name = name.encode('latin-1').decode('utf-8')  # to latin-1
        except:
            unicode_name = name
    normalize_name = unicode_name if onlyDecode else normalize('NFKD', unicode_name)
    return normalize_name.encode('ascii', 'ignore')


def uncodeName(name):  # Convert all the &# codes to char, remove extra-space and normalize
    from HTMLParser import HTMLParser
    name = name.replace('<![CDATA[', '').replace(']]', '')
    name = HTMLParser().unescape(name.lower())
    return name


def unquoteName(name):  # Convert all %symbols to char
    from urllib import unquote
    return unquote(name).decode("utf-8")


def safeName(value):  # Make the name directory and filename safe
    value = normalize(value)  # First normalization
    value = unquoteName(value)
    value = uncodeName(value)
    value = normalize(value)  # Last normalization, because some unicode char could appear from the previous steps
    value = value.lower().title().replace('_', ' ')
    value = re.sub('- ([0-9][0-9][0-9][0-9]) ', ' \g<1>', value + " ")
    value = re.sub('- ([0-9]+) ', '- EP\g<1>', value + " ")
    value = re.sub('  ([0-9]+) ', '- EP\g<1>', value + " ")
    keys = {'"': ' ', '*': ' ', '/': ' ', ':': ' ', '<': ' ', '>': ' ', '?': ' ', '|': ' ',
            "'": '', 'Of': 'of', 'De': 'de', '.': ' ', ')': ' ', '(': ' ', '[': ' ', ']': ' ', '-': ' '}
    for key in keys.keys():
        value = value.replace(key, keys[key])
    value = ' '.join(value.split())
    return value.replace('S H I E L D', 'SHIELD')


def checkQuality(text=""):
    # quality
    quality = "480p"
    if "480p" in text:
        quality = "480p"
    if "720p" in text:
        quality = "720p"
    if "1080p" in text:
        quality = "1080p"
    if "3d" in text:
        quality = "3D"
    return quality


def width(quality="480p"):
    result = 720
    if '480p' in quality:
        result = 720
    elif '720p' in quality:
        result = 1280
    elif '1080p' in quality:
        result = 1920
    elif '3D' in quality:
        result = 1920
    return result

def height(quality="480p"):
    result = 480
    if '480p' in quality:
        result = 480
    elif '720p' in quality:
        result = 720
    elif '1080p' in quality:
        result = 1080
    elif '3D' in quality:
        result = 1080
    return result


def findLanguage(value=""):
    language = ""  # It is english or unknown
    if "spa" in value or "spanish" in value or "espanol" in value:
        language = " Español "
    return language


def formatTitle(value=''):
    value = safeName(value).lower()
    formats = [' ep[0-9]+', ' s[0-9]+e[0-9]+', ' s[0-9]+ e[0-9]+', ' [0-9]+x[0-9]+',
               ' [0-9][0-9][0-9][0-9] [0-9][0-9] [0-9][0-9]',
               ' [0-9][0-9] [0-9][0-9] [0-9][0-9]', ' season [0-9]+', ' season[0-9]+', ' s[0-9][0-9]',
               ' temporada [0-9]+ capitulo [0-9]+', ' temporada[0-9]+',
               ' seizoen [0-9]+ afl [0-9]+'
               ]
    sshow = None
    for format in formats:  # search if it is a show
        sshow = re.search(format, value)  # format shows
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
            rest = value[pos + 5:].strip().replace('0000', '')
        else:
            title = value.replace('0000', '')
            rest = ''
        keywords = ['en 1080p', 'en 720p', 'en dvd', 'en dvdrip', 'en hdtv', 'en bluray', 'en blurayrip',
                    'en web', 'en rip', 'en ts screener', 'en screener', 'en cam', 'en camrip',
                    'en ts-screener', 'en hdrip', 'en microhd']
        keywords += ['1080p', '720p', 'dvd', 'dvdrip', 'hdtv', 'bluray', 'blurayrip', 'web',
                     'rip', 'ts screener', 'screener', 'cam', 'camrip', 'ts-screener', 'hdrip', 'microhd',
                     'brrip', 'blu', 'webrip', 'hdrip', 'bdrip', 'ita', 'eng', 'esp', "spanish espanol"]

        while pos != -1:  # loop until doesn't have any keyword in the title
            value = title + ' '
            for keyword in keywords:  # checking keywords
                pos = value.find(' ' + keyword + ' ')
                if pos > 0:
                    title = value[:pos].strip()
                    rest = value[pos:].strip() + ' ' + rest
                    break

        cleanTitle = title
        if '0000' not in year:
            title += ' (' + year.strip() + ')'
        title = title.title().replace('Of', 'of').replace('De', 'de')
        cleanTitle = cleanTitle.title().replace('Of', 'of').replace('De', 'de')
        folder = title
        quality = checkQuality(rest)
        language = findLanguage(rest)
        return {'title': title, 'folder': folder, 'rest': rest.strip(), 'type': 'MOVIE', 'cleanTitle': cleanTitle,
                'year': year, 'quality': quality, 'height': height(quality), "width": width(quality),
                'language': language
                }
    else:
        # it is a show
        episode = sshow.group(0)
        title = value[:value.find(episode)].strip()
        rest = value[value.find(episode) + len(episode):].strip()
        title = title.strip()
        episode = episode.replace('temporada ', 's').replace(' capitulo ', 'e')
        episode = episode.replace('seizoen ', 's').replace(' afl ', 'e')

        if 'x' in episode:
            episode = 's' + episode.replace('x', 'e')

        if 's' in episode and 'e' in episode and 'season' not in episode:  # force S00E00 instead S0E0
            temp_episode = episode.replace('s', '').split('e')
            episode = 's%02de%02d' % (int(temp_episode[0]), int(temp_episode[1]))

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
        cleanTitle = folder
        title = folder + ' ' + episode.upper()
        year = 0000
        ttype = "SHOW"
        if bool(re.search("EP[0-9]+", title)):
            ttype = "ANIME"
        quality = checkQuality(rest)
        language = findLanguage(rest)
        return {'title': title, 'folder': folder, 'rest': rest, 'type': ttype, 'cleanTitle': cleanTitle,
                'year': year, 'quality': quality, 'height': int(quality.replace("p", "")), "width": width(quality),
                "language": language
                }


################################
#### CLASS #####################
################################
class Storage():
    def __init__(self, fileName="", type="list", eval=False):
        from ast import literal_eval
        self.path = os.path.join(xbmc.translatePath('special://temp'), fileName)
        self.type = type
        if type == "list":
            # get the list
            self.database = []
            try:
                with open(self.path, 'r') as fp:
                    for line in fp:
                        self.database.append(line.strip())
            except:
                pass
        elif type == "dict":
            # get the Dictionary
            self.database = {}
            try:
                with open(self.path, 'r') as fp:
                    for line in fp:
                        listedline = line.strip().split('::')  # split around the :: sign
                        if len(listedline) > 1:  # we have the : sign in there
                            self.database[listedline[0]] = listedline[1] if not eval else literal_eval(listedline[1])
            except:
                pass

    def destroy(self):  # Erase the database from the HD
        try:
            os.remove(self.path)
        except OSError:
            pass

    def add(self, key="", info=""):  # add element
        if self.type == "list" and key not in self.database:
            self.database.append(key)
        elif self.type == "dict":
            keySafe = formatTitle(key)
            self.database[keySafe['folder']] = info

    def remove(self, key=""):  # remove element
        if self.type == "list":
            self.database.remove(key)
        elif self.type == "dict":
            keySafe = formatTitle(key)
            del self.database[keySafe['folder']]

    def save(self):  # save the database
        if self.type == "list":
            # save the list
            with open(self.path, 'w') as fp:
                for p in self.database:
                    fp.write("%s\n" % p)
        elif self.type == "dict":
            # save the dictionary
            with open(self.path, 'w') as fp:
                for p in self.database.items():
                    fp.write("%s::%s\n" % p)


class Settings:  # Read Configuration's Addon
    def __init__(self, anime=False):
        # Objects
        self.dialog = xbmcgui.Dialog()
        self.pDialog = xbmcgui.DialogProgress()
        self.settings = xbmcaddon.Addon()

        # General information
        self.idAddon = self.settings.getAddonInfo('ID')  # gets name
        self.icon = self.settings.getAddonInfo('icon')
        self.fanart = self.settings.getAddonInfo('fanart')
        self.path = self.settings.getAddonInfo('path')
        self.name = self.settings.getAddonInfo('name')  # gets name
        self.cleanName = re.sub('.COLOR (.*?)]', '', self.name.replace('[/COLOR]', ''))
        self.storageName = self.cleanName + ".txt"  # Name Database

        # Everything else
        self.value = {}  # it contains all the settings from xml file
        self.value["movieFolder"] = ""
        self.value["showFolder"] = ""
        self.value["animeFolder"] = ""

        with open(path.join(self.path, "resources", "settings.xml"), 'r') as fp:
            data = fp.read()
        soup = bs4.BeautifulSoup(data)
        settings = soup.select("setting")
        for setting in settings:
            id = setting.attrs.get("id")
            if id is not None:
                self.value[id] = self.settings.getSetting(id)

        # Set-up Output folder
        self.movieFolder = self.__folder__(self.value["movieFolder"], "movies")
        self.showFolder = self.__folder__(self.value["showFolder"], "shows")
        self.animeFolder = self.__folder__(self.value["animeFolder"], "animes")

        # subscription
        if "subscription" in self.cleanName: self.__subscription__()

    def __folder__(self, folder, default=""):  # Change to OS friendly names
        if folder == '':  # define default folder
            folder = 'special://temp/%s/' % default
        folder = folder.replace('special://temp/', xbmc.translatePath('special://temp'))
        return folder.replace('smb:', '')  # network compatibility

    def __subscription__(self):  # Additional Code for Subscription List Scripts
        # remove .strm
        if self.value["removeStrm"] == 'true':
            self.notification('Removing .strm files...')
            if self.value["typeLibrary"] == "Global": self.storageName = "pulsar global subscription.txt"
            storage = Storage(self.storageName, type="dict")
            for item in storage.database:
                data = literal_eval(storage.database[item])
                if os.path.exists(data['path']):
                    if '.strm' in data['path']:
                        os.remove(data['path'])
                    else:
                        files = os.listdir(data['path'])
                        for file in files:
                            if '.strm' in file and os.path.exists(data['path'] + file):
                                os.remove(data['path'] + file)
            self.log('All .strm files removed!')
            self.notification('All .strm files removed!', force=True)
            self.settings.setSetting('removeStrm', 'false')
        # clear the database
        if self.value["clearDatabase"] == 'true':
            self.notification('Erasing Database...', force=True)
            storage = Storage(self.storageName, type="dict")
            storage.destroy()
            self.settings.setSetting('clearDatabase', 'false')

    def log(self, message=""):  # to write in the Kodi's log
        xbmc.log('[%s] %s' % (self.cleanName, message if message.startswith("http") else safeName(message)))

    def notification(self, message="", force=False):  # to display a message in Kodi
        if float(self.value["timeNotification"]) > 0 or force:
            xbmcgui.Dialog().notification(self.name, "%s" % message, self.icon,
                                          1000 if force else int(float(self.value["timeNotification"]) * 1000))

    def string(self, id):
        return self.settings.getLocalizedString(id)


# Create settings object and browser to be used in the other tool's functions
settings = Settings()
browser = requests.Session()
browser.headers[
    'User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'


class Filtering:
    def __init__(self):
        self.reason = ''
        self.title = ''
        self.quality_allow = ['*']
        self.quality_deny = []
        self.title = ''
        self.maxSize = 10.00  # 10 it is not limit
        self.minSize = 0.00

        # size
        if settings.value.has_key('movieMinSize'):  # there is size restrictions
            settings.value['movieMinSize'] = float(settings.value['movieMinSize'])
        else:
            settings.value['movieMinSize'] = 0.0
        self.movieMinSize = settings.value['movieMinSize']

        if settings.value.has_key('movieMaxSize'):  # there is size restrictions
            settings.value['movieMaxSize'] = float(settings.value['movieMaxSize'])
        else:
            settings.value['movieMaxSize'] = 10.0
        self.movieMaxSize = settings.value['movieMaxSize']

        if settings.value.has_key('tvMinSize'):  # there is size restrictions
            settings.value['tvMinSize'] = float(settings.value['movieMinSize'])
        else:
            settings.value['tvMinSize'] = 0.0
        self.tvMinSize = settings.value['tvMinSize']

        if settings.value.has_key('tvMaxSize'):  # there is size restrictions
            settings.value['tvMaxSize'] = float(settings.value['movieMaxSize'])
        else:
            settings.value['tvMaxSize'] = 10.0
        self.tvMaxSize = settings.value['tvMaxSize']

        # movie
        movieAllow = []
        if settings.value.has_key('movieKeyAllow') and settings.value['movieKeyAllow'] <> "":
            movieAllow = re.split(',', settings.value['movieKeyAllow'].replace(', ', ',').replace(' ,', ','))
        if settings.value.has_key('movieQua1') and settings.value['movieQua1'] == 'Accept File':
            movieAllow.append('480p')  # 480p
        if settings.value.has_key('movieQua2') and settings.value['movieQua2'] == 'Accept File':
            movieAllow.append('HDTV')  # HDTV
        if settings.value.has_key('movieQua3') and settings.value['movieQua3'] == 'Accept File':
            movieAllow.append('720p')  # 720p
        if settings.value.has_key('movieQua4') and settings.value['movieQua4'] == 'Accept File':
            movieAllow.append('1080p')  # 1080p
        if settings.value.has_key('movieQua5') and settings.value['movieQua5'] == 'Accept File':
            movieAllow.append('3D')  # 3D
        if settings.value.has_key('movieQua6') and settings.value['movieQua6'] == 'Accept File':
            movieAllow.append('CAM')  # CAM
        if settings.value.has_key('movieQua7') and settings.value['movieQua7'] == 'Accept File':
            movieAllow.extend(['TeleSync', ' TS '])  # TeleSync
        if settings.value.has_key('movieQua8') and settings.value['movieQua8'] == 'Accept File':
            movieAllow.append('Trailer')  # Trailer

        # Block File
        movieDeny = []
        if settings.value.has_key('movieKeyDenied') and settings.value['movieKeyDenied'] <> "":
            movieDeny = re.split(',', settings.value['movieKeyDenied'].replace(', ', ',').replace(' ,', ','))
        if settings.value.has_key('movieQua1') and settings.value['movieQua1'] == 'Block File':
            movieDeny.append('480p')  # 480p
        if settings.value.has_key('movieQua2') and settings.value['movieQua2'] == 'Block File':
            movieDeny.append('HDTV')  # HDTV
        if settings.value.has_key('movieQua3') and settings.value['movieQua3'] == 'Block File':
            movieDeny.append('720p')  # 720p
        if settings.value.has_key('movieQua4') and settings.value['movieQua4'] == 'Block File':
            movieDeny.append('1080p')  # 1080p
        if settings.value.has_key('movieQua5') and settings.value['movieQua5'] == 'Block File':
            movieDeny.append('3D')  # 3D
        if settings.value.has_key('movieQua6') and settings.value['movieQua6'] == 'Block File':
            movieDeny.append('CAM')  # CAM
        if settings.value.has_key('movieQua7') and settings.value['movieQua7'] == 'Block File':
            movieDeny.extend(['TeleSync', ' TS '])  # TeleSync
        if settings.value.has_key('movieQua8') and settings.value['movieQua8'] == 'Block File':
            movieDeny.append('Trailer')  # Trailer

        if '' in movieAllow: movieAllow.remove('')
        if '' in movieDeny: movieDeny.remove('')
        if len(movieAllow) == 0: movieAllow = ['*']
        self.movieAllow = movieAllow
        self.movieDeny = movieDeny

        # TV
        tvAllow = []
        if settings.value.has_key('tvKeyAllow'):
            tvAllow.append(re.split(',', settings.value['tvKeyAllow'].replace(', ', ',').replace(' ,', ',')))
        if settings.value.has_key('tvQua1') and settings.value['tvQua1'] == 'Accept File':
            tvAllow.append('480p')  # 480p
        if settings.value.has_key('tvQua2') and settings.value['tvQua2'] == 'Accept File':
            tvAllow.append('HDTV')  # HDTV
        if settings.value.has_key('tvQua3') and settings.value['tvQua3'] == 'Accept File':
            tvAllow.append('720p')  # 720p
        if settings.value.has_key('tvQua4') and settings.value['tvQua4'] == 'Accept File':
            tvAllow.append('1080p')  # 1080p

        # Block File
        tvDeny = []
        if settings.value.has_key('tvKeyDeny'):
            tvDeny.append(re.split(',', settings.value['tvKeyDeny'].replace(', ', ',').replace(' ,', ',')))
        if settings.value.has_key('tvQua1') and settings.value['tvQua1'] == 'Accept File':
            tvDeny.append('480p')  # 480p
        if settings.value.has_key('tvQua2') and settings.value['tvQua2'] == 'Accept File':
            tvDeny.append('HDTV')  # HDTV
        if settings.value.has_key('tvQua3') and settings.value['tvQua3'] == 'Accept File':
            tvDeny.append('720p')  # 720p
        if settings.value.has_key('tvQua4') and settings.value['tvQua4'] == 'Accept File':
            tvDeny.append('1080p')  # 1080p

        if '' in tvAllow: tvAllow.remove('')
        if '' in tvDeny: tvDeny.remove('')
        if len(tvAllow) == 0: tvAllow = ['*']
        self.tvAllow = tvAllow
        self.tvDeny = tvDeny

    def useMovie(self):
        self.qualityAllow = self.movieAllow
        self.qualityDeny = self.movieDeny
        self.minSize = self.movieMinSize
        self.maxSize = self.movieMaxSize

    def useTv(self):
        self.qualityAllow = self.tvAllow
        self.qualityDeny = self.tvDeny
        self.minSize = self.tvMinSize
        self.maxSize = self.tvMaxSize

    def information(self):
        settings.log('Accepted Keywords: %s' % str(self.quality_allow))
        settings.log('Blocked Keywords: %s' % str(self.quality_deny))
        settings.log('min Size: %s' % str(self.minSize) + ' GB')
        settings.log('max Size: %s' % str(self.maxSize) + ' GB') if self.maxSize != 10 else 'MAX'

    # validate keywords
    def included(self, value, keys, strict=False):
        value = ' ' + normalize(value) + ' '
        res = False
        if '*' in keys:
            res = True
        else:
            res1 = []
            for key in keys:
                res2 = []
                for item in re.split('\s', key):
                    item = normalize(item)
                    item = item.replace('?', ' ')
                    if strict: item = ' ' + item + ' '  # it makes that strict the comparation
                    if item.upper() in value.upper():
                        res2.append(True)
                    else:
                        res2.append(False)
                res1.append(all(res2))
            res = any(res1)
        return res

    # validate size
    def size_clearance(self, size):
        max_size1 = 100 if self.maxSize == 10 else self.maxSize
        res = False
        value = float(re.split('\s', size.replace(',', ''))[0])
        value *= 0.001 if 'M' in size else 1
        if self.minSize <= value <= max_size1:
            res = True
        return res

    # verify
    def verify(self, name, size):  # modify to just check quality and size, not name
        self.reason = name.replace(' - ' + settings.cleanName, '') + ' ***Blocked File by'
        result = True
        if name != None:
            if not self.included(name, self.qualityAllow) or self.included(name, self.qualityDeny):
                self.reason += ", Keyword"
                result = False
        if size != None:
            if not self.size_clearance(size):
                result = False
                self.reason += ", Size"
        self.reason = self.reason.replace('by,', 'by') + '***'
        return result


#######################################
######## CLASS FOR SUBSCRIPTION #######
#######################################
class TvShow():
    def __init__(self, name):
        import urllib

        browser.get('http://localhost:65251/shows/search?q=%s' % urllib.quote(name))
        sleep(0.2)
        response = browser.get('http://localhost:65251/shows/search?q=%s' % urllib.quote(name))
        if response.status_code == requests.codes.ok:
            data = response.json()
            dataShow = None
            if len(data['items']) > 0:  # To find the right Tv Show
                dataShow = data['items'][0]
                for item in data['items']:
                    if item['label'].lower() == name.lower():
                        dataShow = item
                        break
            if dataShow is not None:
                self.code = dataShow['path'].replace('plugin://plugin.video.pulsar/show/', '').replace(
                    '/seasons', '')
                sleep(0.2)
                response = browser.get('http://localhost:65251/show/%s/seasons' % self.code)
                data = {}
                try:
                    data = response.json()
                except:
                    data['items'] = []
                seasons = []
                for item in data['items']:
                    seasons.append(int(item['label'].replace('Season ', '').replace('Specials', '0')))
                seasons.sort()
                episodes = {}
                for season in seasons:
                    sleep(0.2)
                    response = browser.get('http://localhost:65251/show/%s/season/%s/episodes' % (self.code, season))
                    data = response.json()
                    episodes[season] = len(data['items'])
                if len(seasons) > 0:
                    self.firstSeason = seasons[0]
                    self.lastSeason = seasons[-1]
                else:
                    self.firstSeason = 0
                    self.lastSeason = 0
                self.lastEpisode = episodes
            else:
                self.code = None
        else:
            self.code = None


class TvShowCode():
    def __init__(self, code, episodes={}, lastSeason=0):
        self.code = code
        response = browser.get('http://localhost:65251/show/%s/seasons' % self.code)
        data = {}
        try:
            data = response.json()
        except:
            data['items'] = []
        seasons = []
        for item in data['items']:
            seasons.append(int(item['label'].replace('Season ', '').replace('Specials', '0')))
        seasons.sort()
        if episodes.has_key(0):
            del episodes[0]
        if lastSeason is not 0:
            del episodes[lastSeason]
        for season in seasons:
            if not episodes.has_key(season):
                sleep(0.2)
                response = browser.get('http://localhost:65251/show/%s/season/%s/episodes' % (self.code, season))
                data = response.json()
                episodes[season] = len(data['items'])
        if len(seasons) > 0:
            self.firstSeason = seasons[0]
            self.lastSeason = seasons[-1]
        else:
            self.firstSeason = 0
            self.lastSeason = 0
        self.lastEpisode = episodes


class Movie():
    def __init__(self, name):
        import urllib

        if ')' in name and '(' in name:
            try:
                yearMovie = int(name[name.find("(") + 1:name.find(")")])
                name = name.replace('(%s)' % yearMovie, '').rstrip()
            except:
                yearMovie = None
        else:
            yearMovie = None
        browser.get('http://localhost:65251/movies/search?q=%s' % urllib.quote(name))  # avoid not info
        sleep(0.2)
        response = browser.get('http://localhost:65251/movies/search?q=%s' % urllib.quote(name))
        if response.status_code == requests.codes.ok:
            data = response.json()
            if len(data['items']) > 0:
                if yearMovie is not None:
                    for movie in data['items']:
                        label = movie['label']
                        path = movie['path']
                        if movie['info'].has_key('year'):
                            year = movie['info']['year']
                        else:
                            year = 0000
                        if year == yearMovie:
                            break
                else:
                    label = data['items'][0]['label']
                    path = data['items'][0]['path']
                    year = data['items'][0]['info']['year']
                self.code = path.replace('plugin://plugin.video.pulsar/movie/', '').replace('/play', '')
                self.label = label
                self.year = year
            else:
                self.code = None
                self.label = name
        else:
            self.code = None
            self.label = name


################################
#### FUNCTIONS #################
################################
def printer(message=""):
    print '****************************'
    print message
    print '*-**************************'


def removeDirectory(folder):
    from os import listdir
    from xbmc import translatePath

    folder = folder.replace('special://temp/', translatePath('special://temp'))
    folder = folder.replace('smb:', '')  # network compatibility
    listFolders = listdir(folder)
    rep = settings.dialog.select('Select the Folder to erase:', listFolders + ['-CANCEL'])
    if rep < len(listFolders):
        if settings.dialog.yesno("Attention!", "Are you sure to erase?", nolabel="No", yeslabel="Yes"):
            __removeDirectory__(folder=folder, title=listFolders[rep])


def __removeDirectory__(folder="", title=""):
    info = formatTitle(title)
    directory = os.path.join(folder, info['folder'])
    if os.path.exists(directory):
        import shutil
        shutil.rmtree(directory, ignore_errors=True)
    if not xbmc.getCondVisibility('Library.IsScanningVideo'):
        xbmc.executebuiltin('XBMC.CleanLibrary(video)')  # clean the library


############  INTEGRATION   ###########################
def integration(titles=[], id=[], magnets=[], typeList='', folder='', silence=False, message=''):
    messageType = {'MOVIE': settings.string(32031), 'SHOW': settings.string(32032), 'ANIME': settings.string(32043)}
    filters = Filtering()  # start filtering
    if typeList == 'MOVIE':
        filters.useMovie()
    else:
        filters.useTv()  # TV SHOWS and Anime
    filters.information()

    total = len(titles)
    answer = True
    if not silence:
        answer = settings.dialog.yesno(settings.string(32033) %
                                       (settings.name, total), '%s' % titles)
    if answer:  # it will integrate the filename list to the local library
        if not silence:
            settings.pDialog.create(settings.name, settings.string(32034) % (messageType[typeList], message))
        else:
            settings.notification(settings.string(32034) % (messageType[typeList], message))

        cont = 0
        for cm, title in enumerate(titles):
            info = formatTitle(title)
            info['folder'] = info['folder'][:100]  # to limit the length of directory name
            check = True
            detailsTitle = ''
            if len(info['rest']) > 0:  # check for quality filtering
                filters.title = info['title'] + ' ' + info['rest']
                if filters.verify(filters.title, None):  # just check the quality no more
                    check = True
                    if settings.value["duplicated"] == 'true':
                        detailsTitle = ' ' + info['rest']
                else:
                    check = False
            if check:  # the file has passed the filtering
                name = info['title'] + detailsTitle
                name = name[:99]  # to limit the length of name

                # Try to create the directory if it doesn't exist
                directory = path.join(folder, info['folder'])
                try:
                    os.makedirs(directory)
                except:
                    pass

                # Set-up the plugin
                uri_string = quote_plus(uncodeName(magnets[cm]))
                if settings.value["plugin"] == 'Pulsar':
                    link = 'plugin://plugin.video.pulsar/play?uri=%s' % uri_string
                elif settings.value["plugin"] == 'KmediaTorrent':
                    link = 'plugin://plugin.video.kmediatorrent/play/%s' % uri_string
                elif settings.value["plugin"] == "Torrenter":
                    link = 'plugin://plugin.video.torrenter/?action=playSTRM&url=' + uri_string + \
                           '&not_download_only=True'
                elif settings.value["plugin"] == "YATP":
                    link = 'plugin://plugin.video.yatp/?action=play&torrent=' + uri_string
                else:
                    link = 'plugin://plugin.video.xbmctorrent/play/%s' % uri_string

                # start to create the strm file
                filename = path.join(directory, name + ".strm")
                if not os.path.isfile(filename) or settings.value["overwrite"] == 'true':
                    cont += 1  # add new file's count
                    with open(filename, "w") as text_file:  # create .strm
                        text_file.write(link)
                    if len(id) > 0 and id[cm] != "":
                        if typeList == "MOVIE":
                            with open(filename.replace(".strm", ".nfo"), "w") as text_file:  # create .nfo MOVIE
                                text_file.write("http://www.imdb.com/title/%s/" % id[cm])
                        else:
                            with open(path.join(directory, "tvshow.nfo"), "w") as text_file:  # create .nfo SHOW
                                text_file.write("http://thetvdb.com/?tab=series&id=%s" % id[cm])

                    if not silence: settings.pDialog.update(int(float(cm) / total * 100), settings.string(32036)
                                                            % (directory, name))
                    if not silence and settings.pDialog.iscanceled(): break
                    if cont % 100 == 0: settings.notification(
                        settings.string(32037) % (cont, messageType[typeList], message))
                    settings.log(settings.string(32038) % filename)
                if not silence and settings.pDialog.iscanceled(): break
        if not silence: settings.pDialog.close()

        if cont > 0:  # There are files added
            if not xbmc.getCondVisibility('Library.IsScanningVideo'):
                xbmc.executebuiltin('XBMC.UpdateLibrary(video)')  # update the library with the new information
            settings.log(settings.string(32040) % (cont, messageType[typeList], message))
            if not silence:
                settings.dialog.ok(settings.name, settings.string(32040) % (cont, messageType[typeList], message))
            else:
                settings.notification(settings.string(32040) % (cont, messageType[typeList], message))
        else:
            settings.log(settings.string(32041) % (messageType[typeList], message))
            if not silence:
                settings.dialog.ok(settings.name, settings.string(32042) % (messageType[typeList], message))
            else:
                settings.notification(settings.string(32042) % (messageType[typeList], message))
                # del filters


############  SUBSCRIPTION   ###########################
def subscription(titles=[], id=[], typeList='', folder='', silence=False, message=''):
    messageType = {'MOVIE': settings.string(32031), 'SHOW': settings.string(32032)}
    total = len(titles)
    answer = True
    if not silence:
        answer = settings.dialog.yesno(settings.string(32033) %
                                       (settings.name, total), '%s' % titles)

    if answer:  # it will integrate the filename list to the local library
        if not silence:
            settings.pDialog.create(settings.name, settings.string(32034) % (messageType[typeList], message))
        else:
            settings.notification(settings.string(32034) % (messageType[typeList], message))
        # Open Database
        storage = Storage(settings.storageName, type="dict")
        cont = 0
        for cm, item_list in enumerate(titles):
            info = formatTitle(item_list)
            item = info['title'] if typeList == 'MOVIE' else info['cleanTitle']
            if storage.database.has_key(item):
                data = literal_eval(storage.database[item])
                if typeList == 'SHOW':  # update the database to find new episodes
                    tvShow = TvShowCode(data['ID'], data['lastEpisode'], data['lastSeason'])
                    data['firstSeason'] = tvShow.firstSeason
                    data['lastSeason'] = tvShow.lastSeason
                    data['lastEpisode'] = tvShow.lastEpisode
            else:
                # create the item
                data = {}
                if len(id) > 0:
                    data['ID'] = id[cm]
                    if typeList == 'SHOW':
                        tvShow = TvShowCode(id[cm])
                        data['firstSeason'] = tvShow.firstSeason
                        data['lastSeason'] = tvShow.lastSeason
                        data['lastEpisode'] = tvShow.lastEpisode
                else:
                    if typeList == 'MOVIE':
                        movie = Movie(item)  # name of the movie with (year) format: Frozen (2013)
                        data['ID'] = movie.code  # search the IMDB id
                    elif typeList == 'SHOW':
                        tvShow = TvShow(info['cleanTitle'])  # search the name without year
                        data['ID'] = tvShow.code
                        if data['ID'] is not None:
                            data['firstSeason'] = tvShow.firstSeason
                            data['lastSeason'] = tvShow.lastSeason
                            data['lastEpisode'] = tvShow.lastEpisode
                data['type'] = typeList
                data['season'] = 0
                data['episode'] = 0
            # start to create strm files
            if typeList == 'MOVIE' and data['type'] == 'MOVIE' and data['episode'] == 0 and data['ID'] is not None:
                cont += 1
                # Try to create the directory if it doesn't exist
                directory = path.join(folder, info['folder'])
                try:
                    os.makedirs(directory)
                except:
                    pass
                data['path'] = directory  # To be able to erase the folder

                if settings.value["detailedLog"] == 'true':
                    settings.log('Code %s=%s' % (typeList, data['ID']))

                link = 'plugin://plugin.video.pulsar/movie/%s/%s' % (data['ID'], settings.value["action"])

                # start to create the strm file
                filename = path.join(directory, item + ".strm")
                with open(filename, "w") as text_file:  # create .strm MOVIE
                    text_file.write(link)
                with open(filename.replace(".strm", ".nfo"), "w") as text_file:  # create .nfo MOVIE
                    text_file.write("http://www.imdb.com/title/%s/" % data['ID'])
                data['path'] = filename
                data['episode'] = 1
                if not silence: settings.pDialog.update(int(float(cm) / total * 100), settings.string(32036)
                                                        % (directory, item))
                if cont % 100 == 0: settings.notification(settings.string(32037)
                                                          % (cont, messageType[typeList], message))
                settings.log(settings.string(32038) % filename)
            elif typeList == 'SHOW' and data['type'] == 'SHOW' and data['ID'] is not None:  # add shows
                if settings.value["specials"] == 'false' and data['firstSeason'] == 0:
                    data['firstSeason'] = 1
                directory = folder + item + folder[-1]
                # Try to create the directory if it doesn't exist
                directory = path.join(folder, info['folder'])
                try:
                    os.makedirs(directory)
                except:
                    pass
                data['path'] = directory  # To be able to erase the folder
                if settings.value["detailedLog"] == 'true':
                    settings.log(settings.string(32035) % (typeList, data['ID'], message))
                    settings.log(
                        '%s %s-%s: %s' % (item, data['firstSeason'], data['lastSeason'], data['lastEpisode']))
                with open(path.join(directory, "tvshow.nfo"), "w") as text_file:  # create .nfo SHOW
                    text_file.write("http://thetvdb.com/?tab=series&id=%s" % data['ID'])
                for season in range(max(data['season'], data['firstSeason']), data['lastSeason'] + 1):
                    for episode in range(data['episode'] + 1, data['lastEpisode'][season] + 1):
                        cont += 1
                        link = 'plugin://plugin.video.pulsar/show/%s/season/%s/episode/%s/%s' % (
                            data['ID'], season, episode, settings.value["action"])
                        if not silence: settings.pDialog.update(int(float(cm) / total * 100),
                                                                "%s%s S%02dE%02d.strm" % (
                                                                    directory, item, season, episode))
                        if cont % 100 == 0: settings.notification(
                            settings.string(32037) % (cont, messageType[typeList], message))
                        filename = path.join(directory, item + " S%02dE%02d.strm" % (season, episode))
                        with open(filename, "w") as text_file:  # create .strm
                            text_file.write(link)
                            settings.log(settings.string(32038) % filename)
                        if not silence and settings.pDialog.iscanceled(): break
                    data['episode'] = 0  # change to new season and reset the episode to 1
                if not silence and settings.pDialog.iscanceled(): break
                data['season'] = data['lastSeason']
                if data['lastEpisode'].has_key(data['lastSeason']):
                    data['episode'] = data['lastEpisode'][data['lastSeason']]
                if not silence: settings.pDialog.update(int(float(cm) / total * 100),
                                                        settings.string(32036) % (directory, item))
                settings.log(settings.string(32039) % (directory, item))
            # update database
            if data['ID'] is not None:
                storage.database[item] = data
            if not silence and settings.pDialog.iscanceled(): break
        # confirmation and close database
        storage.save()
        if cont > 0:
            if not xbmc.getCondVisibility('Library.IsScanningVideo'):
                xbmc.executebuiltin('XBMC.UpdateLibrary(video)')  # update the library with the new information
            settings.log(settings.string(32040) % (cont, messageType[typeList], message))
            if not silence:
                settings.dialog.ok(settings.name, settings.string(32040) % (cont, messageType[typeList], message))
            else:
                settings.notification(settings.string(32040) % (cont, messageType[typeList], message))

        else:
            settings.log(settings.string(32041) % (messageType[typeList], message))
            if not silence:
                settings.dialog.ok(settings.name, settings.string(32042) % (messageType[typeList], message))
            else:
                settings.notification(settings.string(32042) % (messageType[typeList], message))
        del storage
