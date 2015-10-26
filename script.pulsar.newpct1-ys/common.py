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
        self.language = self.settings.getSetting('language')
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
            self.status = 200
        except urllib2.URLError as e:
            self.status = e.reason
            result = False
        except urllib2.HTTPError as e:
            self.status = e.code
            result = False
        return result

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
        self.reason = ''
        self.title = ''
        self.quality_allow = ['*']
        self.quality_deny = []
        self.title = ''
        self.max_size = 10.00  # 10 it is not limit
        self.min_size = 0.00
        #size
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
        # Accept File
        movie_key_allowed = self.settings.getSetting('movie_key_allowed').replace(', ',',').replace(' ,',',')
        movie_allow = re.split(',',movie_key_allowed)
        if movie_qua1 == 'Accept File': movie_allow.append('480p')
        if movie_qua2 == 'Accept File': movie_allow.append('HDTV')
        if movie_qua3 == 'Accept File': movie_allow.append('720p')
        if movie_qua4 == 'Accept File': movie_allow.append('1080p')
        if movie_qua5 == 'Accept File': movie_allow.append('3D')
        if movie_qua6 == 'Accept File': movie_allow.append('CAM')
        if movie_qua7 == 'Accept File': movie_allow.extend(['TeleSync', ' TS '])
        #Block File
        movie_key_denied = self.settings.getSetting('movie_key_denied').replace(', ',',').replace(' ,',',')
        movie_deny = re.split(',',movie_key_denied)
        if movie_qua1 == 'Block File': movie_deny.append('480p')
        if movie_qua2 == 'Block File': movie_deny.append('HDTV')
        if movie_qua3 == 'Block File': movie_deny.append('720p')
        if movie_qua4 == 'Block File': movie_deny.append('1080p')
        if movie_qua5 == 'Block File': movie_deny.append('3D')
        if movie_qua6 == 'Block File': movie_deny.append('CAM')
        if movie_qua7 == 'Block File': movie_deny.extend(['TeleSync', '?TS?'])
        if '' in movie_allow: movie_allow.remove('')
        if '' in movie_deny: movie_deny.remove('')
        if len(movie_allow)==0: movie_allow = ['*']
        self.movie_allow = movie_allow
        self.movie_deny = movie_deny
        # TV
        TV_qua1 = self.settings.getSetting('TV_qua1')  # 480p
        TV_qua2 = self.settings.getSetting('TV_qua2')  # HDTV
        TV_qua3 = self.settings.getSetting('TV_qua3')  # 720p
        TV_qua4 = self.settings.getSetting('TV_qua4')  # 1080p
        # Accept File
        TV_key_allowed = self.settings.getSetting('TV_key_allowed').replace(', ',',').replace(' ,',',')
        TV_allow = re.split(',',TV_key_allowed)
        if TV_qua1 == 'Accept File': TV_allow.append('480p')
        if TV_qua2 == 'Accept File': TV_allow.append('HDTV')
        if TV_qua3 == 'Accept File': TV_allow.append('720p')
        if TV_qua4 == 'Accept File': TV_allow.append('1080p')
        # Block File
        TV_key_denied = self.settings.getSetting('TV_key_denied').replace(', ',',').replace(' ,',',')
        TV_deny = re.split(',',TV_key_denied)
        if TV_qua1 == 'Block File': TV_deny.append('480p')
        if TV_qua2 == 'Block File': TV_deny.append('HDTV')
        if TV_qua3 == 'Block File': TV_deny.append('720p')
        if TV_qua4 == 'Block File': TV_deny.append('1080p')
        if '' in TV_allow: TV_allow.remove('')
        if '' in TV_deny: TV_deny.remove('')
        if len(TV_allow)==0: TV_allow = ['*']
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
        xbmc.log('[%s] max Size: %s' % (self.id_addon, (str(self.max_size)  + ' GB') if self.max_size != 10 else 'MAX'))

    #normalize
    def normalize(self, word):
        value = ''
        for a in word:
            if ord(a) < 128:
                value += chr(ord(a))
        value = value.replace('-', ' ').replace('&ntilde;', '')
        return value

    # validate keywords
    def included(self, value, keys):
        value = self.normalize(value)
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
    def verify(self, name, size):
        self.reason = name.replace(' - ' + self.name_provider, ' ***Blocked File by')
        if self.included(name, [self.title.replace('.', ' ')]):
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
    lines = re.findall('<!--(.*?)-->',data)
    for line in lines:
        data = data.replace(line, '')
    return data


# find the name in different language
def translator(imdb_id, language):
    import unicodedata
    import json
    browser1 = Browser()
    url_themoviedb = "http://api.themoviedb.org/3/find/%s?api_key=8d0e4dca86c779f4157fc2c469c372ca&language=%s&external_source=imdb_id" % (imdb_id, language)
    if browser1.open(url_themoviedb):
        movie = json.loads(browser1.content)
        title0 = movie['movie_results'][0]['title'].replace(u'\xf1', '*')
        title_normalize = unicodedata.normalize('NFKD', title0)
        title = title_normalize.encode('ascii', 'ignore').replace(':', '')
        title = title.decode('utf-8').replace('*', u'\xf1').encode('utf-8')
    else:
        title = 'Pas de communication avec le themoviedb.org'
    return title

def clean(title):
    title = title.replace('s h i e l d', 's.h.i.e.l.d')
    title = title.replace(' s ', 's ')
    return title