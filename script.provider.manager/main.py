# coding: utf-8
import xbmcaddon
import xbmcgui
import xbmc
import os

# this read the settings
settings = xbmcaddon.Addon()
settings.openSettings()
language = settings.getSetting('language')
language1 = settings.getSetting('language1')
extra = settings.getSetting('extra')
time_noti = settings.getSetting('time_noti')
movie_min_size = settings.getSetting('movie_min_size')
movie_max_size = settings.getSetting('movie_max_size')
TV_min_size = settings.getSetting('TV_min_size')
TV_max_size = settings.getSetting('TV_max_size')
max_magnets = settings.getSetting('max_magnets')  # max_magnets
movie_key_allowed = settings.getSetting('movie_key_allowed')
movie_key_denied = settings.getSetting('movie_key_denied')
movie_qua1 = settings.getSetting('movie_qua1')  # 480p
movie_qua2 = settings.getSetting('movie_qua2')  # HDTV
movie_qua3 = settings.getSetting('movie_qua3')  # 720p
movie_qua4 = settings.getSetting('movie_qua4')  # 1080p
movie_qua5 = settings.getSetting('movie_qua5')  # 3D
movie_qua6 = settings.getSetting('movie_qua6')  # CAM
movie_qua7 = settings.getSetting('movie_qua7')  # TeleSync
TV_key_allowed = settings.getSetting('TV_key_allowed')
TV_key_denied = settings.getSetting('TV_key_denied')
TV_qua1 = settings.getSetting('TV_qua1')  # 480p
TV_qua2 = settings.getSetting('TV_qua2')  # HDTV
TV_qua3 = settings.getSetting('TV_qua3')  # 720p
TV_qua4 = settings.getSetting('TV_qua4')  # 1080p
# get providers Installed
path = xbmc.translatePath('special://home') + "addons/"
providers = os.listdir(path)
list_providers = ""
for provider in providers:
    try:
        if provider.endswith('-mc'):
            path = xbmc.translatePath('special://home') + "addons/" + provider
            if os.path.exists(path):
                list_providers += provider + '\n'
                print '[' + provider + ']: Settings were updated!'
                settings1 = xbmcaddon.Addon(provider)
                settings1.setSetting('language', language)
                settings1.setSetting('extra', extra)
                settings1.setSetting('time_noti', time_noti)
                settings1.setSetting('movie_min_size', movie_min_size)
                settings1.setSetting('movie_max_size', movie_max_size)
                settings1.setSetting('TV_min_size', TV_min_size)
                settings1.setSetting('TV_max_size', TV_max_size)
                settings1.setSetting('max_magnets', max_magnets)
                settings1.setSetting('movie_key_allowed', movie_key_allowed)
                settings1.setSetting('movie_key_denied', movie_key_denied)
                settings1.setSetting('movie_qua1', movie_qua1)
                settings1.setSetting('movie_qua2', movie_qua2)
                settings1.setSetting('movie_qua3', movie_qua3)
                settings1.setSetting('movie_qua4', movie_qua4)
                settings1.setSetting('movie_qua5', movie_qua5)
                settings1.setSetting('movie_qua6', movie_qua6)
                settings1.setSetting('movie_qua7', movie_qua7)
                settings1.setSetting('TV_key_allowed', TV_key_allowed)
                settings1.setSetting('TV_key_denied', TV_key_denied)
                settings1.setSetting('TV_qua1', TV_qua1)
                settings1.setSetting('TV_qua2', TV_qua2)
                settings1.setSetting('TV_qua3', TV_qua3)
                settings1.setSetting('TV_qua4', TV_qua4)
    except:
        continue
dialog = xbmcgui.Dialog()
dialog.ok('Changes are Done!!', list_providers + '         have been Updated!')