# library to access URL, translation title and filtering
__author__ = 'mancuniancol'
import re

import xbmcaddon
import xbmc


class Settings:
    def __init__(self):
        self.settings = xbmcaddon.Addon()
        self.id_addon = self.settings.getAddonInfo('id')  # gets name
        self.url = self.settings.getSetting('url_address')
        self.icon = self.settings.getAddonInfo('icon')
        self.name_provider = self.settings.getAddonInfo('name')  # gets name
        self.name_provider = re.sub('.COLOR (.*?)]', '', self.name_provider.replace('[/COLOR]', ''))
        self.language = self.settings.getSetting('language')
        if self.language == '': self.language = 'en'
        self.extra = self.settings.getSetting('extra')
        self.time_noti = int(self.settings.getSetting('time_noti'))
        max_magnets = self.settings.getSetting('max_magnets')
        self.max_magnets = int(max_magnets) if max_magnets is not '' else 10  # max_magnets


class Browser:
    def __init__(self):
        import cookielib

        self._cookies = None
        self.cookies = cookielib.LWPCookieJar()
        self.content = None
        self.status = None

    def create_cookies(self, payload):
        import urllib

        self._cookies = urllib.urlencode(payload)

    def open(self, url='', language='en'):
        import urllib2

        result = True
        if self._cookies is not None:
            req = urllib2.Request(url, self._cookies)
            self._cookies = None
        else:
            req = urllib2.Request(url)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/39.0.2171.71 Safari/537.36')
        req.add_header('Content-Language', language)
        req.add_header("Accept-Encoding", "gzip")
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))  # open cookie jar
        try:
            response = opener.open(req)  # send cookies and open url
            # borrow from provider.py Steeve
            if response.headers.get("Content-Encoding", "") == "gzip":
                import zlib

                self.content = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(response.read())
            else:
                self.content = response.read()
            response.close()
            self.status = 200
        except urllib2.URLError as e:
            self.status = e.reason
            result = False
        except urllib2.HTTPError as e:
            self.status = e.code
            result = False
        return result

    def open2(self, url=''):
        import httplib

        word = url.split("://")
        search = word[1]
        pos = search.find("/")
        conn = httplib.HTTPConnection(search[:pos])
        conn.request("GET", search[pos:])
        r1 = conn.getresponse()
        self.status = str(r1.status) + " " + r1.reason
        self.content = r1.read()
        if r1.status == 200:
            return True
        else:
            return False

    def login(self, url, payload, word):
        result = False
        self.create_cookies(payload)
        if self.open(url):
            result = True
            data = self.content
            if word in data:
                self.status = 'Wrong Username or Password'
                result = False
        return result


class Filtering:
    def __init__(self):
        self.settings = xbmcaddon.Addon()
        self.id_addon = self.settings.getAddonInfo('id')  # gets name
        self.name_provider = self.settings.getAddonInfo('name')  # gets name
        self.time_noti = int(self.settings.getSetting('time_noti'))  # time notification
        self.icon = self.settings.getAddonInfo('icon')
        self.name_provider = self.settings.getAddonInfo('name')  # gets name
        self.name_provider = re.sub('.COLOR (.*?)]', '', self.name_provider.replace('[/COLOR]', ''))
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

    def type_filtering(self, query, separator='%20'):
        from xbmcgui import Dialog
        from urllib import quote

        if '#MOVIE&FILTER' in query:
            self.use_movie()
            query = query.replace('#MOVIE&FILTER', '')
        elif '#TV&FILTER' in query:
            self.use_TV()
            query = query.replace('#TV&FILTER', '')
            query = exception(query)  # CSI series problem
        self.title = query  # to do filtering by name
        if self.time_noti > 0:
            dialog = Dialog()
            dialog.notification(self.name_provider, query.title(), self.icon, self.time_noti)
            del Dialog
        query = quote(query.rstrip()).replace('%20', separator)
        return query

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

    # validate keywords
    def included(self, value, keys, strict=False):
        value = ' ' + value + ' '
        res = False
        if '*' in keys:
            res = True
        else:
            res1 = []
            for key in keys:
                res2 = []
                for item in re.split('\s', key):
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
        value = float(re.split('\s', size.strip().replace(',', ''))[0])
        value *= 0.001 if 'M' in size else 1
        if self.min_size <= value <= max_size1:
            res = True
        return res

    def normalize(self, name):
        from unicodedata import normalize
        import types

        if type(name) == types.StringType:
            unicode_name = name.decode('unicode-escape')
        else:
            unicode_name = name
        normalize_name = normalize('NFKD', unicode_name)
        return normalize_name.encode('ascii', 'ignore')

    def uncode_name(self, name):  # convert all the &# codes to char, remove extra-space and normalize
        from HTMLParser import HTMLParser

        name = name.replace('<![CDATA[', '').replace(']]', '')
        name = HTMLParser().unescape(name.lower())
        return name

    def unquote_name(self, name):  # convert all %symbols to char
        from urllib import unquote

        return unquote(name).decode("utf-8")

    def safe_name(self, value):  # make the name directory and filename safe
        value = self.normalize(value)  # First normalization
        value = self.unquote_name(value)
        value = self.uncode_name(value)
        value = self.normalize(
            value)  # Last normalization, because some unicode char could appear from the previous steps
        value = value.lower().title()
        keys = {'"': ' ', '*': ' ', '/': ' ', ':': ' ', '<': ' ', '>': ' ', '?': ' ', '|': ' ',
                "'": '', 'Of': 'of', 'De': 'de', '.': ' ', ')': ' ', '(': ' ', '[': ' ', ']': ' ', '-': ' '}
        for key in keys.keys():
            value = value.replace(key, keys[key])
        value = ' '.join(value.split())
        return value.replace('S H I E L D', 'SHIELD')

    # verify
    def verify(self, name, size):
        name = self.safe_name(name)
        self.title = self.safe_name(self.title)
        self.reason = name.replace(' - ' + self.name_provider, '') + ' ***Blocked File by'
        if self.included(name, [self.title], True):
            result = True
            if name != None:
                if not self.included(name, self.quality_allow) or self.included(name, self.quality_deny):
                    self.reason += ", Keyword"
                    result = False
            if size != None:
                if not self.size_clearance(size):
                    result = False
                    self.reason += ", Size"
        else:
            result = False
            self.reason += ", Name"
        self.reason = self.reason.replace('by,', 'by') + '***'
        return result


