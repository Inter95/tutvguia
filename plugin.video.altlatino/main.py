# coding: utf-8
# Main Addon
__author__ = 'mancuniancol'

from xbmcswift2 import Plugin
from tools import *


##SOME FUNCTIONS
def unshorten_adfly(uri):  # using the code from https://github.com/jkehler/unshortenit
    import re
    from base64 import b64decode
    try:
        _headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding': 'gzip,deflate,sdch',
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36'}
        _adfly_regex = r'adf\.ly|q\.gs|j\.gs|u\.bb|ay\.gy'
        _timeout = 10
        r = requests.get(uri, headers=_headers, timeout=_timeout)
        html = r.text
        ysmm = re.findall(r"var ysmm =.*\;?", html)

        if len(ysmm) > 0:
            ysmm = re.sub(r'var ysmm \= \'|\'\;', '', ysmm[0])

            left = ''
            right = ''

            for c in [ysmm[i:i + 2] for i in range(0, len(ysmm), 2)]:
                left += c[0]
                right = c[1] + right

            decoded_uri = b64decode(left.encode() + right.encode())[2:].decode()

            if re.search(r'go\.php\?u\=', decoded_uri):
                decoded_uri = b64decode(re.sub(r'(.*?)u=', '', decoded_uri)).decode()

            return decoded_uri
        else:
            return uri, 'No ysmm variable found'

    except Exception as e:
        return uri


def get_torrent(url_code):
    browser1 = requests.session()
    response = browser1.get(url_code)
    code = re.search('{id:(.*?),', response.text).group(1)
    response = browser1.get('%s/ajax/download.html?id=%s&code=0' % (settings.value["urlAddress"], code))
    url_adfly = response.text
    settings.log("AdFly Url:", url_adfly)
    result = unshorten_adfly(url_adfly)
    settings.log("magnet:", result)
    return result


def getData(data=""):
    datos = re.search("var datos =(.*?);", data, re.DOTALL).group(1).replace("{", "").replace("}", "")
    params = {}
    for item in datos.split("\n"):
        if item.strip() != "":
            key, value = item.strip()[:-1].split(':')
            params[key] = value.replace("'", "")
    # settings.debug(params)
    opciones = re.search("var options =(.*?);", data, re.DOTALL).group(1).replace("{", "").replace("}", "") + ": ''"
    params1 = {}
    for item in opciones.split("\n"):
        if item.strip() != "":
            key, value = item.strip()[:-1].split(':')
            params1[key] = value.replace("'", "")
    # settings.debug(params1)
    urlPage = re.search('url: "(.*?)"', data).group(1)
    return urlPage, params, params1["totalPages"]


##INITIALISATION
storage = Storage(settings.storageName, type="dict", eval=True)
plugin = Plugin()
isLogin = False
# Getting the cookies from cache
cookies = plugin.get_storage('cookies', TTL=5)
if settings.value["user"] == "" or settings.value["password"] == "":
    settings.dialog.ok(settings.cleanName, "Por favor, suministre su usuario y clave")
    settings.settings.openSettings()
    settings = Settings()

if len(cookies.items()) < 2:
    settings.log("Asking the new credentials")
    browser.get(settings.value["urlAddress"] + "/")
    goodSpider()
    params = {"user": settings.value["user"],
              "password": settings.value["password"]}
    browser.post(settings.value["urlAddress"] + "/ajax/login_check_user.php", data={"user": settings.value["user"]})
    browser.post(settings.value["urlAddress"] + "/ajax/login_check_pass.php", data=params)
    browser.post(settings.value["urlAddress"] + "/ajax/login_check.php", data=params)
    cookies.update(browser.cookies.items())
    cookies.sync()
    goodSpider()
else:
    settings.log("Taking credentials from cache")
    requests.utils.add_dict_to_cookiejar(browser.cookies, cookies)

settings.debug(cookies.items())
response = browser.get(settings.value["urlAddress"] + "/")
if response.text.find(settings.value["user"]) < 0:
    settings.dialog.ok(settings.cleanName, "Credenciales incorrectas")
    cookies.update({})
    cookies.sync()
    settings.settings.openSettings()
    settings = Settings()
else:
    isLogin = True


###############################
###  MENU    ##################
###############################

