# -*- coding: UTF-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# Welcome to House Atreides.  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

import os
import sys
import urllib
import urlparse

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin


sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))
action = params.get('action')

def mainmenu():
        tIcon = xbmcaddon.Addon().getAddonInfo('icon')
        tFanart =  xbmcaddon.Addon().getAddonInfo('fanart')
        url = sysaddon + '?action=showOK'
        list_item = xbmcgui.ListItem('OK Dialog', iconImage=tIcon)
        list_item.setArt({'fanart': tFanart})
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=syshandle, url=url, listitem=list_item, isFolder=False)

        url = sysaddon + '?action=showProgress'
        list_item = xbmcgui.ListItem('Progress Dialog', iconImage=tIcon)
        list_item.setArt({'fanart': tFanart})
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=syshandle, url=url, listitem=list_item, isFolder=False)

        url = sysaddon + '?action=showYesNo'
        list_item = xbmcgui.ListItem('Yes/No Dialog', iconImage=tIcon)
        list_item.setArt({'fanart': tFanart})
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=syshandle, url=url, listitem=list_item, isFolder=False)

        url = sysaddon + '?action=showNInfo'
        list_item = xbmcgui.ListItem('Info Notification Popup (Focused)', iconImage=tIcon)
        list_item.setArt({'fanart': tFanart})
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=syshandle, url=url, listitem=list_item, isFolder=False)

        url = sysaddon + '?action=showNWarning'
        list_item = xbmcgui.ListItem('Warning Notification Popup (Focused)', iconImage=tIcon)
        list_item.setArt({'fanart': tFanart})
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=syshandle, url=url, listitem=list_item, isFolder=False)

        url = sysaddon + '?action=showNError'
        list_item = xbmcgui.ListItem('Error Notification Popup (Focused)', iconImage=tIcon)
        list_item.setArt({'fanart': tFanart})
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=syshandle, url=url, listitem=list_item, isFolder=False)

        url = sysaddon + '?action=showChanges'
        list_item = xbmcgui.ListItem('Changelog Viewer', iconImage=tIcon)
        list_item.setArt({'fanart': tFanart})
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=syshandle, url=url, listitem=list_item, isFolder=False)

        endDirectory()


def endDirectory():
    xbmcplugin.endOfDirectory(syshandle)


if action is None:
    mainmenu()
elif action == 'showOK':
    from dialogs import ok
    ok.OK_Dialog(title='Example OK Window', msg='Click the button to close the OK window')
elif action == 'showProgress':
    from dialogs import progress
    dialog = progress.Progress_Dialog()
    dialog.create('My Title', 'This is my message for it')
    xbmc.sleep(1000)
    dialog.update(0.0, 'Get It Started at 0.....')
    xbmc.sleep(1000)
    dialog.update(25.0, '25 percent')
    xbmc.sleep(1000)
    dialog.update(35.0, '35 percent')
    xbmc.sleep(1000)
    dialog.update(55.0, '55 percent')
    xbmc.sleep(1000)
    dialog.update(75.0, '75 percent')
    xbmc.sleep(1000)
    dialog.update(100.0, '100 percent')
elif action == 'showYesNo':
    from dialogs import yesno, ok
    ret = yesno.YN_Dialog(title='Example Yes/No Window', msg='Returns True for Yes, False for No')
    ok.OK_Dialog(title='Yes/No Return Value', msg='You clicked on %s' % (ret))
elif action == 'showNInfo':
    from dialogs import notification
    notification.infoDialog(title='Whatever', msg='The Message', style='INFO', timer=3000)
elif action == 'showNWarning':
    from dialogs import notification
    notification.infoDialog(title='Beware', msg='You been warned', style='WARNING', timer=3000)
elif action == 'showNError':
    from dialogs import notification
    notification.infoDialog(title='Fucked Up', msg='You did it now!', style='ERROR', timer=3000)
elif action == 'showChanges':
    from dialogs import changelog
    changelog.ChangelogViewer()
