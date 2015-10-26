# library to access URL, translation title and filtering
__author__ = 'mancuniancol'
import re
import os

import xbmcaddon
import xbmc
import xbmcgui


class Settings:
    def __init__(self, anime=False):
        self.dialog = xbmcgui.Dialog()
        self.settings = xbmcaddon.Addon()
        self.id_addon = self.settings.getAddonInfo('id')  # gets name
        self.icon = self.settings.getAddonInfo('icon')
        self.path = self.settings.getAddonInfo('path')
        self.name_provider = self.settings.getAddonInfo('name')  # gets name
        self.name_provider_clean = re.sub('.COLOR (.*?)]', '', self.name_provider.replace('[/COLOR]', ''))
        self.query = self.settings.getSetting('query')
        self.querymovie = self.settings.getSetting('querymovie')
        self.querytv = self.settings.getSetting('querytv')
        self.url_address = self.settings.getSetting('url_address')
        self.service = self.settings.getSetting('service')
        pages = self.settings.getSetting('pages')
        if pages == '':
            self.pages = 0
        else:
            self.pages = int(pages)
        self.time_noti = int(self.settings.getSetting('time_noti'))
        self.movie_folder = self.settings.getSetting('movie_folder')
        if self.movie_folder == '':  # define movie folder
            self.movie_folder = 'special://temp/movies/'
        self.show_folder = self.settings.getSetting('show_folder')
        if self.show_folder == '':  # define shows folder
            if anime:
                self.show_folder = 'special://temp/animes/'
            else:
                self.show_folder = 'special://temp/shows/'
        # remove .strm
        self.number_files = int('0%s' % self.settings.getSetting('number_files'))
        self.dialog = xbmcgui.Dialog()
        self.max_magnets = 100  # max_magnets
        self.language = 'en'

    def log(self, message=""):
        xbmc.log('[%s] %s' % (self.name_provider_clean, message))

    def notification(self, message="", force=False):
        if self.time_noti > 0 or force:
            xbmcgui.Dialog().notification(self.name_provider,"%s" % message, self.icon, 1000 if force else self.time_noti)


