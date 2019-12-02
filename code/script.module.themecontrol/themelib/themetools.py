# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

'''
2019/11/30: Work Started
'''

import os
import requests

import xbmcaddon
import themecontrol

addon = xbmcaddon.Addon()

def getDialogText(url):
    try:
        if url.startswith('http'):
            message = requests.get(url).content
        else:
            r = open(url)
            message = r.read()
            r.close()

        if message is None:
            return 'Nothing today! Blame Someone Else.'
        if '[link]' in message:
            tcolor = '[COLOR %s]' % (themecontrol.ThemeColors().link_color)
            message = message.replace('[link]', tcolor).replace('[/link]', '[/COLOR]')
        return message
    except Exception:
        return 'Nothing today! Blame Someone Else.'
