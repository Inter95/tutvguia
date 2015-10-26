# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2014 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os,datetime,xbmc,xbmcaddon

class main:
    def __init__(self):
        while (not xbmc.abortRequested):

            if xbmcaddon.Addon().getSetting("service_update") == 'true':
                try:
                    t1 = datetime.datetime.strptime(xbmcaddon.Addon().getSetting("service_run"), "%Y-%m-%d %H:%M:%S.%f")
                    t2 = datetime.datetime.now()
                    hoursList = [2, 5, 10, 15, 24]
                    interval = int(xbmcaddon.Addon().getSetting("service_interval"))
                    update = abs(t2 - t1) > datetime.timedelta(hours=hoursList[interval])
                    if update == False: raise Exception()
                    if not (xbmc.Player().isPlaying() or xbmc.getCondVisibility('Library.IsScanningVideo')):
                        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.genesis/?action=library_service)')
                except:
                    pass

            if not (xbmcaddon.Addon().getSetting("trakt_user") == '' or xbmcaddon.Addon().getSetting("trakt_password") == ''):
                try:
                    t1 = datetime.datetime.strptime(xbmcaddon.Addon().getSetting("service_trakt"), "%Y-%m-%d %H:%M:%S.%f")
                    t2 = datetime.datetime.now()
                    update = abs(t2 - t1) > datetime.timedelta(hours=4)
                    if update == False: raise Exception()
                    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.genesis/?action=indicator_service)')
                    xbmc.sleep(10000)
                except:
                    pass
                try:
                    t1 = datetime.datetime.strptime(xbmcaddon.Addon().getSetting("service_trakt_tv"), "%Y-%m-%d %H:%M:%S.%f")
                    t2 = datetime.datetime.now()
                    update = abs(t2 - t1) > datetime.timedelta(hours=4)
                    if update == False: raise Exception()
                    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.genesis/?action=indicator_service)')
                    xbmc.sleep(10000)
                except:
                    pass

            xbmc.sleep(1000)

main()