class Filtering:
    def __init__(self):
        self.settings = xbmcaddon.Addon()
        self.id_addon = self.settings.getAddonInfo('id')  # gets name
        self.name_provider = self.settings.getAddonInfo('name')  # gets name
        self.reason = ''
        self.title = ''
        self.quality_allow = ['*']
        self.quality_deny = []
        self.title = ''
        self.max_size = 10.00  # 10 it is not limit
        self.min_size = 0.00
        # size
        if self.settings.getSetting('movie_min_size') == '':
            self.movie_min_size = 0.0
        else:
            self.movie_min_size = float(self.settings.getSetting('movie_min_size'))
        if self.settings.getSetting('movie_max_size') == '':
            self.movie_max_size = 10.0
        else:
            self.movie_max_size = float(self.settings.getSetting('movie_max_size'))
        if self.settings.getSetting('TV_min_size') == '':
            self.TV_min_size = 0.0
        else:
            self.TV_min_size = float(self.settings.getSetting('TV_min_size'))
        if self.settings.getSetting('TV_max_size') == '':
            self.TV_max_size = 10.0
        else:
            self.TV_max_size = float(self.settings.getSetting('TV_max_size'))

        # movie
        movie_qua1 = self.settings.getSetting('movie_qua1')  # 480p
        movie_qua2 = self.settings.getSetting('movie_qua2')  # HDTV
        movie_qua3 = self.settings.getSetting('movie_qua3')  # 720p
        movie_qua4 = self.settings.getSetting('movie_qua4')  # 1080p
        movie_qua5 = self.settings.getSetting('movie_qua5')  # 3D
        movie_qua6 = self.settings.getSetting('movie_qua6')  # CAM
        movie_qua7 = self.settings.getSetting('movie_qua7')  # TeleSync
        movie_qua8 = self.settings.getSetting('movie_qua8')  # Trailer
        # Accept File
        movie_key_allowed = self.settings.getSetting('movie_key_allowed').replace(', ', ',').replace(' ,', ',')
        movie_allow = re.split(',', movie_key_allowed)
        if movie_qua1 == 'Accept File': movie_allow.append('480p')
        if movie_qua2 == 'Accept File': movie_allow.append('HDTV')
        if movie_qua3 == 'Accept File': movie_allow.append('720p')
        if movie_qua4 == 'Accept File': movie_allow.append('1080p')
        if movie_qua5 == 'Accept File': movie_allow.append('3D')
        if movie_qua6 == 'Accept File': movie_allow.append('CAM')
        if movie_qua7 == 'Accept File': movie_allow.extend(['TeleSync', ' TS '])
        if movie_qua8 == 'Accept File': movie_allow.append('Trailer')
        # Block File
        movie_key_denied = self.settings.getSetting('movie_key_denied').replace(', ', ',').replace(' ,', ',')
        movie_deny = re.split(',', movie_key_denied)
        if movie_qua1 == 'Block File': movie_deny.append('480p')
        if movie_qua2 == 'Block File': movie_deny.append('HDTV')
        if movie_qua3 == 'Block File': movie_deny.append('720p')
        if movie_qua4 == 'Block File': movie_deny.append('1080p')
        if movie_qua5 == 'Block File': movie_deny.append('3D')
        if movie_qua6 == 'Block File': movie_deny.append('CAM')
        if movie_qua7 == 'Block File': movie_deny.extend(['TeleSync', '?TS?'])
        if movie_qua8 == 'Block File': movie_deny.append('Trailer')
        if '' in movie_allow: movie_allow.remove('')
        if '' in movie_deny: movie_deny.remove('')
        if len(movie_allow) == 0: movie_allow = ['*']
        self.movie_allow = movie_allow
        self.movie_deny = movie_deny
        # TV
        TV_qua1 = self.settings.getSetting('TV_qua1')  # 480p
        TV_qua2 = self.settings.getSetting('TV_qua2')  # HDTV
        TV_qua3 = self.settings.getSetting('TV_qua3')  # 720p
        TV_qua4 = self.settings.getSetting('TV_qua4')  # 1080p
        # Accept File
        TV_key_allowed = self.settings.getSetting('TV_key_allowed').replace(', ', ',').replace(' ,', ',')
        TV_allow = re.split(',', TV_key_allowed)
        if TV_qua1 == 'Accept File': TV_allow.append('480p')
        if TV_qua2 == 'Accept File': TV_allow.append('HDTV')
        if TV_qua3 == 'Accept File': TV_allow.append('720p')
        if TV_qua4 == 'Accept File': TV_allow.append('1080p')
        # Block File
        TV_key_denied = self.settings.getSetting('TV_key_denied').replace(', ', ',').replace(' ,', ',')
        TV_deny = re.split(',', TV_key_denied)
        if TV_qua1 == 'Block File': TV_deny.append('480p')
        if TV_qua2 == 'Block File': TV_deny.append('HDTV')
        if TV_qua3 == 'Block File': TV_deny.append('720p')
        if TV_qua4 == 'Block File': TV_deny.append('1080p')
        if '' in TV_allow: TV_allow.remove('')
        if '' in TV_deny: TV_deny.remove('')
        if len(TV_allow) == 0: TV_allow = ['*']
        self.TV_allow = TV_allow
        self.TV_deny = TV_deny

    def use_movie(self):
        self.quality_allow = self.movie_allow
        self.quality_deny = self.movie_deny
        self.min_size = self.movie_min_size
        self.max_size = self.movie_max_size

    def use_TV(self):
        self.quality_allow = self.TV_allow
        self.quality_deny = self.TV_deny
        self.min_size = self.TV_min_size
        self.max_size = self.TV_max_size

    def information(self):
        xbmc.log('[%s] Accepted Keywords: %s' % (self.id_addon, str(self.quality_allow)))
        xbmc.log('[%s] Blocked Keywords: %s' % (self.id_addon, str(self.quality_deny)))
        xbmc.log('[%s] min Size: %s' % (self.id_addon, str(self.min_size) + ' GB'))
        xbmc.log('[%s] max Size: %s' % (self.id_addon, (str(self.max_size) + ' GB') if self.max_size != 10 else 'MAX'))

    # normalize
    def normalize(self, word):
        value = ''
        for a in word:
            if ord(a) < 128:
                value += chr(ord(a))
        value = value.replace('-', ' ').replace('&ntilde;', '')
        return value

    # validate keywords
    def included(self, value, keys, strict=False):
        value = ' ' + self.normalize(value) + ' '
        res = False
        if '*' in keys:
            res = True
        else:
            res1 = []
            for key in keys:
                res2 = []
                for item in re.split('\s', key):
                    item = self.normalize(item)
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
        max_size1 = 100 if self.max_size == 10 else self.max_size
        res = False
        value = float(re.split('\s', size.replace(',', ''))[0])
        value *= 0.001 if 'M' in size else 1
        if self.min_size <= value <= max_size1:
            res = True
        return res

    # verify
    def verify(self, name, size):  # modify to just check quality and size, not name
        self.reason = name.replace(' - ' + self.name_provider, '') + ' ***Blocked File by'
        result = True
        if name != None:
            if not self.included(name, self.quality_allow) or self.included(name, self.quality_deny):
                self.reason += ", Keyword"
                result = False
        if size != None:
            if not self.size_clearance(size):
                result = False
                self.reason += ", Size"
        self.reason = self.reason.replace('by,', 'by') + '***'
        return result

