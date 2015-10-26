# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2014 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,re,os,datetime,base64,xbmcaddon

try:
    import CommonFunctions as common
except:
    import commonfunctionsdummy as common
try:
    import json
except:
    import simplejson as json


class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='5'):
        if not proxy == None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post == None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0')
        if not referer == None:
            request.add_header('Referer', referer)
        if not cookie == None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class cleantitle:
    def movie(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def tv(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title


class icefilms:
    def __init__(self):
        self.base_link = 'https://ipv6.icefilms.info'
        self.moviesearch_link = '/movies/a-z/%s'
        self.tvsearch_link = '/tv/a-z/%s'
        self.video_link = '/membersonly/components/com_iceplayer/video.php?vid=%s'
        self.resp_link = '/membersonly/components/com_iceplayer/video.phpAjaxResp.php'

    def get_movie(self, imdb, title, year):
        try:
            query = title.upper()
            if query.startswith('THE '): query = query.replace('THE ', '')
            elif query.startswith('A '): query = query.replace('A ', '')
            if not query[0].isalpha(): query = '1'
            query = self.base_link + self.moviesearch_link % query[0]

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = re.compile('id=%s>.+?href=(.+?)>' % imdb).findall(result)[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            return

    def get_show(self, imdb, show, show_alt, year):
        try:
            query = show.upper()
            if query.startswith('THE '): query = query.replace('THE ', '')
            elif query.startswith('A '): query = query.replace('A ', '')
            if not query[0].isalpha(): query = '1'
            query = self.base_link + self.tvsearch_link % query[0]

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = re.compile('id=%s>.+?href=(.+?)>' % imdb).findall(result)[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        try:
            url = self.base_link + url
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = re.compile('href=(/ip.php[?]v=.+?)&>%01dx%02d' % (int(season), int(episode))).findall(result)[0]
            url = url.split('href=')[-1]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            id = url.split('v=', 1)[-1].rsplit('&', 1)[0]
            url = self.base_link + self.video_link % id
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            sec = re.compile('lastChild[.]value="(.+?)"').findall(result)[0]
            links = common.parseDOM(result, "div", attrs = { "class": "ripdiv" })

            import random

            try:
                hd_links = ''
                hd_links = [i for i in links if '>HD 720p<' in i][0]
                hd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(hd_links)
            except:
                pass

            for url, host in hd_links:
                try:
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosthdDict: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    sources.append({'source': host, 'quality': 'HD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass

            try:
                sd_links = ''
                sd_links = [i for i in links if '>DVDRip / Standard Def<' in i]
                if len(sd_links) == 0: sd_links = [i for i in links if '>DVD Screener<' in i]
                if len(sd_links) == 0: sd_links = [i for i in links if '>R5/R6 DVDRip<' in i]
                sd_links = sd_links[0]
                sd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(sd_links)
            except:
                pass

            for url, host in sd_links:
                try:
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    sources.append({'source': host, 'quality': 'SD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            post = url
            url = self.base_link + self.resp_link
            result = getUrl(url, post=post).result

            url = result.split("?url=", 1)[-1]
            url = urllib.unquote_plus(url)

            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class primewire:
    def __init__(self):
        self.base_link = 'http://www.primewire.ag'
        self.proxy_link = 'http://proxy.cyberunlocker.com/browse.php?u='
        self.key_link = '/index.php?search'
        self.moviesearch_link = '/index.php?search_keywords=%s&key=%s&search_section=1'
        self.tvsearch_link = '/index.php?search_keywords=%s&key=%s&search_section=2'

    def get_movie(self, imdb, title, year):
        try:
            base_link = self.base_link
            result = getUrl(base_link + self.key_link, mobile=True).result
            if not "Search" in result:
                base_link = self.proxy_link + self.base_link
                result = getUrl(base_link + self.key_link, mobile=True).result

            key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
            query = base_link + self.moviesearch_link % (urllib.quote_plus(re.sub('\'', '', title)), key)

            result = getUrl(query, mobile=True).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "index_item.+?" })

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            match = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a", ret="title")[0])  for i in result]
            match = [i[0] for i in match if any(x in i[1] for x in years)]
            match = [i.replace(base_link, '') for i in match]
            match = uniqueList(match).list

            if match == []: return
            for i in match[:5]:
                try:
                    result = getUrl(base_link + i, mobile=True).result
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                    t = common.parseDOM(result, "meta", ret="content", attrs = { "property": "og:title" })[0]
                    if title == cleantitle().movie(t):
                        match2 = i
                except:
                    pass

            url = match2.replace(base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, show, show_alt, year):
        try:
            base_link = self.base_link
            result = getUrl(base_link + self.key_link, mobile=True).result
            if not "Search" in result:
                base_link = self.proxy_link + self.base_link
                result = getUrl(base_link + self.key_link, mobile=True).result

            key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
            query = base_link + self.tvsearch_link % (urllib.quote_plus(re.sub('\'', '', show)), key)
            result = getUrl(query, mobile=True).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "index_item.+?" })

            shows = [cleantitle().tv(show), cleantitle().tv(show_alt)]
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            match = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a", ret="title")[0])  for i in result]
            match = [i[0] for i in match if any(x in i[1] for x in years)]
            match = [i.replace(base_link, '') for i in match]
            match = uniqueList(match).list

            if match == []: return
            for i in match[:5]:
                try:
                    result = getUrl(base_link + i, mobile=True).result
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                    t = common.parseDOM(result, "meta", ret="content", attrs = { "property": "og:title" })[0]
                    if any(x == cleantitle().tv(t) for x in shows):
                        match2 = i
                except:
                    pass

            url = match2
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        url = url.replace('/watch-','/tv-')
        url += '/season-%01d-episode-%01d' % (int(season), int(episode))
        url = common.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            base_link = self.base_link
            result = getUrl(base_link + url, mobile=True).result
            if not "choose_tabs" in result:
                base_link = self.proxy_link + self.base_link
                result = getUrl(base_link + url, mobile=True).result

            result = result.decode('iso-8859-1').encode('utf-8')
            links = common.parseDOM(result, "tbody")

            for i in links:
                try:
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = re.compile('url=(.+?)&').findall(url)[0]
                    url = base64.urlsafe_b64decode(url.encode('utf-8'))
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = common.parseDOM(i, "a", ret="href")[0]
                    host = re.compile('domain=(.+?)&').findall(host)[0]
                    host = base64.urlsafe_b64decode(host.encode('utf-8'))
                    host = host.rsplit('.', 1)[0]
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    quality = common.parseDOM(i, "span", ret="class")[0]
                    if quality == 'quality_cam' or quality == 'quality_ts': quality = 'CAM'
                    elif quality == 'quality_dvd': quality = 'SD'
                    else:  raise Exception()
                    quality = quality.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'Primewire', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class movie25:
    def __init__(self):
        self.base_link = 'http://www.movie25.cm'
        self.proxy_link = 'http://proxy.cyberunlocker.com/browse.php?u='
        self.search_link = '/search.php?key=%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % urllib.quote_plus(title)

            base_link = self.base_link
            result = getUrl(base_link + query).result
            if not "movie_table" in result:
                base_link = self.proxy_link + self.base_link
                result = getUrl(base_link + query).result

            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "movie_table" })[0]
            result = common.parseDOM(result, "li")

            years = [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)]
            match = [i for i in result if any(x in i for x in years)]
            match = [common.parseDOM(i, "a", ret="href")[0] for i in match]
            match = [i.replace(base_link, '') for i in match]
            match = uniqueList(match).list

            if match == []: return
            for i in match[:10]:
                try:
                    result = getUrl(base_link + i).result
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                except:
                    pass

            url = match2.replace(base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            base_link = self.base_link
            result = getUrl(base_link + url).result
            if not "links_quality" in result:
                base_link = self.proxy_link + self.base_link
                result = getUrl(base_link + url).result

            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "links_quality" })[0]

            quality = common.parseDOM(result, "h1")[0]
            quality = quality.replace('\n','').rsplit(' ', 1)[-1]
            if quality == 'CAM' or quality == 'TS': quality = 'CAM'
            elif quality == 'SCREENER': quality = 'SCR'
            else: quality = 'SD'

            links = common.parseDOM(result, "ul")

            for i in links:
                try:
                    name = common.parseDOM(i, "a")[0]
                    name = common.replaceHTMLCodes(name)
                    if name.isdigit(): raise Exception()

                    host = common.parseDOM(i, "li", attrs = { "class": "link_name" })[0]
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = url.replace(base_link, '')
                    url = '%s%s' % (self.base_link, url)
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'Movie25', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            result = getUrl(url).result
            if not "location.href" in result:
                result = getUrl(self.proxy_link + url).result

            result = result.decode('iso-8859-1').encode('utf-8')
            url = common.parseDOM(result, "input", ret="onclick")
            url = [i for i in url if 'location.href' in i and 'http://' in i][0]
            url = url.split("'", 1)[-1].rsplit("'", 1)[0]

            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class watchseries:
    def __init__(self):
        self.base_link = 'http://watchseries.ag'
        self.proxy_link = 'http://proxy.cyberunlocker.com/browse.php?u='
        self.search_link = '/json/search/%s'
        self.episode_link = '/json/episode/%s_s%s_e%s.html'

    def get_show(self, imdb, show, show_alt, year):
        try:
            query = self.search_link % urllib.quote_plus(show)

            base_link = self.base_link
            result = getUrl(base_link + query, mobile=True).result
            if not "Search" in result:
                base_link = self.proxy_link + self.base_link
                result = getUrl(base_link + query, mobile=True).result

            result = json.loads(result)
            result = json.dumps(result['results'])
            result = re.compile('".+?".+?({".+?".+?})').findall(result)
            result = [json.loads(i) for i in result]

            shows = [cleantitle().tv(show), cleantitle().tv(show_alt)]
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            match = [i['href'] for i in result if any(x == i['year'] for x in years)]
            match = [i.replace(base_link, '') for i in match][::-1]
            match = uniqueList(match).list

            if match == []: return
            for i in match[:5]:
                try:
                    result = getUrl(base_link + i, mobile=True).result
                    result = json.loads(result)
                    result = json.dumps(result['results'])
                    result = result.replace('\\"', '')
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                    t = re.compile('"tvName".+?"(.+?)"').findall(result)[0]
                    if any(x == cleantitle().tv(t) for x in shows):
                        match2 = i
                except:
                    pass

            url = match2.replace(base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        url = url.rsplit('/', 1)[-1]
        url = self.episode_link % (url, season, episode)
        url = common.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            base_link = self.base_link
            result = getUrl(base_link + url, mobile=True).result
            if not "episode" in result:
                base_link = self.proxy_link + self.base_link
                result = getUrl(base_link + url, mobile=True).result

            result = json.loads(result)
            result = result['results']['0']['links']
            links = [i for i in result if i['lang'] == 'English' and i['host'].lower() in hostDict]

            for i in links:
                try:
                    url = i['url']
                    url = url.replace(base_link, '')
                    url = '%s%s' % (self.base_link, url)
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = i['host']
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': 'SD', 'provider': 'Watchseries', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if url.startswith(self.base_link):
                url = getUrl(self.proxy_link + url, output='geturl').result
                url = url.replace(self.proxy_link, '')

            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class iwatchonline:
    def __init__(self):
        self.base_link = 'http://www.iwatchonline.to'
        self.proxy_link = 'http://proxy.cyberunlocker.com/browse.php?u='
        self.search_link = '/advance-search'
        self.show_link = '/tv-shows/%s'
        self.episode_link = '/episode/%s-s%02de%02d'

    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link
            post = urllib.urlencode({'searchquery': title, 'searchin': '1'})

            base_link = self.base_link
            result = getUrl(base_link + query, post=post).result
            if not "widget search-page" in result:
                base_link = self.proxy_link + self.base_link
                result = getUrl(base_link + query, post=post).result

            result = common.parseDOM(result, "div", attrs = { "class": "widget search-page" })[0]
            result = common.parseDOM(result, "td")

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[-1], common.parseDOM(i, "a")[-1])  for i in result]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = result.replace(base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, show, show_alt, year):
        try:
            query = self.search_link
            post = urllib.urlencode({'searchquery': show, 'searchin': '2'})

            base_link = self.base_link
            result = getUrl(base_link + query, post=post).result
            if not "widget search-page" in result:
                base_link = self.proxy_link + self.base_link
                result = getUrl(base_link + query, post=post).result

            result = common.parseDOM(result, "div", attrs = { "class": "widget search-page" })[0]
            result = common.parseDOM(result, "td")

            shows = [cleantitle().tv(show), cleantitle().tv(show_alt)]
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[-1], common.parseDOM(i, "a")[-1])  for i in result]
            result = [i for i in result if any(x == cleantitle().tv(i[1]) for x in shows)]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = result.rsplit('/', 1)[-1]
            url = self.show_link % url
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        url = url.rsplit('/', 1)[-1]
        url = self.episode_link % (url, int(season), int(episode))
        url = common.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            base_link = self.base_link
            result = getUrl(base_link + url).result
            if not '"pt0"' in result:
                base_link = self.proxy_link + self.base_link
                result = getUrl(base_link + url).result

            links = common.parseDOM(result, "tr", attrs = { "id": "pt.+?" })

            for i in links:
                try:
                    host = common.parseDOM(i, "img", attrs = { "src": ".+?" })[0]
                    host = host.split(' ', 1)[0].split('<', 1)[0]
                    host = host.rsplit('.', 1)[0].split('.', 1)[-1]
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    lang = common.parseDOM(i, "img", ret="data-original-title", attrs = { "src": ".+?" })[0]
                    if not lang == 'English': raise Exception()

                    if '>Cam<' in i or '>TS<' in i: quality = 'CAM'
                    else: quality = 'SD'

                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = url.replace(base_link, '')
                    url = '%s%s' % (self.base_link, url)
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'Iwatchonline', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            result = getUrl(url).result
            if not "frame" in result:
                result = getUrl(self.proxy_link + url).result

            url = common.parseDOM(result, "iframe", ret="src", attrs = { "class": "frame" })[0]
            url = url.replace(self.proxy_link, '')

            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class movietube:
    def __init__(self):
        self.base_link = 'http://tunemovie.me'
        self.tvbase_link = 'http://tvstreaming.cc'
        self.index_link = '/index.php'
        self.docs_link = 'https://docs.google.com/file/d/%s/'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.index_link
            post = urllib.urlencode({'a': 'retrieve', 'c': 'result', 'p': '{"KeyWord":"%s","Page":"1","NextToken":""}' % title})

            result = getUrl(query, post=post).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "tr")

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [common.parseDOM(i, "h1")[0] for i in result]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a")[0]) for i in result]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = result.split('v=', 1)[-1]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, show, show_alt, year):
        try:
            url = show
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        try:
            query = self.tvbase_link + self.index_link
            post = urllib.urlencode({'a': 'retrieve', 'c': 'result', 'p': '{"KeyWord":"%s","Page":"1","NextToken":""}' % url})

            result = getUrl(query, post=post).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "tr")

            show = cleantitle().tv(url)
            season = '%01d' % int(season)
            episode = '%02d' % int(episode)
            result = [common.parseDOM(i, "h1")[0] for i in result]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a")[0]) for i in result]
            result = [(i[0], re.sub('\sSeason\s\d*.+', '', i[1]), re.compile('\sSeason\s(\d*)').findall(i[1])[0]) for i in result]
            result = [i for i in result if show == cleantitle().tv(i[1])]
            result = [i[0] for i in result if season == i[2]][0]

            url = result.split('v=', 1)[-1]
            url = '%s|%s' % (url, episode)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            content = re.compile('(.+?)\|\d*$').findall(url)

            if len(content) == 0:
                query = self.base_link + self.index_link
                post = urllib.urlencode({'a': 'getmoviealternative', 'c': 'result', 'p': '{"KeyWord":"%s"}' % url})
                result = getUrl(query, post=post).result
                result = re.compile('(<a.+?</a>)').findall(result)

                links = [i for i in result if '0000000008400000.png' in i]
                links = [i for i in links if '>1080p<' in i or '>720p<' in i]
                links = [common.parseDOM(i, "a", ret="href")[0] for i in links][:3]
                links = [i.split('?v=')[-1] for i in links]

                for u in links:
                    try:
                        query = self.base_link + self.index_link
                        post = urllib.urlencode({'a': 'getplayerinfo', 'c': 'result', 'p': '{"KeyWord":"%s"}' % u})
                        result = getUrl(query, post=post).result

                        url = common.parseDOM(result, "source", ret="src", attrs = { "data-res": "1080" })
                        if len(url) > 0:
                            sources.append({'source': 'Movietube', 'quality': '1080p', 'provider': 'Movietube', 'url': url[0]})

                        url = common.parseDOM(result, "source", ret="src", attrs = { "data-res": "720" })
                        if len(url) > 0:
                            sources.append({'source': 'Movietube', 'quality': 'HD', 'provider': 'Movietube', 'url': url[0]})
                    except:
                        pass

            else:
                query = self.tvbase_link + self.index_link
                url, episode = re.compile('(.+?)\|(\d*)$').findall(url)[0]
                post = urllib.urlencode({'a': 'getpartlistinfo', 'c': 'result', 'p': '{"KeyWord":"%s","Episode":"%s"}' % (url, episode)})
                result = getUrl(query, post=post).result
                result = re.compile('(<a.+?</a>)').findall(result)

                links = [common.parseDOM(i, "a", ret="data") for i in result]
                links = [i[0] for i in links if len(i) > 0]
                links = [i for i in links if i.startswith('--MP4') or i.startswith('--Doc')]

                for u in links:
                    try:
                        if u.startswith('--Doc'):
                            import commonresolvers
                            url = self.docs_link % u.split('--', 2)[-1]
                            url = commonresolvers.googledocs(url)

                            for i in url: sources.append({'source': 'Movietube', 'quality': i['quality'], 'provider': 'Movietube', 'url': i['url']})
                        else:
                            import commonresolvers
                            url = u.split('--', 2)[-1]
                            i = commonresolvers.google(url)[0]

                            sources.append({'source': 'Movietube', 'quality': i['quality'], 'provider': 'Movietube', 'url': i['url']})
                    except:
                        pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class moviezone:
    def __init__(self):
        self.base_link = 'http://www.hdmoviezone.net'
        self.search_link = '/feeds/posts/summary?alt=json&q=%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = json.loads(result)

            imdb = 'tt' + imdb
            result = result['feed']['entry']
            result = [i['link'] for i in result if imdb in i['summary']['$t']][0]
            result = [i['href'] for i in result if i['rel'] == 'alternate'][0]

            url = result.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            result = getUrl(self.base_link + url).result

            url = re.compile('server_php\s+=\s+"(.+?)"').findall(result)
            url = [i for i in url if i.endswith('.php')][::-1][:2]

            post = common.parseDOM(result, "div", ret="file", attrs = { "id": "mediainfo" })[0]
            post = urllib.urlencode({'url': post})

            def get_php(url, post):
                request = urllib2.Request(url, post)
                request.add_header('Origin', self.base_link)
                response = urllib2.urlopen(request, timeout=5)
                result = response.read()
                response.close()
                result = json.loads(result)
                return result

            try: result = get_php(url[0], post)
            except: result = get_php(url[1], post)
            result = result['content']

            links = [i['url'] for i in result]

            for u in links:
                try:
                    import commonresolvers
                    i = commonresolvers.google(u)[0]
                    url = getUrl(i['url'], output='geturl').result
                    quality = i['quality']

                    sources.append({'source': 'Moviezone', 'quality': quality, 'provider': 'Moviezone', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class muchmovies:
    def __init__(self):
        self.base_link = 'http://umovies.me'
        self.search_link = '/search/%s'

    def get_movie(self, imdb, title, year):
        try:
            query = urllib.quote_plus(title.replace(' ', '-').rsplit(':', 1)[0])
            query = self.base_link + self.search_link % query

            result = getUrl(query, mobile=True).result
            result = common.parseDOM(result, "ul", attrs = { "class": "movies.+?" })
            result = common.parseDOM(result, "li")

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "h3")[0]) for i in result]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = result.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []
            url = self.base_link + url
            sources.append({'source': 'Muchmovies', 'quality': 'HD', 'provider': 'Muchmovies', 'url': url})
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            result = getUrl(url, mobile=True).result
            url = common.parseDOM(result, "a", ret="href", attrs = { "data-role": "button" })
            url = [i for i in url if str('.mp4') in i][0]
            return url
        except:
            return