@plugin.route('/')
def index():
    if isLogin:
        textViewer(plugin.get_string(32000), once=True)
        items = [
            {'label': "Busqueda Manual",
             'path': plugin.url_for('search'),
             'thumbnail': dirImages("busqueda-manual.png"),
             'properties': {'fanart_image': settings.fanart}
             },
            {'label': "Estrenos",
             'path': plugin.url_for('readItems', url="/"),
             'thumbnail': dirImages("estrenos.png"),
             'properties': {'fanart_image': settings.fanart}
             },
            {'label': "Calidad",
             'path': plugin.url_for('quality'),
             'thumbnail': dirImages("calidad.png"),
             'properties': {'fanart_image': settings.fanart}
             },
            {'label': "Género",
             'path': plugin.url_for('genres'),
             'thumbnail': dirImages("genero.png"),
             'properties': {'fanart_image': settings.fanart}
             },
            {'label': "Años",
             'path': plugin.url_for('decade'),
             'thumbnail': dirImages("anos.png"),
             'properties': {'fanart_image': settings.fanart}
             },
            {'label': "Ayuda",
             'path': plugin.url_for('help'),
             'thumbnail': dirImages("ayuda.png"),
             'properties': {'fanart_image': settings.fanart}
             }
        ]
    else:
        items = [{'label': 'Reinicie el addon'}]
    return items


@plugin.route('/help/')
def help():
    textViewer(plugin.get_string(32000), once=False)


@plugin.route('/search/')
def search():
    query = settings.dialog.input("Cual película buscar?")
    url = "/?q=%s" % query
    return readItems(url)


