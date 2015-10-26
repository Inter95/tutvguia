# -*- coding: utf-8 -*-
from pulsar import provider
import sys
import json
import base64
import re
import urllib
import urllib2
import time
import xbmc
import xbmcaddon
import xbmcplugin
import unicodedata 
from string import maketrans 

API_KEY = "57983e31fb435df4df77afb854740ea9"
BASE_URL = "http://api.themoviedb.org/3"
results = []

temporada = 1
capt = 1
__addon__ = xbmcaddon.Addon(id="script.pulsar.newpct")
__proxy__ = __addon__.getSetting("url_proxy")
__idioma__ = __addon__.getSetting("idioma_xml")
use_screener = __addon__.getSetting("use_screener")
use_3D = __addon__.getSetting("use_3D")
only_HD = __addon__.getSetting("only_HD")
IDIOMA = __idioma__

HEADERS = {
    "Referer": BASE_URL,
}
PAYLOAD = json.loads(base64.b64decode(sys.argv[1]))

def search(query):
    tipo = "peli"
    busqueda_completa = "%s" % query
    pagina_busqueda = __proxy__ + 'buscar-descargas/cID=0&tLang=0&oBy=0&oMode=0&category_=All&subcategory_=All&idioma_=1&calidad_=All&oByAux=0&oModeAux=0&size_=0&q='
    ttt = pagina_busqueda + busqueda_completa
    lectura_pagina(ttt, tipo, query, 0, 0, query)
    return results    

def search_episode(episode):
    tipo = "serie" 
    imdb_id = episode.get("imdb_id") 
    name = episode.get("title")  
    season = episode.get("season")  
    episodio = episode.get("episode") 
    provider.log.info("cont: %s "  % episode)
    provider.log.info("name: " + name)
    provider.log.info("season: %s"  %season)
    provider.log.info("season: %s"  %episodio)
    temporada = season
    capt = episodio
    url_pelicula = "http://api.themoviedb.org/3/find/%s?api_key=57983e31fb435df4df77afb854740ea9&language=%s&external_source=imdb_id" % (imdb_id, IDIOMA)
    pelicula = urllib2.urlopen(url_pelicula)
    texto1 = json.loads(pelicula.read())
    texto2 = texto1['tv_results']
    texto3 = texto2[0]

    nombre = texto3.get("name")
    nombre_serie = nombre
    
    if nombre == "24" and season == 9 and IDIOMA == 'es':
                 nombre = u"24 vive otro dia"
                 name = u"24 live other day"
                 season = 1

    nombre = nombre.replace(u'á', "a")
    nombre = nombre.replace(u'é', "e")
    nombre = nombre.replace(u'í', "i")
    nombre = nombre.replace(u'ó', "o")
    nombre = nombre.replace(u'ú', "u")  
    
    temporada = "" 
    pag_bus = ""
    suf_idioma = ""
    
    
    if nombre.lower() <> name.lower():
        nombre2 = '"' + name + '"' + suf_idioma
        nombre = '("' + nombre + '" OR ' + nombre2 + ')' 
   
    else:    
        nombre = '"' + name + '"' + suf_idioma   
    nombre = nombre.replace(":", "")     

    capitulo = "%s%dX%02d%s%d%02d%s" % (" (",season, episodio, " OR ", season, episodio, " )")
 #   busqueda_completa =  nombre + capitulo + "/"
   #----Calidad ------------------------------------      
    if only_HD == "true": 
             calidad = '1469' 
    else: 
             calidad = 'All'
                           
            
  #----------------------------------------------------------   
    busqueda_completa =  nombre
    pagina_busqueda = __proxy__ + 'buscar-descargas/cID=0&tLang=0&oBy=0&oMode=0&category_=%s&subcategory_=All&idioma_=1&calidad_=All&oByAux=0&oModeAux=0&size_=0&q=' % (calidad)
    ttt = pagina_busqueda + busqueda_completa
    lectura_pagina(ttt, tipo, nombre, season, episodio, name, nombre_serie)
  #  resp = provider.GET(pagina_busqueda, params={"q": busqueda_completa.encode('utf-8'),})
  #  return provider.extract_magnets(resp.data)
 #   provider.log.info("Victor retorna: %s"  %results)      
    return results