class sweflix:
    def __init__(self):
        self.base_link = 'https://sweflix.net'
        self.search_link = '/index.php?act=query&query=%s'
        self.footer_link = '/film_api.php?target=footer&fid=%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "hover-group.+?" })

            title = cleantitle().movie(title)
            years = ['>%s<' % str(year), '>%s<' % str(int(year)+1), '>%s<' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="data-movieid")[0], common.parseDOM(i, "h5")[-1], common.parseDOM(i, "p")[-1]) for i in result]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

            url = result.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + self.footer_link % url
            result = getUrl(url).result

            url = common.parseDOM(result, "a", ret="href")
            url = [i for i in url if 'play/' in i][0]
            url = self.base_link + url

            result = getUrl(url).result

            url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/.+?" })[0]
            if '1080p' in url: quality = '1080p'
            else: quality = 'HD'

            sources.append({'source': 'Sweflix', 'quality': quality, 'provider': 'Sweflix', 'url': url})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url

class movieshd:
    def __init__(self):
        self.base_link = 'http://movieshd.co'
        self.search_link = '/?s=%s'
        self.player_link = 'http://videomega.tv/iframe.php?ref=%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = common.parseDOM(result, "ul", attrs = { "class": "listing-videos.+?" })[0]
            result = common.parseDOM(result, "li", attrs = { "class": ".+?" })

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a", ret="title")[0])  for i in result]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = result.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + url
            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "class": "video-embed" })[0]

            url = re.compile("data-rocketsrc='(.+?)'").findall(result)
            url = [i for i in url if 'hashkey' in i]
            if len(url) > 0: result = getUrl(url[0]).result
            url = re.compile('ref=[\'|\"](.+?)[\'|\"]').findall(result)[0]

            url = self.player_link % url
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.videomega(url)
            if url == None: raise Exception()

            sources.append({'source': 'Videomega', 'quality': 'HD', 'provider': 'MoviesHD', 'url': url})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