# clean_html
def clean_html(data):
    lines = re.findall('<!--(.*?)-->', data)
    for line in lines:
        data = data.replace(line, '')
    return data


# find the name in different language
def translator(imdb_id, language, extra=True):
    import json

    browser1 = Browser()
    keywords = {'en': '', 'de': '', 'es': 'espa', 'fr': 'french', 'it': 'italian', 'pt': 'portug'}
    url_themoviedb = "http://api.themoviedb.org/3/find/%s?api_key=8d0e4dca86c779f4157fc2c469c372ca&language=%s" \
                     "&external_source=imdb_id" % (imdb_id, language)
    if browser1.open(url_themoviedb):
        movie = json.loads(browser1.content)
        title = movie['movie_results'][0]['title'].encode('utf-8')
        original_title = movie['movie_results'][0]['original_title'].encode('utf-8')
        if title == original_title and extra:
            title += ' ' + keywords[language]
    else:
        title = 'Pas de communication avec le themoviedb.org'
    return title.rstrip()


def size_int(size_txt):
    size_txt = size_txt.upper()
    size1 = size_txt.replace('B', '').replace('I', '').replace('K', '').replace('M', '').replace('G', '')
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
        self.name = result.title()
        # trackers
        self.trackers = re.findall('tr=(.*?)&', self.magnet)


def IMDB_title(IMDB_id):
    browser = Browser()
    result = ''
    if browser.open('http://www.omdbapi.com/?i=%s&r=json' % IMDB_id):
        data = browser.content.replace('"', '').replace('{', '').replace('}', '').split(',')
        result = data[0].split(":")[1] + ' ' + data[1].split(":")[1]
    return result


def exception(title):
    title = title.lower()
    title = title.replace('csi crime scene investigation', 'CSI')
    title = title.replace('law and order special victims unit', 'law and order svu')
    title = title.replace('law order special victims unit', 'law and order svu')
    return title


def getlinks(page):
    browser = Browser()
    result = ""
    if browser.open(page):
        content = re.findall('magnet:\?[^\'"\s<>\[\]]+', browser.content)
        if content != None:
            result = content[0]
        else:
            content = re.findall('http(.*?).torrent', browser.content)
            if content != None:
                result = 'http' + content[0] + '.torrent'
    return result


# function to parse table html, returning array 2D
def table(data="", order=1):
    table_val = []
    if data != "":
        # there is information
        import re

        finder = re.findall("<table(.*?)>(.*?)</table>", data, re.S)
        if len(finder) >= order:
            table = finder[order - 1][1]
            finder = re.findall("<tr(.*?)>(.*?)</tr>", table, re.S)
            for (attribut, row) in finder:
                row_val = []
                if "<th" in row:
                    finder = re.findall("<th(.*?)>(.*?)</th>", row, re.S)
                else:
                    finder = re.findall("<td(.*?)>(.*?)</td>", row, re.S)
                for x in range(len(finder)):
                    row_val.append(finder[x - 1][1])
                table_val.append(row_val)
    return table_val


# (attributs, text, tag
def parse_tag(data=""):
    finder = []
    if data != "":
        # there is information
        import re

        finder = re.findall("<(.*?)>(.*?)</(.*?)>", data, re.S)
    return finder