class Storage():
    def __init__(self, fileName="", type="list"):
        self.path = os.path.join(xbmc.translatePath('special://temp') , fileName)
        self.type = type
        if type=="list":
            # get the list
            self.database = []
            try:
                with open(self.path, 'r') as fp:
                    for line in fp:
                        self.database.append(line.strip())
            except:
                pass
        elif type=="dict":
            # get the Dictionary
            self.database = {}
            try:
                with open(self.path, 'r') as fp:
                    for line in fp:
                        listedline = line.strip().split('::')  # split around the :: sign
                        if len(listedline) > 1:  # we have the : sign in there
                            self.database[listedline[0]] = listedline[1]
            except:
                pass

    def add(self, key="", info=""):
        if self.type == "list" and key not in self.database:
            self.database.append(key)
        elif self.type == "dict":
            self.database[key] = info

    def remove(self, key=""):
        if self.type == "list":
            self.database.remove(key)
        elif self.type == "dict":
            del self.database[id]

    def save(self):
        if self.type=="list":
            # save the list
            with open(self.path, 'w') as fp:
                for p in self.database:
                    fp.write("%s\n" % p)
        elif self.type=="dict":
            # save the dictionary
            with open(self.path, 'w') as fp:
                for p in self.database.items():
                    fp.write("%s::%s\n" % p)



# clean_html
def clean_html(data):
    lines = re.findall('<!--(.*?)-->', data)
    for line in lines:
        data = data.replace(line, '')
    return data


# find the name in different language
def translator(imdb_id, language):
    import unicodedata
    import json
    import lib.mechanize as mechanize
    browser1 = mechanize.Browser()
    keywords = {'en': '', 'de': '', 'es': 'espa', 'fr': 'french', 'it': 'italian', 'pt': 'portug'}
    url_themoviedb = "http://api.themoviedb.org/3/find/%s?api_key=8d0e4dca86c779f4157fc2c469c372ca&language=%s" \
                     "&external_source=imdb_id" % (
                         imdb_id, language)
    response = browser1.open(url_themoviedb)
    if response.code==200:
        movie = json.loads(response.read())
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


def exception(title):
    title = title.lower()
    if title == 'csi crime scene investigation':
        title = 'CSI'
    return title


def size_int(size_txt):
    size_txt = size_txt.upper()
    size1 = size_txt.replace('B', '').replace('K', '').replace('M', '').replace('G', '').replace('I', '')
    size = float(size1)
    if 'K' in size_txt:
        size *= 1000
    if 'M' in size_txt:
        size *= 1000000
    if 'G' in size_txt:
        size *= 1e9
    return int(size)


class Magnet():
    def __init__(self, magnet):
        self.magnet = magnet + '&'
        # hash
        hash = re.search('urn:btih:(.*?)&', self.magnet)
        result = ''
        if hash is not None:
            result = hash.group(1)
        self.hash = result
        # name
        name = re.search('dn=(.*?)&', self.magnet)
        result = ''
        if name is not None:
            result = name.group(1).replace('+', ' ')
        self.name = safe_name(result)
        # trackers
        self.trackers = re.findall('tr=(.*?)&', self.magnet)