class niter:
    def __init__(self):
        self.base_link = 'http://niter.tv'
        self.search_link = '/typeahead/%s'
        self.movie_link = '/movies/%s'
        self.pk_link = '/player/pk/pk/plugins/player_p2.php?url=%s'

    def get_movie(self, imdb, title, year):
        try:
            query = urllib.quote(title)
            query = self.base_link + self.search_link % query

            request = urllib2.Request(query)
            request.add_header('X-Requested-With', 'XMLHttpRequest')
            response = urllib2.urlopen(request, timeout=5)
            result = response.read()
            response.close()

            title = cleantitle().movie(title)
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            result = json.loads(result)
            url = [i['id'] for i in result if title == cleantitle().movie(i['title'])][0]
            url = self.base_link + self.movie_link % str(url)

            result = getUrl(url).result
            result = common.parseDOM(result, "a", attrs = { "class": "title-title" })[0]
            y = re.compile('(\d{4})').findall(result)[-1]
            if not any(x == str(y) for x in years): raise Exception()

            url = url.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            base = self.base_link + url
            result = getUrl(base).result
            result = common.parseDOM(result, "div", attrs = { "id": "videoParameter" })[0]
            result = result.replace('pic=', '')

            links = result.split('&')[:3]

            for i in links:
                try:
                    url = self.base_link + self.pk_link % i
                    result = getUrl(url, referer=base).result
                    result = json.loads(result)

                    url = [i['url'] for i in result if 'x-shockwave-flash' in i['type']]
                    url += [i['url'] for i in result if 'video/mpeg4' in i['type']]
                    url = url[-1]
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    sources.append({'source': 'Niter', 'quality': 'HD', 'provider': 'Niter', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class yify:
    def __init__(self):
        self.base_link = 'http://yify.tv'
        self.search_link = '/wp-admin/admin-ajax.php'
        self.pk_link = '/reproductor2/pk/pk/plugins/player_p2.php?url=%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link
            post = urllib.urlencode({'action': 'ajaxy_sf', 'sf_value': title})

            result = getUrl(query, post=post).result
            result = result.replace('&#8211;','-').replace('&#8217;','\'')
            result = json.loads(result)
            result = result['post']['all']

            title = cleantitle().movie(title)
            url = [i['post_link'] for i in result if title == cleantitle().movie(i['post_title'])][0]

            result = getUrl(url).result
            if not str('tt' + imdb) in result: raise Exception()

            url = url.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            base = self.base_link + url
            result = getUrl(base).result

            i = re.compile('showPkPlayer[(]"(.+?)"[)]').findall(result)[0]

            url = self.base_link + self.pk_link % i
            result = getUrl(url, referer=base).result
            result = json.loads(result)

            url = [i['url'] for i in result if 'x-shockwave-flash' in i['type']]
            url += [i['url'] for i in result if 'video/mpeg4' in i['type']]
            url = url[-1]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            sources.append({'source': 'YIFY', 'quality': 'HD', 'provider': 'YIFY', 'url': url})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class movietv:
    def __init__(self):
        self.base_link = 'http://movietv.to'
        self.moviesearch_link = '/titles/paginate?query=%s&type=movie&availToStream=true'
        self.tvsearch_link = '/titles/paginate?query=%s&type=series&availToStream=true'

    def get_movie(self, imdb, title, year):
        try:
            url = '%s (%s)' % (title, year)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, show, show_alt, year):
        try:
            url = '%s (%s)' % (show, year)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        try:
            url = '%s S%02dE%02d' % (url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            content = re.compile('(.+?)S\d*E\d*$').findall(url)

            if len(content) == 0:
                title, year = re.compile('(.+?) [(](\d{4})[)]$').findall(url)[0]

                query = urllib.quote_plus(title)
                query = self.base_link + self.moviesearch_link % query

                result = getUrl(query, referer=self.base_link).result
                result = json.loads(result)
                result = result['items']

                title = cleantitle().movie(title)
                years = [str(year), str(int(year)+1), str(int(year)-1)]
                result = [i for i in result if title == cleantitle().movie(i['title'])]
                result = [i for i in result if any(x in str(i['year']) for x in years)][0]

                url = result['link'][0]['url']
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

            else:
                title, year, season, episode = re.compile('(.+?) [(](\d{4})[)] S(\d*)E(\d*)$').findall(url)[0]
                season, episode = '%01d' % int(season), '%01d' % int(episode)

                query = urllib.quote_plus(title)
                query = self.base_link + self.tvsearch_link % query

                result = getUrl(query, referer=self.base_link).result
                result = json.loads(result)
                result = result['items']

                title = cleantitle().tv(title)
                years = [str(year), str(int(year)+1), str(int(year)-1)]
                result = [i for i in result if title == cleantitle().tv(i['title'])]
                result = [i for i in result if any(x in str(i['year']) for x in years)][0]

                url = result['link']
                url = [i for i in url if str(i['season']) == season and str(i['episode']) == episode][0]
                url = url['url']
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

            sources.append({'source': 'MovieTV', 'quality': 'SD', 'provider': 'MovieTV', 'url': url})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            cookie = getUrl(self.base_link, output='cookie').result

            url += "|Cookie=%s" % urllib.quote(cookie + '; aoe=fm')
            return url
        except:
            return

class ororo:
    def __init__(self):
        self.base_link = 'http://ororo.tv'
        self.key_link = base64.urlsafe_b64decode('dXNlciU1QnBhc3N3b3JkJTVEPWMyNjUxMzU2JnVzZXIlNUJlbWFpbCU1RD1jMjY1MTM1NiU0MGRyZHJiLmNvbQ==')
        self.sign_link = 'http://ororo.tv/users/sign_in'

    def get_show(self, imdb, show, show_alt, year):
        try:
            result = getUrl(self.base_link).result
            if not "'index show'" in result:
                cookie = getUrl(self.sign_link, post=self.key_link, output='cookie').result
                result = getUrl(self.base_link, cookie=cookie).result

            result = common.parseDOM(result, "div", attrs = { "class": "index show" })
            result = [(common.parseDOM(i, "a", attrs = { "class": "name" })[0], common.parseDOM(i, "span", attrs = { "class": "value" })[0], common.parseDOM(i, "a", ret="href")[0]) for i in result]

            shows = [cleantitle().tv(show), cleantitle().tv(show_alt)]
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            result = [i for i in result if any(x in i[1] for x in years)]
            result = [i[2] for i in result if any(x == cleantitle().tv(i[0]) for x in shows)][0]

            url = result.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        try:
            url = self.base_link + url

            result = getUrl(url).result
            if not "menu season-tabs" in result:
                cookie = getUrl(self.sign_link, post=self.key_link, output='cookie').result
                result = getUrl(url, cookie=cookie).result

            url = common.parseDOM(result, "a", ret="data-href", attrs = { "href": "#%01d-%01d" % (int(season), int(episode)) })[0]

            url = url.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []
            url = self.base_link + url
            sources.append({'source': 'Ororo', 'quality': 'SD', 'provider': 'Ororo', 'url': url})
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            result = getUrl(url).result
            if not "my_video" in result:
                cookie = getUrl(self.sign_link, post=self.key_link, output='cookie').result
                result = getUrl(url, cookie=cookie).result

            url = None
            try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/webm" })[0]
            except: pass
            try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/mp4" })[0]
            except: pass

            if url == None: return
            if not url.startswith('http://'): url = '%s%s' % (self.base_link, url)
            url = '%s|Cookie=%s' % (url, urllib.quote_plus('video=true'))

            return url
        except:
            return

class vkbox:
    def __init__(self):
        self.base_link = 'http://mobapps.cc'
        self.data_link = '/data/data_en.zip'
        self.moviedata_link = 'movies_lite.json'
        self.tvdata_link = 'tv_lite.json'
        self.movie_link = '/api/serials/get_movie_data/?id=%s'
        self.show_link = '/api/serials/es?id=%s'
        self.episode_link = '/api/serials/e/?h=%s&u=%01d&y=%01d'
        self.vk_link = 'https://vk.com/video_ext.php?oid=%s&id=%s&hash=%s'

    def get_movie(self, imdb, title, year):
        try:
            import zipfile, StringIO
            query = self.base_link + self.data_link
            data = urllib2.urlopen(query, timeout=5).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            result = zip.read(self.moviedata_link)
            zip.close()

            imdb = 'tt' + imdb
            result = json.loads(result)
            result = [i['id'] for i in result if imdb == i['imdb_id']][0]

            url = self.movie_link % result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, show, show_alt, year):
        try:
            import zipfile, StringIO
            query = self.base_link + self.data_link
            data = urllib2.urlopen(query, timeout=5).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            result = zip.read(self.tvdata_link)
            zip.close()

            imdb = 'tt' + imdb
            result = json.loads(result)
            result = [i['id'] for i in result if imdb == i['imdb_id']][0]

            url = self.show_link % result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        url = url.rsplit('id=', 1)[-1]
        url = self.episode_link % (url, int(season), int(episode))
        url = common.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + url

            import urlparse
            par = urlparse.parse_qs(urlparse.urlparse(url).query)
            try: num = int(par['h'][0]) + int(par['u'][0]) + int(par['y'][0])
            except: num = int(par['id'][0]) + 537

            request = urllib2.Request(url)
            request.add_header('User-Agent', 'android-async-http/1.4.1 (http://loopj.com/android-async-http)')
            response = urllib2.urlopen(request, timeout=5)
            result = response.read()
            response.close()

            result = json.loads(result)
            try: result = result['langs']
            except: pass
            i = [i for i in result if i['lang'] == 'en'][0]

            url = (str(int(i['apple']) + num), str(int(i['google']) + num), i['microsoft'])
            url = self.vk_link % url

            import commonresolvers
            url = commonresolvers.vk(url)

            for i in url: sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'VKBox', 'url': i['url']})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

