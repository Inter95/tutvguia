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
pag_esp = u' (castellano OR esp OR spanish OR newpct OR elitetorrent)'
pag_ita = u" +(ITA OR italian)"
pag_rus = " +rus"
pag_fra = " +french"
no_ITA = " -ITA"
screener = " -screener -CAM -Cam -camrip -TeleSync -TS -camlat"
sin_3d = " -3D"

alta_definicion = " (720 OR 1080 OR microhd)"

__addon__ = xbmcaddon.Addon(id="script.pulsar.kiasmulti")
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
    busqueda_completa = "%s" % query
    pagina_busqueda = __proxy__ + 'usearch/'
    resp = provider.GET(pagina_busqueda, params={"q": busqueda_completa.encode('utf-8'),})
    return provider.extract_magnets(resp.data)
        

def search_episode(episode):
    imdb_id = episode.get("imdb_id") 
    name = episode.get("title")  
    season = episode.get("season")  
    episodio = episode.get("episode") 
    url_pelicula = "http://api.themoviedb.org/3/find/%s?api_key=57983e31fb435df4df77afb854740ea9&language=%s&external_source=imdb_id" % (imdb_id, IDIOMA)
    pelicula = urllib2.urlopen(url_pelicula)
    texto1 = json.loads(pelicula.read())
    texto2 = texto1['tv_results']
    texto3 = texto2[0]

    nombre = texto3.get("name")
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
    if IDIOMA == 'es':
            suf_idioma = pag_esp
    elif IDIOMA == 'it':
            suf_idioma = pag_ita
    elif IDIOMA == 'ru':
            suf_idioma = pag_rus 
    elif IDIOMA == 'fr':
            suf_idioma = pag_fra 
    
    if nombre.lower() <> name.lower():
        nombre2 = '"' + name + '"' + suf_idioma
        nombre = '("' + nombre + '" OR ' + nombre2 + ')' 
   
    else:    
        nombre = '"' + name + '"' + suf_idioma   
    nombre = nombre.replace(":", " ")     

    capitulo = "%s%dX%02d%s%d%02d%s" % (" (",season, episodio, " OR ", season, episodio, " )")
    busqueda_completa =  nombre + capitulo + "/"
    pagina_busqueda = __proxy__ + 'usearch/'
    resp = provider.GET(pagina_busqueda, params={"q": busqueda_completa.encode('utf-8'),})
    return provider.extract_magnets(resp.data)
        



def search_movie(movie):
  
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
    var_1 = "%s" % name
    var_2 = "%s" % nombre
    suf_idioma = ""
 
      
    if IDIOMA == 'es':
            suf_idioma = pag_esp
    elif IDIOMA == 'it':
            suf_idioma = pag_ita
    elif IDIOMA == 'ru':
            suf_idioma = pag_rus 
    elif IDIOMA == 'fr':
            suf_idioma = pag_fra         
 
    nombre2 = '"' + name + '"' + suf_idioma 
    var_1 = var_1.lower()
    var_2 = var_2.lower()
    if var_1 == var_2:
        nombre = nombre2
    else:    
         nombre = '"' + nombre + '"'
  #----Calidad ------------------------------------      
    if only_HD == "true": 
             nombre = nombre + alta_definicion 
    else: 
        if use_screener == "true": 
          nombre = nombre + screener
          
    if use_3D == "false":      
         nombre = nombre + sin_3d    
  #----------------------------------------------------------       
    nombre = nombre.replace(":", " ") 
    
    pagina_busqueda = __proxy__ + 'usearch/'
    busqueda_completa =  nombre + u' category:movies'

    busqueda_completa = busqueda_completa.encode('utf-8')

    resp = provider.GET(pagina_busqueda, params={"q": busqueda_completa,})
    return provider.extract_magnets(resp.data)
        
   


# This registers your module for use
provider.register(search, search_movie, search_episode)
