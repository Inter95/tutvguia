# coding: utf-8
__author__ = 'Ruben'
a = "http://www.yaske.cc/es/peliculas/genero/action"

b = "http://www.yaske.cc/es/peliculas/page/2/genero/action"

c = "http://www.yaske.cc/"

d = "http://www.yaske.cc/es/peliculas/page/2/"

import re
print b
print re.sub("[0-9]+", "%s", b)