class clickplay:
    def __init__(self):
        self.base_link = 'http://clickplay.to'
        self.search_link = '/search/%s'
        self.episode_link = '%sseason-%01d/episode-%01d'

    def get_show(self, imdb, show, show_alt, year):
        try:
            query = ' '.join([i for i in show.split() if i not in ['The','the','A','a']])
            query = self.base_link + self.search_link % urllib.quote_plus(query)

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "id": "video_list" })[0]
            result = result.split('</a>')
            result = [(common.parseDOM(i, "span", attrs = { "class": "article-title" }), common.parseDOM(i, "a", ret="href")) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if not (len(i[0]) == 0 or len(i[1]) == 0)]

            shows = [cleantitle().tv(show), cleantitle().tv(show_alt)]
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [i for i in result if any(x == cleantitle().tv(i[0]) for x in shows)]
            result = [i[1] for i in result if any(x in i[0] for x in years)][0]

            url = result.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        url = self.episode_link % (url, int(season), int(episode))
        url = common.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + url

            result = getUrl(url).result
            u = common.parseDOM(result, "meta", ret="content", attrs = { "property": "og:url" })[0]
            links = re.compile('<a href="([?]link_id=.+?)".+?>\[720p\].+?</a>').findall(result)
            links = [u + i for i in links]

            import gkdecrypter

            for u in links[:3]:
                try:
                    result = getUrl(u).result
                    url = re.compile('proxy[.]link=clickplay[*](.+?)"').findall(result)[-1]
                    url = gkdecrypter.decrypter(198,128).decrypt(url,base64.urlsafe_b64decode('bW5pcUpUcUJVOFozS1FVZWpTb00='),'ECB').split('\0')[0]

                    if not 'vk.com' in url: raise Exception()

                    import commonresolvers
                    vk = commonresolvers.vk(url)

                    for i in vk: sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'Clickplay', 'url': i['url']})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class moviestorm:
    def __init__(self):
        self.base_link = 'http://moviestorm.eu'
        self.search_link = '/search?q=%s'
        self.episode_link = '%s?season=%01d&episode=%01d'

    def get_movie(self, imdb, title, year):
        try:
            query = urllib.quote_plus(title)
            query = self.base_link + self.search_link % query

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "movie_box" })

            imdb = 'tt' + imdb
            result = [i for i in result if imdb in i][0]
            result = common.parseDOM(result, "a", ret="href")[0]

            url = result.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, show, show_alt, year):
        try:
            query = urllib.quote_plus(show)
            query = self.base_link + self.search_link % query

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "movie_box" })

            imdb = 'tt' + imdb
            result = [i for i in result if imdb in i][0]
            result = common.parseDOM(result, "a", ret="href")[0]

            url = result.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        url = self.episode_link % (url, int(season), int(episode))
        url = common.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            url = self.base_link + url

            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "class": "links" })[0]
            result = common.parseDOM(result, "tr")
            result = [(common.parseDOM(i, "td", attrs = { "class": "quality_td" })[0], common.parseDOM(i, "a", ret="href")[-1]) for i in result]

            ts_quality = ['CAM', 'TS']
            links = [i for i in result if not any(x in i[0] for x in ts_quality)]
            if len(links) == 0: links = result

            for i in links:
                try:
                    url = i[1]
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.sub('.+?/exit/\d*-|[.].+?[.]html|http://(|www[.])|/.+|[.].+$','', i[1])
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    if any(x in i[0] for x in ts_quality): quality = 'CAM'
                    else: quality = 'SD'

                    sources.append({'source': host, 'quality': quality, 'provider': 'Moviestorm', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            if url.startswith(self.base_link):
                result = getUrl(url).result
                url = common.parseDOM(result, "a", ret="href", attrs = { "class": "real_link" })[0]

            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class einthusan:
    def __init__(self):
        self.base_link = 'http://www.einthusan.com'
        self.search_link = '/search/?search_query=%s&lang=%s'

    def get_movie(self, imdb, title, year):
        try:
            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if not 'India' in country: return

            languages = ['hindi', 'tamil', 'telugu', 'malayalam']
            language = [i.strip().lower() for i in search['Language'].split(',')]
            language = [i for i in language if any(x == i for x in languages)][0]

            query = urllib.quote_plus(title)
            query = self.base_link + self.search_link % (query, language)

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "search-category" })
            result = [i for i in result if 'Movies' in common.parseDOM(i, "p")[0]][0]
            result = common.parseDOM(result, "li")

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a")[0]) for i in result]
            r = [i for i in result if any(x in i[1] for x in years)]
            if not len(r) == 0: result = r
            result = [i[0] for i in result if title == cleantitle().movie(i[1])][0]

            url = result.replace(self.base_link, '')
            url = url.replace('../', '/')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []
            url = self.base_link + url
            sources.append({'source': 'Einthusan', 'quality': 'HD', 'provider': 'Einthusan', 'url': url})
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            result = getUrl(url).result
            url = re.compile("'file': '(.+?)'").findall(result)[0]
            return url
        except:
            return

