# -*- coding: utf-8 -*-
import urllib2
import urllib
import time
import re
import json
import xbmcaddon
import os
from pulsar import provider
# Leia-me
# - Modifique o arquivo resources\data.json para adicionar novos animes,
# se der certo me avise para atualizar o repositório ou se souber como crie um pull request.
# - Só vai funcionar com trackers abertos
# - Instruções sobre o arquivo resources\data.json:
#
# desc: Descrição da entrada.
# tvdb_id: Código do anime (vide http://thetvdb.com/).
# search_string: String usada para busca, onde %EPISODE% será substituído pelo número do episódio.
# tracker_engine: Valores aceitos atualmente -> 'generic' ou 'btdigg_api'.
# base_url: Parte da URL que fica antes da "String de Busca".\
#
# Atenção não se esqueça da virgula no final, das aspas e chaves.
# A tracker_engine "generic" só funciona com pesquisas que retornem o link magnético direto.
inicio = time.time()
PREFIX_LOG = 'ANIMESBR - '
__addon__ = xbmcaddon.Addon()
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
provider.log.info(open(os.path.join(addon_dir, 'resources', 'data.json')))
animes_array = json.loads(open(os.path.join(addon_dir, 'resources', 'data.json'),'r').read())["animes"]
provider.log.info("Conteúdo do data.json:" + str(animes_array))

def search(query):
    return []

def search_movie(movie):
    return []

def search_episode(ep):
    title = ep['title']
    absolute_number = ep['absolute_number']
    tvdb_id = ep['tvdb_id']
    provider.log.info(PREFIX_LOG + 'Procurando por: ' + title + ' ' + str(absolute_number))
    result = []
    tracker_engine = ''
    base_url = ''
    search_string = ''    
    for anime in animes_array:
        if int(anime["tvdb_id"]) == tvdb_id:
            search_string = re.sub(' ', '+',re.sub('%EPISODE%', str(absolute_number),anime["search_string"]))
            tracker_engine = anime["tracker_engine"]
            base_url = anime["base_url"]
            provider.log.info(PREFIX_LOG + 'String de busca: ' + search_string)
            break
    if ((tracker_engine != '') and (base_url != '') and (search_string != '')):
        result = search_anime(tracker_engine, base_url, search_string)
    provider.log.info(PREFIX_LOG + 'Result:' + str(result))
    return result
    
def search_anime(tracker_engine, base_url, search_string):
    if tracker_engine == 'btdigg_api':
        return search_btdigg(base_url, search_string)
    else:
        return search_generic(base_url, search_string)
        
def search_btdigg(base_url, search_string):
    result = []
    u = urllib2.urlopen(base_url + search_string)
    try:
       for line in u:
        if line.startswith('#'):
            continue
        info_hash, name, files, size, dl, seen = line.strip().split('\t')[:6]
        res = dict(uri = 'magnet:?xt=urn:btih:%s' % (info_hash,) + '&amp;dn=' + '%s' % name.translate(None, '|') ) 
        if(files == '1'):
            result.append(res)
    except urllib2.HTTPError as error_code:
        provider.log.error(PREFIX_LOG + ' error %s' % error_code, xbmc.LOGDEBUG)
    finally:
        u.close()
    return result
    
def search_generic(base_url, search_string):
    data = urllib2.urlopen(base_url + search_string)
    return provider.extract_magnets(data.read())

provider.log.info(PREFIX_LOG + 'Time: ' + str((time.time() - inicio)))
provider.register(search, search_movie, search_episode)