def search_movie(movie):
    tipo = "peli"
  # Busqueda de titulo en idioma de audio ------------------------ 
    if IDIOMA <> 'en':
      inicio_proceso = time.time()
      imdb_id = movie.get("imdb_id")
      name = movie.get("title")
      url_pelicula = "http://api.themoviedb.org/3/find/%s?api_key=57983e31fb435df4df77afb854740ea9&language=%s&external_source=imdb_id" % (imdb_id, IDIOMA)

      pelicula = urllib2.urlopen(url_pelicula)
      texto1 = json.loads(pelicula.read())
      
      texto2 = texto1['movie_results']
      texto3 = texto2[0]
      nombre = texto3.get("title")
      nombre = nombre.replace(u'á', "a")
      nombre = nombre.replace(u'é', "e")
      nombre = nombre.replace(u'í', "i")
      nombre = nombre.replace(u'ó', "o")
      nombre = nombre.replace(u'ú', "u")
    else:
      nombre = name  
  # -------------------------------------------------------------

    nombre = '"' + nombre + '"/'
    calidad = 'all'
  #----Calidad ------------------------------------      
    if only_HD == "true": 
             calidad = '1027' 
    else: 
             calidad = 'All'
          
    if use_3D == "true":  
              calidad = '1599'                  
            
  #----------------------------------------------------------       
    nombre = nombre.replace(":", "") 
  
    
    pagina_busqueda = __proxy__ + 'buscar-descargas/'
    busqueda_completa = 'cID=0&tLang=0&oBy=0&oMode=0&category_=%s&subcategory_=All&idioma_=1&calidad_=All&oByAux=0&oModeAux=0&size_=0&q=%s' % (calidad, nombre)

    busqueda_completa = busqueda_completa.encode('utf-8')
    
    ttt = pagina_busqueda + busqueda_completa
    lectura_pagina(ttt, tipo, nombre, 0, 0, name, "")
#    provider.log.info("Victor retorna: %s"  %results)  
    return results
#    return provider.extract_magnets(resp.data)


        
def lectura_pagina(urltarget, tipo, nombre, season, episodio, name, nombre_serie):   
    urltarget = urltarget.replace(' ', "%20")   
    provider.log.info("Victor: " + urltarget)
    u = urllib2.urlopen(urltarget)
    try:
        resp = u.read()
 #       provider.log.info("Contenido pagina: " + resp)
    except urllib2.HTTPError as error_code:
            provider.log.error(' Victor error %s' % error_code, xbmc.LOGDEBUG)
    finally:
            u.close()
   
    #resp = provider.GET(pagina_busqueda, params={"q": busqueda_completa,})

    pmagnet = re.compile(r'magnet:\?[^\'"\s<>\[\]]+')
    ptorrent = re.compile(r'http[s]?://.*\.torrent')
    ptitulo = re.compile(r'title="*]"')

    sections = (resp.split("<td"))

 
  # a section (<td) could contain a magnet link, torrent or both
  # prioritize magnets
    for section in sections:
     magnet = pmagnet.search(section)
     if magnet == None:
       torrent = ptorrent.search(section)
       if torrent != None:
    #      provider.log.info("Contenido pagina: " + section) 
          if tipo == "serie":
             capitulo1 = "%dX%02d" % (season, episodio)     
             capitulo2 = "%d%02d" % (season, episodio) 
             capitulo3 = "S%02dE%02d" % (season, episodio) 
    #         provider.log.info("Contenido pagina: " + capitulo2)   
             if (capitulo1 in section) or (capitulo2 in section):
    #         if (section.find(capitulo2) < 0):
    #             provider.log.info("No encuentra: " + capitulo2)  
    #         if ( section.find(capitulo1) > 0) or (section.find(capitulo2) > 0):
                 if ( section.find("1080") > 0) :
                    prub1 = 3
                    prub2 = "1080p"
                 elif ( section.find("720") > 0) :  
                    prub1 = 2 
                    prub2 = "720p"
                 else :
                    prub1 = 1 
                    prub2 = "HDTV"   
                  
    #             provider.log.info("Contenido pagina: %s" %prub1)
                 results.append({"name": nombre_serie + " " + capitulo3 + " " + prub2 + "- Newpct Provaider" , "uri": torrent.group(0) , "resolution" : prub1})
    #             provider.log.info("Victor Found torrent: " + torrent.group(0))
          else:
    #         provider.log.info("tipo: " + tipo + nombre) 
             nombre = nombre
             nombre = nombre.replace('"', "")
             nombre = nombre.replace('/', "")
             ptitulo = re.compile(nombre, re.I)
             ptitulo2 = re.compile(name, re.I)
             titulo = ptitulo.search(section)
             titulo2 = ptitulo2.search(section)
             if (titulo != None) or (titulo2 != None): 
       #         provider.log.info("Detectado titulo: " + nombre)
                results.append({"uri": torrent.group(0)})
                provider.log.info("Found torrent: " + torrent.group(0))
         # provider.log.info("Found torrent: " + titulo)
     else:
          provider.log.info("Found magnet: " + magnet.group(0))
          results.append({"uri": magnet.group(0)})
      
  

# This registers your module for use
provider.register(search, search_movie, search_episode)