class myvideolinks:
    def __init__(self):
        self.base_link = 'http://myvideolinks.xyz'
        self.search_link = '/?s=%s'

    def get_movie(self, imdb, title, year):
        try:
            url = '%s %s' % (title, year)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            query = urllib.quote_plus(url)
            query = self.base_link + self.search_link % query

            result = getUrl(query).result
            links = common.parseDOM(result, "div", attrs = { "class": "archive" })

            title, hdlr = re.compile('(.+?) (\d{4})$').findall(url)[0]
            title = cleantitle().movie(title)
            hdlr = [str(hdlr), str(int(hdlr)+1), str(int(hdlr)-1)]

            dt = int(datetime.datetime.now().strftime("%Y%m%d"))

            for link in links:
                try:
                    name = common.parseDOM(link, "a", attrs = { "title": ".+?" })[-1]
                    name = common.replaceHTMLCodes(name)

                    url = common.parseDOM(link, "a", ret="href")[0]
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    date = re.compile('(/\d{4}/\d{2}/\d{2}/)').findall(url)[0]
                    date = re.sub('[^0-9]', '', str(date))
                    if (abs(dt - int(date)) < 100) == False: raise Exception()

                    cat = common.parseDOM(link, "a", attrs = { "rel": "category tag" })
                    if not any(i.endswith(('3-D Movies', 'BDRip', 'BluRay')) for i in cat): raise Exception()

                    t = re.sub('(\.|\(|\[|\s)(\d{4})(\.|\)|\]|\s)(.+)', '', name)
                    t = cleantitle().movie(t)
                    if not t == title: raise Exception()

                    y = re.compile('[\.|\(|\[|\s](\d{4})[\.|\)|\]|\s]').findall(name)[-1]
                    if not any(i == y for i in hdlr): raise Exception()

                    fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4})(\.|\)|\]|\s)', '', name)
                    fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                    fmt = [i.lower() for i in fmt]

                    if '1080p' in fmt: quality = '1080p'
                    else: quality = 'HD'

                    info = ''
                    size = re.compile('Size: (.+? [M|G]B) ').findall(link)
                    if len(size) > 0:
                        size = size[-1]
                        if size.endswith(' GB'): div = 1
                        else: div = 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                        info += '%.2f GB | %s' % (size, quality)
                    else:
                        info += '%s' % quality

                    if '3-D Movies' in cat:
                        info += ' | 3D'

                    try:
                        result = getUrl(url).result
                        result = common.parseDOM(result, "ul")
                        result = str(result)
                    except:
                        pass

                    result = common.parseDOM(result, "a", ret="href")

                    for i in result:
                        try:
                            url = i
                            url = common.replaceHTMLCodes(url)
                            url = url.encode('utf-8')

                            host = re.sub('http(|s)://|www[.]|/.+|[.].+$','', url)
                            host = host.strip().lower()
                            if not host in hosthdDict: raise Exception()

                            info2 = '%s | %s' % (host, info)
                            info2 = info2.upper()

                            sources.append({'source': host, 'quality': quality, 'provider': 'Myvideolinks', 'url': url, 'info': info2})
                        except:
                            pass
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class tvrelease:
    def __init__(self):
        self.base_link = 'http://tv-release.net'
        self.search_link = '/?s=%s&cat=TV-720p'

    def get_show(self, imdb, show, show_alt, year):
        try:
            url = show
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        try:
            url = '%s S%02dE%02d' % (url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            query = url.replace('\'', '').replace('.', ' ')
            query = re.sub('\s+',' ',query)
            query = self.base_link + self.search_link % urllib.quote_plus(query)

            result = getUrl(query).result
            links = common.parseDOM(result, "table", attrs = { "class": "posts_table" })

            title, hdlr = re.compile('(.+?) (S\d*E\d*)$').findall(url)[0]
            title = cleantitle().tv(title)
            hdlr = [hdlr]

            dt = int(datetime.datetime.now().strftime("%Y%m%d"))

            for link in links:
                try:
                    name = common.parseDOM(link, "a")[-1]
                    name = common.replaceHTMLCodes(name)

                    url = common.parseDOM(link, "a", ret="href")[-1]
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    date = re.compile('(\d{4}-\d{2}-\d{2})').findall(link)[-1]
                    date = re.sub('[^0-9]', '', str(date))
                    if (abs(dt - int(date)) < 100) == False: raise Exception()

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|3D)(\.|\)|\]|\s)(.+)', '', name)
                    t = cleantitle().tv(t)
                    if not t == title: raise Exception()

                    y = re.compile('[\.|\(|\[|\s](S\d*E\d*)[\.|\)|\]|\s]').findall(name)[-1]
                    if not any(x == y for x in hdlr): raise Exception()

                    fmt = re.sub('(.+)(\.|\(|\[|\s)(S\d*E\d*)(\.|\)|\]|\s)', '', name)
                    fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                    fmt = [i.lower() for i in fmt]

                    if '1080p' in fmt: quality = '1080p'
                    else: quality = 'HD'

                    info = ''
                    size = common.parseDOM(link, "td")
                    size = [i for i in size if i.endswith((' MB', ' GB'))]
                    if len(size) > 0:
                        size = size[-1]
                        if size.endswith(' GB'): div = 1
                        else: div = 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                        info += '%.2f GB | %s' % (size, quality)
                    else:
                        info += '%s' % quality

                    result = getUrl(url).result
                    result = common.parseDOM(result, "td", attrs = { "class": "td_cols" })[0]
                    result = result.split('"td_heads"')

                    for i in result:
                        try:
                            url = common.parseDOM(i, "a", ret="href")
                            if not len(url) == 1: raise Exception()
                            url = url[0]
                            url = common.replaceHTMLCodes(url)
                            url = url.encode('utf-8')

                            host = re.sub('http(|s)://|www[.]|/.+|[.].+$','', url)
                            host = host.strip().lower()
                            if not host in hosthdDict: raise Exception()

                            info2 = '%s | %s' % (host, info)
                            info2 = info2.upper()

                            sources.append({'source': host, 'quality': quality, 'provider': 'TVrelease', 'url': url, 'info': info2})
                        except:
                            pass
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class directdl:
    def __init__(self):
        self.base_link = 'http://directdownload.tv'
        self.search_link = '/index/search/keyword/%s/qualities/hdtv,dvdrip,realhd,webdl,webdl1080p/from/0/search'

    def get_show(self, imdb, show, show_alt, year):
        try:
            url = show
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        try:
            url = '%s S%02dE%02d' % (url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            query = self.base_link
            post = urllib.urlencode({'username': 'gen', 'password': 'gen', 'Login': 'Login', 'mode': 'normal'})
            cookie = getUrl(query, post=post, output='cookie').result

            query = urllib.quote_plus(url)
            query = self.base_link + self.search_link % query

            result = getUrl(query, cookie=cookie).result
            result = json.loads(result)
            links = result

            title, hdlr = re.compile('(.+?) (S\d*E\d*)$').findall(url)[0]
            title = cleantitle().tv(title)
            hdlr = [hdlr]

            for link in links:
                try:
                    name = link['release']
                    name = common.replaceHTMLCodes(name)

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|3D)(\.|\)|\]|\s)(.+)', '', name)
                    t = cleantitle().tv(t)
                    if not t == title: raise Exception()

                    y = re.compile('[\.|\(|\[|\s](S\d*E\d*)[\.|\)|\]|\s]').findall(name)[-1]
                    if not any(x == y for x in hdlr): raise Exception()

                    p = link['links']
                    p = [i['hostname'] for i in p]
                    if not len(p) == len(uniqueList(p).list): raise Exception()

                    quality = link['quality']
                    quality = common.replaceHTMLCodes(quality)

                    if quality == 'webdl1080p': quality = '1080p'
                    elif quality in ['realhd', 'webdl']: quality = 'HD'
                    else: quality = 'SD'

                    size = link['size']
                    size = float(size)/1024

                    info = '%.2f GB | %s' % (size, quality)
                    info = info.upper()

                    result = link['links']

                    for i in result:
                        try:
                            url = i['url']
                            url = common.replaceHTMLCodes(url)
                            url = url.encode('utf-8')

                            host = re.sub('http(|s)://|www[.]|/.+|[.].+$','', url)
                            host = host.strip().lower()
                            if not host in hosthdDict: raise Exception()

                            info2 = '%s | %s' % (host, info)
                            info2 = info2.upper()

                            sources.append({'source': host, 'quality': quality, 'provider': 'DirectDL', 'url': url, 'info': info2})
                        except:
                            pass
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.get(url)
            return url
        except:
            return

