# coding: utf-8
import xbmc
import xbmcgui
import bencode

dialog = xbmcgui.Dialog()
file = dialog.browse(1, 'Torrent2Pulsar', 'files')
#convert the torrent to magnet  take from http://stackoverflow.com/questions/12479570/given-a-torrent-file-how-do-i-generate-a-magnet-link-in-python
torrent = open(file, 'rb').read()
metadata = bencode.bdecode(torrent)
hashcontents = bencode.bencode(metadata['info'])
import hashlib
digest = hashlib.sha1(hashcontents).digest()
import base64
b32hash = base64.b32encode(digest)
magneturi = 'magnet:?xt=urn:btih:' + b32hash
xbmc.executebuiltin( "PlayMedia(plugin://plugin.video.pulsar/play?uri=%s)" % magneturi)