@plugin.route('/quality/')
def quality():
    items = [
        {'label': "1080p",
         'path': plugin.url_for('readItems', url="/catalogo/calidad/1080p.html"),
         'thumbnail': dirImages("1080p.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "720p",
         'path': plugin.url_for('readItems', url="/catalogo/calidad/720p.html"),
         'thumbnail': dirImages("720p.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "3D",
         'path': plugin.url_for('readItems', url="/catalogo/calidad/3d.html"),
         'thumbnail': dirImages("3D.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "BLURAY",
         'path': plugin.url_for('readItems', url="/catalogo/calidad/bluray.html"),
         'thumbnail': dirImages("bluray.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "FullHD",
         'path': plugin.url_for('readItems', url="/catalogo/calidad/fullhd.html"),
         'thumbnail': dirImages("fullhd.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "WEBDL-1080p",
         'path': plugin.url_for('readItems', url="/catalogo/calidad/webdl-1080p.html"),
         'thumbnail': dirImages("webdl-1080p.png"),
         'properties': {'fanart_image': settings.fanart}
         },
    ]
    return items


@plugin.route('/genres/')
def genres():
    items = [
        {'label': "Acción",
         'path': plugin.url_for('readItems', url="/catalogo/genero/accion.html"),
         'thumbnail': dirImages("accion.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Animación",
         'path': plugin.url_for('readItems', url="/catalogo/genero/animacion.html"),
         'thumbnail': dirImages("animacion.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Aventura",
         'path': plugin.url_for('readItems', url="/catalogo/genero/aventura.html"),
         'thumbnail': dirImages("aventura.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Ciencia Ficción",
         'path': plugin.url_for('readItems', url="/catalogo/genero/ciencia-ficcion.html"),
         'thumbnail': dirImages("ciencia-ficcion.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Comedia",
         'path': plugin.url_for('readItems', url="/catalogo/genero/comedia.html"),
         'thumbnail': dirImages("comedia.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Crimen",
         'path': plugin.url_for('readItems', url="/catalogo/genero/crimen.html"),
         'thumbnail': dirImages("crimen.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Documental",
         'path': plugin.url_for('readItems', url="/catalogo/genero/documental.html"),
         'thumbnail': dirImages("documental.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Drama",
         'path': plugin.url_for('readItems', url="/catalogo/genero/drama.html"),
         'thumbnail': dirImages("drama.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Familia",
         'path': plugin.url_for('readItems', url="/catalogo/genero/familia.html"),
         'thumbnail': dirImages("familia.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Fantasía",
         'path': plugin.url_for('readItems', url="/catalogo/genero/fantasa.html"),
         'thumbnail': dirImages("fantasia.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Guerra",
         'path': plugin.url_for('readItems', url="/catalogo/genero/guerra.html"),
         'thumbnail': dirImages("guerra.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Historia",
         'path': plugin.url_for('readItems', url="/catalogo/genero/historia.html"),
         'thumbnail': dirImages("historia.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Romance",
         'path': plugin.url_for('readItems', url="/catalogo/genero/romance.html"),
         'thumbnail': dirImages("romance.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Terror",
         'path': plugin.url_for('readItems', url="/catalogo/genero/terror.html"),
         'thumbnail': dirImages("terror.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': "Western",
         'path': plugin.url_for('readItems', url="/catalogo/genero/western.html"),
         'thumbnail': dirImages("western.png"),
         'properties': {'fanart_image': settings.fanart}
         },
    ]
    return items


@plugin.route('/decade/')
def decade():
    from datetime import date
    dec = int(date.today().year / 10) * 10
    items = []
    for decade in range(dec - 50, dec + 10, 10):
        items.append(
            {'label': "%s - %s" % (decade, decade + 9),
             'path': plugin.url_for('years', decade=decade),
             'thumbnail': dirImages("%s-%s.png" % (decade, decade + 9)),
             'properties': {'fanart_image': settings.fanart}
             }
        )
    return items


@plugin.route('/years/<decade>')
def years(decade):
    items = []
    for year in range(int(decade), int(decade) + 10, 1):
        items.append(
            {'label': str(year),
             'path': plugin.url_for('readItems', url="/catalogo/year/%s.html" % year),
             'thumbnail': "DefaultVideo.png",
             'properties': {'fanart_image': settings.fanart}
             }
        )
    return items


@plugin.route('/play/<url>')
def play(url):
    magnet = get_torrent(url)
    # Set-up the plugin
    uri_string = quote_plus(getPlayableLink(uncodeName(magnet)))
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
    # play media
    settings.debug("PlayMedia(%s)" % link)
    xbmc.executebuiltin("PlayMedia(%s)" % link)


@plugin.route('/importOne/<title>/<magnet>')
def importOne(title, magnet):
    info = formatTitle(title)
    if 'MOVIE' in info['type']:
        integration(titles=[title], magnets=[magnet], typeList='MOVIE',
                    folder=settings.movieFolder, silence=True)
    if 'SHOW' in info['type']:
        integration(titles=[title], magnets=[magnet], typeList='SHOW',
                    folder=settings.showFolder, silence=True)
    if 'ANIME' in info['type']:
        integration(titles=[title], magnets=[magnet], typeList='ANIME',
                    folder=settings.animeFolder, silence=True)


@plugin.route('/readItems/<url>', name="readItems")
@plugin.route('/nextPage/<url>/<data>', name="nextPage")
def readItems(url="", data="{'pagina':1}"):
    # read from URL
    settings.log(settings.value["urlAddress"] + url)
    data = eval(data)
    if data['pagina'] == 1:
        response = browser.get(settings.value["urlAddress"] + url)
    else:
        response = browser.post(settings.value["urlAddress"] + url, data=data)
    soup = bs4.BeautifulSoup(response.text)
    links = soup.select("div.thumbnail a.titulo")

    # Items Menu Creation
    plugin.set_content("movies")
    items = []
    for a in links:
        title = a.get("title", "")
        urlSource = settings.value["urlAddress"] + "/" + a["href"]
        settings.debug(title)
        infoTitle = formatTitle(a["href"])  # organize the title information
        infoLabels = getInfoLabels(infoTitle)  # using script.module.metahandlers to the the infoLabels
        settings.debug(infoTitle)
        settings.debug(infoLabels)
        items.append({'label': infoLabels['label'],
                      'path': plugin.url_for('play', url=urlSource),
                      'thumbnail': infoLabels["cover_url"],
                      'properties': {'fanart_image': infoLabels["backdrop_url"]},
                      'info': infoLabels,
                      'stream_info': {'width': infoTitle["width"],
                                      'height': infoTitle["height"],
                                      'duration': infoLabels["duration"],
                                      },
                      'is_playable': True,
                      'context_menu': [
                          (plugin.get_string(32009),
                           'XBMC.RunPlugin(%s)' % plugin.url_for('importOne', title=infoLabels['label'],
                                                                 magnet=urlSource))
                      ]
                      })
    # next page
    urlNext, data, totalPages = getData(response.text)
    data['pagina'] = eval(data['pagina']) + 1
    if data['pagina'] < eval(totalPages):
        items.append({'label': "Página Siguiente..",
                      'path': plugin.url_for('nextPage', url=urlNext, data=str(data)),
                      'thumbnail': settings.icon,
                      'properties': {'fanart_image': settings.fanart}
                      })
    return plugin.finish(items=items, view_mode=settings.value['viewMode'])


if __name__ == '__main__':
    plugin.run()