class noobroom:
    def __init__(self):
        self.base_link = 'http://superchillin.com'
        self.search_link = '/search.php?q=%s'
        self.login_link = '/login.php'
        self.login2_link = '/login2.php'
        self.mail = xbmcaddon.Addon().getSetting("noobroom_mail")
        self.password = xbmcaddon.Addon().getSetting("noobroom_password")
        self.login()

    def login(self):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()
            post = urllib.urlencode({'email': self.mail, 'password': self.password})
            getUrl(self.base_link + self.login_link, close=False).result
            getUrl(self.base_link + self.login_link, output='cookie').result
            result = urllib2.Request(self.base_link + self.login2_link, post)
            urllib2.urlopen(result, timeout=5)
        except:
            return

    def get_movie(self, imdb, title, year):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()

            query = urllib.quote_plus(title)
            query = self.base_link + self.search_link % query

            result = getUrl(query).result
            result = re.compile('(<i>Movies</i>.+)').findall(result)[0]
            result = result.split("'tippable'")

            title = '>' + cleantitle().movie(title) + '<'
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [i for i in result if any(x in i for x in years)]
            result = [i for i in result if title in cleantitle().movie(i)][0]
            result = re.compile("href='(.+?)'").findall(result)[0]

            url = result.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, show, show_alt, year):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()

            query = urllib.quote_plus(show)
            query = self.base_link + self.search_link % query

            result = getUrl(query).result
            result = re.compile('(<i>TV Series</i>.+)').findall(result)[0]
            result = result.replace('(incomplete)', '')
            result = result.split("><a ")

            title = '>' + cleantitle().tv(show) + '<'
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            result = [i for i in result if title in cleantitle().tv(i)][0]
            result = re.compile("href='(.+?)'").findall(result)[:2]

            for i in result:
                try:
                    result = getUrl(self.base_link + i).result
                    y = re.compile('\d*-\d*-(\d{4})').findall(result)[0]
                    if any(x == y for x in years):
                        match = i
                        break
                except:
                    pass

            url = match.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        try:
            url = self.base_link + url

            result = getUrl(url).result
            result = re.compile("<b>%01dx%02d .+?style=.+? href='(.+?)'" % (int(season), int(episode))).findall(result)[0]

            url = result.replace(self.base_link, '')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []
            url = self.base_link + url
            sources.append({'source': 'Noobroom', 'quality': 'HD', 'provider': 'Noobroom', 'url': url})
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            result = getUrl(url).result
            result = re.compile('"file": "(.+?)"').findall(result)

            url = [i for i in result if 'type=flv' in i]
            url += [i for i in result if 'type=mp4' in i]
            url = self.base_link + url[-1]

            try: url = getUrl(url, output='geturl').result
            except: pass
            try: url = getUrl(url.replace('&hd=0', '&hd=1'), output='geturl').result
            except: pass

            return url
        except:
            return

