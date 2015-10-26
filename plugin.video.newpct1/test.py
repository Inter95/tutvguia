# coding: utf-8
__author__ = 'Ruben'

import requests

# url = "http://www.newpct1.com/index.php?page=categorias&url=estrenos-de-cine&letter=&pg="
# browser = requests.Session()
# page = "1"
# import bs4
#
# response = browser.get( url + page)
#
# soup = bs4.BeautifulSoup(response.text)
# links = soup.select("ul.pelilist li")
# for link in links:
#     print link.a.get("href", ""), link.h2.text
#     url = link.a["href"].replace("/pelicula/", "/descarga-torrent/pelicula/")
#     print url
#     print "*****"
#     break

url = "http://www.newpct1.com/pelicula/del-reves-(inside-out)/"
pos = url.find('/', len('http://www.newpct1.com'))
print url[pos:]
##descarga-torrent
# browser = requests.Session()
# import bs4
#
# response = browser.get( url)
#
# soup = bs4.BeautifulSoup(response.text)
# links = soup.select("div#tab1 a.btn-torrent")
# print links[0].get("href", "")




# import re
#
# datos = re.search("var datos =(.*?);", data, re.DOTALL).group(1).replace("{", "").replace("}", "")
# params = {}
# for item in datos.split("\n"):
#     if item.strip() != "":
#         key, value = item.strip()[:-1].split(':')
#         params[key] = value.replace("'", "")
# #settings.debug(params)
# opciones = re.search("var options =(.*?);", data, re.DOTALL).group(1).replace("{", "").replace("}", "") + ": ''"
# params1 = {}
# for item in opciones.split("\n"):
#     if item.strip() != "":
#         key, value = item.strip()[:-1].split(':')
#         params1[key] = value.replace("'", "")
# #settings.debug(params1)
# urlPage = re.search('url: "(.*?)"', data).group(1)