def val(value):
    if value == '':
        return 1000
    else:
        return int(value)


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


def unquote_name(name):  # convert all %symbols to char
    from urllib import unquote
    return unquote(name).decode("utf-8")


def safe_name(value):  # make the name directory and filename safe
    value = normalize(value)  # First normalization
    value = unquote_name(value)
    value = uncode_name(value)
    value = normalize(value)  # Last normalization, because some unicode char could appear from the previous steps
    value = value.lower().title()
    keys = {'"': ' ', '*': ' ', '/': ' ', ':': ' ', '<': ' ', '>': ' ', '?': ' ', '|': ' ',
            "'": '', 'Of': 'of', 'De': 'de', '.': ' ', ')': ' ', '(': ' ', '[': ' ', ']': ' ', '-': ' '}
    for key in keys.keys():
        value = value.replace(key, keys[key])
    value = ' '.join(value.split())
    return value.replace('S H I E L D', 'SHIELD')


def format_title(value=''):
    import re
    value = safe_name(value).lower()
    formats = ['ep[0-9]+', 's[0-9]+e[0-9]+', 's[0-9]+ e[0-9]+', '[0-9]+x[0-9]+',
               '[0-9][0-9][0-9][0-9] [0-9][0-9] [0-9][0-9]',
               '[0-9][0-9] [0-9][0-9] [0-9][0-9]', 'season [0-9]+', 'season[0-9]+', 's[0-9][0-9]', 'temporada [0-9]+',
               'temporada[0-9]+',
               'seizoen [0-9]+ afl [0-9]+']
    for format in formats:
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
                     'brrip', 'blu', 'webrip', 'hdrip', 'bdrip', 'ita', 'eng', 'esp']
        while pos != -1:  # loop until doesn't have any keyword in the title
            value = title + ' '
            for keyword in keywords:  # checking keywords
                pos = value.find(' ' + keyword + ' ')
                if pos > 0:
                    title = value[:pos].strip()
                    rest = value[pos:].strip() + ' ' + rest
                    break
        # title = title.strip()
        clean_title = title
        if '0000' not in year:
            title += ' (' + year.strip() + ')'
        title = title.title().replace('Of', 'of').replace('De', 'de')
        clean_title = clean_title.title().replace('Of', 'of').replace('De', 'de')
        folder = title
        return {'title': title, 'folder': folder, 'rest': rest.strip(), 'type': 'MOVIE', 'clean_title': clean_title,
                'year': year}
    else:
        # it is a show
        episode = sshow.group(0)
        title = value[:value.find(episode)].strip()
        rest = value[value.find(episode) + len(episode):].strip()
        title = title.strip()
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
        clean_title = folder
        title = folder + ' ' + episode.upper()
        year = 0000
        return {'title': title, 'folder': folder, 'rest': rest, 'type': 'SHOW', 'clean_title': clean_title,
                'year': year}