class furk:
    def __init__(self):
        self.base_link = 'http://api.furk.net'
        self.search_link = '/api/plugins/metasearch'
        self.login_link = '/api/login/login'
        self.user = xbmcaddon.Addon().getSetting("furk_user")
        self.password = xbmcaddon.Addon().getSetting("furk_password")

    def get_movie(self, imdb, title, year):
        try:
            if (self.user == '' or self.password == ''): raise Exception()

            url = '%s %s' % (title, year)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, show, show_alt, year):
        try:
            if (self.user == '' or self.password == ''): raise Exception()

            url = show
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, title, date, season, episode):
        try:
            if (self.user == '' or self.password == ''): raise Exception()

            url = '%s S%02dE%02d' % (url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict):
        try:
            sources = []

            if (self.user == '' or self.password == ''): raise Exception()

            query = self.base_link + self.login_link
            post = urllib.urlencode({'login': self.user, 'pwd': self.password})
            cookie = getUrl(query, post=post, output='cookie').result

            query = self.base_link + self.search_link
            post = urllib.urlencode({'sort': 'relevance', 'filter': 'all', 'moderated': 'yes', 'offset': '0', 'limit': '100', 'match': 'all', 'q': url})
            result = getUrl(query, post=post, cookie=cookie).result
            result = json.loads(result)
            links = result['files']

            title, hdlr = re.compile('(.+?) (\d{4}|S\d*E\d*)$').findall(url)[0]

            if hdlr.isdigit():
                type = 'movie'
                title = cleantitle().movie(title)
                hdlr = [str(hdlr), str(int(hdlr)+1), str(int(hdlr)-1)]
            else:
                type = 'episode'
                title = cleantitle().tv(title)
                hdlr = [hdlr]

            for i in links:
                try:
                    info = i['video_info']
                    if type == 'movie' and not '#0:1(eng): Audio:' in info: raise Exception()

                    name = i['name']
                    name = common.replaceHTMLCodes(name)

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|3D)(\.|\)|\]|\s)(.+)', '', name)
                    if type == 'movie': t = cleantitle().movie(t)
                    else: t = cleantitle().tv(t)
                    if not t == title: raise Exception()

                    y = re.compile('[\.|\(|\[|\s](\d{4}|S\d*E\d*)[\.|\)|\]|\s]').findall(name)[-1]
                    if not any(x == y for x in hdlr): raise Exception()

                    fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*)(\.|\)|\]|\s)', '', name)
                    fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                    fmt = [x.lower() for x in fmt]

                    if any(x.endswith(('subs', 'sub', 'dubbed', 'dub')) for x in fmt): raise Exception()
                    if any(x in ['extras'] for x in fmt): raise Exception()

                    res = i['video_info'].replace('\n','')
                    res = re.compile(', (\d*)x\d*').findall(res)[0]
                    res = int(res)
                    if 1900 <= res <= 1920: quality = '1080p'
                    elif 1200 <= res <= 1280: quality = 'HD'
                    else: quality = 'SD'
                    if any(x in ['dvdscr', 'r5', 'r6'] for x in fmt): quality = 'SCR'
                    elif any(x in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'ts'] for x in fmt): quality = 'CAM'

                    size = i['size']
                    size = float(size)/1073741824
                    if int(size) > 2 and not quality in ['1080p', 'HD']: raise Exception()
                    if int(size) > 5: raise Exception()

                    url = i['url_pls']
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    info = i['video_info'].replace('\n','')
                    v = re.compile('Video: (.+?),').findall(info)[0]
                    a = re.compile('Audio: (.+?), .+?, (.+?),').findall(info)[0]
                    q = quality
                    if '3d' in fmt: q += ' | 3D'

                    info = '%.2f GB | %s | %s | %s | %s' % (size, q, v, a[0], a[1])
                    info = re.sub('\(.+?\)', '', info)
                    info = info.replace('stereo', '2.0')
                    info = ' '.join(info.split())
                    info = info.upper()

                    sources.append({'source': 'Furk', 'quality': quality, 'provider': 'Furk', 'url': url, 'info': info})
                except:
                    pass

            if not all(i['quality'] in ['CAM', 'SCR'] for i in sources): 
                sources = [i for i in sources if not i['quality'] in ['CAM', 'SCR']]

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            query = self.base_link + self.login_link
            post = urllib.urlencode({'login': self.user, 'pwd': self.password})
            cookie = getUrl(query, post=post, output='cookie').result

            result = getUrl(url, cookie=cookie).result
            url = common.parseDOM(result, "location")[0]
            return url
        except:
            return
