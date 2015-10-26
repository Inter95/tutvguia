# coding: utf-8
import os
import shutil
import xbmcgui
# copying yaske.py

try:
    kodiPath = xbmc.translatePath('special://home')

    path1 = os.path.join(kodiPath, "addons", "script.tvguia.mod", "files", "yaske.py")
    path2 = os.path.join(kodiPath, "addons", "plugin.video.pelisalacarta", "channels")
    shutil.copy(path1, path2)

    # copying xmb
    path1 = os.path.join(kodiPath, "addons", "script.tvguia.mod", "files", "xbmctools.py")
    path2 = os.path.join(kodiPath, "addons", "plugin.video.pelisalacarta", "platformcode")
    shutil.copy(path1, path2)

    # conclusion
    xbmcgui.Dialog().ok("TvGuia Mod", "Configuración terminada, disfruta tu tvguia")
except:
    xbmcgui.Dialog().ok("TvGuia Mod", "Error, configuración incompleta")