# find the name in different language
def integration(filename=[], magnet=[], title=[], type_list='', folder='', silence=False, message='', name_provider=''):
    from urllib import quote_plus
    from xbmc import translatePath
    folder = folder.replace('special://temp/', translatePath('special://temp'))
    folder = folder.replace('smb:', '')  # network compatibility
    if len(title) == 0:
        known_title = False
    else:
        known_title = True
    filters = Filtering()  # start filtering
    if type_list == 'MOVIE':
        filters.use_movie()
    else:
        filters.use_TV()  # TV SHOWS and Anime
    name_provider_clean = re.sub('.COLOR (.*?)]', '', name_provider.replace('[/COLOR]', ''))
    dialog = xbmcgui.Dialog()
    overwrite = xbmcaddon.Addon().getSetting('overwrite')
    duplicated = xbmcaddon.Addon().getSetting('duplicated')
    plugin = xbmcaddon.Addon().getSetting('plugin')
    time_noti = int(xbmcaddon.Addon().getSetting('time_noti'))
    total = len(filename)
    if total > 0:
        if not silence:
            answer = dialog.yesno('%s: %s items\nDo you want to integrate this list?' % (name_provider, total),
                                  '%s' % filename)
        else:
            answer = True
        if answer:
            pDialog = xbmcgui.DialogProgress()
            if not silence:
                pDialog.create(name_provider, 'Checking for %s\n%s' % (type_list, message))
            else:
                if time_noti > 0: dialog.notification(name_provider, 'Checking for %s\n%s' % (type_list, message),
                                                      xbmcgui.NOTIFICATION_INFO, time_noti)
            cont = 0
            for cm, name in enumerate(filename):
                info = format_title(name)
                check = False
                details_title = ''
                if len(info['rest']) > 0:  # check for quality filtering
                    filters.title = info['title'] + ' ' + info['rest']
                    if filters.verify(filters.title, None):  # just check the quality no more
                        check = True
                        if duplicated == 'true':
                            details_title = ' ' + info['rest']
                else:
                    check = True
                if check:  # the file has passed the filtering
                    name = info['title'] + details_title
                    if known_title:  # use the user's title, instead of the title found from filename
                        info['folder'] = safe_name(title[cm])
                    if len(info['folder']) > 100:  # to limit the length of directory name
                        info['folder'] = info['folder'][:100]
                    directory = folder + info['folder'] + folder[-1]
                    if not os.path.exists(directory):
                        try:
                            os.makedirs(directory)
                        except:
                            pass
                    uri_string = quote_plus(uncode_name(magnet[cm]))
                    if plugin == 'Pulsar':
                        link = 'plugin://plugin.video.pulsar/play?uri=%s' % uri_string
                    elif plugin == 'KmediaTorrent':
                        link = 'plugin://plugin.video.kmediatorrent/play/%s' % uri_string
                    elif plugin == "Torrenter":
                        link = 'plugin://plugin.video.torrenter/?action=playSTRM&url=' + uri_string + \
                               '&not_download_only=True'
                    else:
                        link = 'plugin://plugin.video.xbmctorrent/play/%s' % uri_string
                    if not os.path.isfile("%s%s.strm" % (directory, name)) or overwrite == 'true':
                        cont += 1
                        if len(name) > 100:
                            name = name[:99]
                        with open("%s%s.strm" % (directory, name), "w") as text_file:  # create .strm
                            text_file.write(link)
                        if not silence: pDialog.update(int(float(cm) / total * 100),
                                                       'Creating %s%s.strm...' % (directory, name))
                        if not silence:
                            if pDialog.iscanceled():
                                break
                        if cont % 100 == 0 and time_noti > 0:
                            dialog.notification(name_provider, '%s %s found - Still working...\n%s'
                                                % (cont, type_list, message), xbmcgui.NOTIFICATION_INFO, time_noti)
                        xbmc.log('[%s]%s%s.strm added' % (name_provider_clean, directory, name))
                    if not silence:
                        if pDialog.iscanceled():
                            break
            if not silence:
                pDialog.close()
            if cont > 0:
                if not xbmc.getCondVisibility('Library.IsScanningVideo'):
                    xbmc.executebuiltin('XBMC.UpdateLibrary(video)')  # update the library with the new information
                xbmc.log('[%s]%s %s added./n%s' % (name_provider_clean, cont, type_list, message))
                if not silence:
                    dialog.ok(name_provider, '%s %s added.\n%s' % (cont, type_list, message))
                else:
                    if time_noti > 0: dialog.notification(name_provider,
                                                          '%s %s added.\n%s' % (cont, type_list, message),
                                                          xbmcgui.NOTIFICATION_INFO, time_noti)
            else:
                xbmc.log('[%s] No new %s\n%s' % (name_provider_clean, type_list, message))
                if not silence:
                    dialog.ok(name_provider, 'No new %s\n%s' % (type_list, message))
                else:
                    if time_noti > 0: dialog.notification(name_provider, 'No new %s\n%s' % (type_list, message),
                                                          xbmcgui.NOTIFICATION_INFO, time_noti)
            del pDialog
    else:
        xbmc.log('[%s] Empty List' % name_provider_clean)
        if not silence: dialog.ok(name_provider, 'Empty List, Try another one, please')
    del dialog
    del filters


def printer(message=""):
    print '****************************'
    print message
    print '*-**************************'


