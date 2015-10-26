# coding: utf-8
from tools import *
import xml.etree.ElementTree as ET

# this read the settings of add on
settings = Settings()
path = xbmc.translatePath('special://userdata')
if os.path.exists("%sfavourites.xml" % path):
    tree = ET.parse("%sfavourites.xml" % path)
    root = tree.getroot()

    # check movies
    titles = []
    ID = []
    for child in root:
        data = child.text
        if 'plugin://plugin.video.pulsar/movie/' in data:
            titles.append(child.attrib['name'])
            ID.append(re.search('plugin://plugin.video.pulsar/movie/(.*?)/', data).group(1))
    if len(titles) > 0:
        subscription(titles, ID,'MOVIE', settings.movieFolder, True, message='Single Movie List')

    # check movies sections
    titles = []
    ID = []
    for child in root:
        data = child.text.replace('"plugin://plugin.video.pulsar/movies/"', '')  # remove movies root
        if 'plugin://plugin.video.pulsar/movies/' in data:
            section = re.search('plugin://plugin.video.pulsar/movies/(.*?)"', data).group(1)
            # get the list of movies
            sleep(0.002)
            response = browser.get('http://localhost:65251/movies/%s' % section)
            data = response.json()
            for item in data['items']:
                if 'title' in item['info'] and item['info'].has_key('code'):
                    titles.append(item['info']['title'].encode('ascii', 'ignore') + ' (' + str(item['info']['year']) + ')')
                    ID.append(item['info']['code'])
    if len(titles) > 0:
        subscription(titles, ID,'MOVIE', settings.movieFolder, True, message='Pulsar Movies Section')

    # check tv shows
    titles = []
    ID = []
    for child in root:
        data = child.text
        name = child.attrib['name']
        if 'plugin://plugin.video.pulsar/show/' in data and 'Season ' not in name:
            titles.append(name)
            ID.append(re.search('plugin://plugin.video.pulsar/show/(.*?)/', data).group(1))
    if len(titles) > 0:
        subscription(titles, ID,'SHOW', settings.showFolder, True, message='Single TV Shows List')
else:
    settings.notification(settings.string(32158))

	
#clear memory
del settings