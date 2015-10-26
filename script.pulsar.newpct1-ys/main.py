# coding: utf-8
from pulsar import provider
from urllib import unquote_plus
import re
import common

# this read the settings
settings = common.Settings()
# define the browser
browser = common.Browser()
# create the filters
filters = common.Filtering()


# Las siguientes funciones son invocadas desde Pulsar directamente
def extract_torrents(data, query):
    try:
        query_re = query.replace("+","-")
        provider.log.info('Query de busqueda : ' + query + " y query retocada : " + query_re)
        filters.information()  # Pintamos las opciones de filtrado en el log
        data = common.clean_html(data) # Elimina los comentarios que haya ('<!--(.*?)-->')
        cont = 0
        last_item = ''
        pattern = r'<a\shref=[\'"]?([^\'" >]+%s.*?").*?<span>(.*?)</span>.*?<span>(.*?[GB MB])</span>' % query_re
        provider.log.info('Patron : ' + pattern)
        datos_lista = data
        pagina = 0
        while True:
          pagina = pagina + 1
          if datos_lista=='': provider.log.info('Error. No vienen datos ' )
          for cm,(item,fecha,tam) in enumerate(re.findall(pattern, datos_lista)): #http://www.newpct1.com/descarga-torrent/peliculas/carretera-perdida-1997--en--blurayrip-ac3-5-1--peliculas
            nombre_largo = item.split("/")[4]
            provider.log.info("Nombre largo: " + nombre_largo)
            if last_item != item and nombre_largo == query.replace('+','-'):
                provider.log.info('Item url : ' + item) 
                next_url = item.replace(".com/",".com/descarga-torrent/")
                next_url = next_url.replace('"','')
                print next_url
                print next_url.split("/")
                nombre = next_url.split("/")[4]
                browser.open(next_url)
                provider.log.info('Next Url : ' + next_url)
                provider.log.info('Status of browser request : ' + str(browser.status))
                data_next = browser.content
                pattern_next = '<a href="([^"]+)" title="[^"]+" class="btn-torrent" target="_blank">'
                # Con el patron anterior obtengo <a href="http://tumejorjuego.com/download/index.php?link=descargar-torrent/058310_yo-frankenstein-blurayrip-ac3-51.html" title="Descargar torrent de Yo Frankenstein " class="btn-torrent" target="_blank">Descarga tu Archivo torrent!</a>
                
                link =re.findall(pattern_next,data_next)
                link_url = link[0]
                provider.log.info('Link : ' + link_url) 
                provider.log.info('Longitud : '+ str(len(link_url)))
                provider.log.info('Ultimo caracter : ' + link_url[len(link_url)-1])
                if link_url[len(link_url)-1] <> "/": link_url = link_url + "/"
                
                partes = link_url.split("/")
                cadena = partes[ len(partes)-2 ]
                torrent = cadena.split("_")
                provider.log.info(torrent)
                provider.log.info('Torrent : ' + torrent[0])
                cadena = torrent[1].split(".")
                titulo = cadena[0]
                provider.log.info('Titulo : ' + titulo)
                titulo = titulo + ' - ' + fecha + " - " +  tam + " - " + settings.name_provider
                
                if filters.verify(titulo, None):
                    yield {"name": titulo, "uri": link_url}  # devuelve el torrent
                    cont += 1
                else:
                    provider.log.warning(filters.reason)
                if cont == settings.max_magnets:  # limit magnets
                    break  
            if nombre_largo <> query.replace('+','-'): provider.log.info('No se contabliza : nombre_largo: ' + nombre_largo + ' y query : ' + query)
            last_item = item
          # Elimina los comentarios que haya ('<!--(.*?)-->')
          if pagina == 2: break
          if "Next" in datos_lista:
            provider.log.info('Hay mas paginas. Paginamos')
            url_next_page  = re.findall('Next.*?<a href=(.*?)>',datos_lista)[0]
            url_next_page = url_next_page.replace('"',"")
            provider.log.info("Siguiente enlace de paginacion : " + url_next_page)
            browser.content = ''
            browser.open(url_next_page)
            provider.log.info('Status of browser request : ' + str(browser.status))
            if "Next" in browser.content: provider.log.info('<<<<<<<<<<<<ERORRRRR>>>>>>>>>>>>>>>>>>>>>>')
            datos_lista = ''
            datos_lista = browser.content
            datos_lista = common.clean_html(datos_lista)
            # print datos_lista
          else:
             provider.log.info('<<<<<<<<<<<<<<<<<No hay mas paginas. >>>>>>>>>>>><')
             break
        provider.log.info('>>>>>>' + str(cont) + ' torrents sent to Pulsar<<<<<<<')
    except:
        print "Unexpected error:", sys.exc_info()
        provider.log.error('>>>>>>> ERROR parsing data from newpct1<<<<<<<')
        provider.notify(message='ERROR parsing data', header=None, time=5000, image=settings.icon)


def search(query):
    global filters
    query = query.lower()
    filters.title = query  # to do filtering by name
    if settings.extra <> '': query += ' ' + settings.extra
    if settings.time_noti > 0: provider.notify(message="Searching: " + query.encode('utf-8','ignore').title() + '...', header=None, time=settings.time_noti, image=settings.icon)
    query = provider.quote_plus(query.lstrip()) #Esto añade los %20 de los espacios    
    url_search = "%s/index.php?page=buscar&q=%s&ordenar=Nombre&inon=Ascendente&idioma=1" % (settings.url,query)
    provider.log.info(url_search)
    if browser.open(url_search):
        results = extract_torrents(browser.content, query)
    else:
        provider.log.error('>>>>>>>%s<<<<<<<' % browser.status)
        provider.notify(message=browser.status, header=None, time=5000, image=settings.icon)
        results = []
    return results


def search_movie(info):
    filters.use_movie()
    query = common.translator(info['imdb_id'], 'es') #define query in spanish
    provider.log.error('Query extracted using IMDB: %s' % query)
    return search(query)


def search_episode(info):
    filters.use_TV()
    query =  common.clean(info['title']) + ' %dx%02d'% (info['season'],info['episode'])  # define query
    return search(query)

# Hay que registar el modulo para poderlo usar
provider.register(search, search_movie, search_episode)