def int_pelisalacarta(channel="", url=[], titles=[], type_list='', folder='', silence=False, message='',
                      name_provider=''):
    from xbmc import translatePath
    from urllib import quote_plus
    from os import path
    folder = folder.replace('special://temp/', translatePath('special://temp'))
    folder = folder.replace('smb:', '')  # network compatibility
    name_provider_clean = re.sub('.COLOR (.*?)]', '', name_provider.replace('[/COLOR]', ''))
    dialog = xbmcgui.Dialog()
    overwrite = xbmcaddon.Addon().getSetting('overwrite')
    time_noti = int(xbmcaddon.Addon().getSetting('time_noti'))
    total = len(url)
    if total > 0:
        if not silence:
            answer = dialog.yesno('%s: %s items\nQuiere agregar estos archivos .strm?' % (name_provider, total),
                                  '%s' % titles, yeslabel="Ahora", nolabel="Luego")
        else:
            answer = True
        if answer:
            pDialog = xbmcgui.DialogProgress()
            if not silence:
                pDialog.create(name_provider, 'Verificando %s\n%s' % (type_list, message))
            else:
                if time_noti > 0: dialog.notification(name_provider, 'Verificando %s\n%s' % (type_list, message),
                                                      xbmcgui.NOTIFICATION_INFO, time_noti)
            cont = 0
            cm = 0
            for item, title in zip(url, titles):  # start writing the list
                info = format_title(title)
                name = info['title']
                directory = path.join(folder, info['folder'])
                if not os.path.exists(directory):
                    try:
                        os.makedirs(directory)
                    except:
                        pass
                link = "plugin://plugin.video.pelisalacarta/?channel=%s&action=play_from_library&url=%s" % (
                    channel, quote_plus(item))
                cm += 1
                fullFileName = path.join(directory, "%s.strm" % name)
                if not os.path.isfile(fullFileName) or overwrite == 'true':
                    cont += 1
                    if len(name) > 100: name = name[:99]
                    with open(fullFileName, "w") as text_file:  # create .strm
                        text_file.write(link)
                    if not silence: pDialog.update(int(float(cm) / total * 100), 'Creando %s...' % fullFileName)
                    if not silence and pDialog.iscanceled(): break
                    if cont % 100 == 0 and time_noti > 0:
                        dialog.notification(name_provider, '%s %s encontrados - Trabajando...\n%s'
                                            % (cont, type_list, message), xbmcgui.NOTIFICATION_INFO, time_noti)
                    xbmc.log('[%s]%s Agragregadosegados' % (name_provider_clean, fullFileName))
                if not silence and pDialog.iscanceled(): break
            if not silence:
                pDialog.close()
            if cont > 0:
                if not xbmc.getCondVisibility('Library.IsScanningVideo'):
                    xbmc.executebuiltin('XBMC.UpdateLibrary(video)')  # update the library with the new information
                xbmc.log('[%s]%s %s agregados./n%s' % (name_provider_clean, cont, type_list, message))
                if not silence:
                    dialog.ok(name_provider, '%s %s agregados.\n%s' % (cont, type_list, message))
                else:
                    if time_noti > 0: dialog.notification(name_provider,
                                                          '%s %s agregados.\n%s' % (cont, type_list, message),
                                                          xbmcgui.NOTIFICATION_INFO, time_noti)
            else:
                xbmc.log('[%s] Nada nuevo %s\n%s' % (name_provider_clean, type_list, message))
                if not silence:
                    dialog.ok(name_provider, 'Nada nuevo %s\n%s' % (type_list, message))
                else:
                    if time_noti > 0: dialog.notification(name_provider, 'Nada nuevo %s\n%s' % (type_list, message),
                                                          xbmcgui.NOTIFICATION_INFO, time_noti)
            del pDialog


def removeDirectory(folder="", title=""):
    from xbmc import translatePath
    folder = folder.replace('special://temp/', translatePath('special://temp'))
    folder = folder.replace('smb:', '')  # network compatibility
    info = format_title(title)
    directory = os.path.join(folder, info['folder'])
    if os.path.exists(directory):
        import shutil
        shutil.rmtree(directory, ignore_errors=True)
    if not xbmc.getCondVisibility('Library.IsScanningVideo'):
        xbmc.executebuiltin('XBMC.CleanLibrary(video)')  # clean the library

