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
2019/12/24: Cleanup
'''

import os
import xml.etree.ElementTree as ET

import xbmcaddon

ACTION_PREVIOUS_MENU = 10  # ESC action
ACTION_NAV_BACK = 92  # Backspace action
ACTION_MOVE_LEFT = 1  # Left arrow key
ACTION_MOVE_RIGHT = 2  # Right arrow key
ACTION_MOVE_UP = 3  # Up arrow key
ACTION_MOVE_DOWN = 4  # Down arrow key
ACTION_MOUSE_WHEEL_UP = 104  # Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN = 105  # Mouse wheel down
ACTION_MOVE_MOUSE = 107  # Down arrow key
ACTION_SELECT_ITEM = 7  # Number Pad Enter
ACTION_BACKSPACE = 110  # ?
ACTION_MOUSE_LEFT_CLICK = 100
ACTION_MOUSE_LONG_CLICK = 108

MENU_ACTIONS = [ACTION_MOVE_UP, ACTION_MOVE_DOWN, ACTION_MOUSE_WHEEL_UP, ACTION_MOUSE_WHEEL_DOWN, ACTION_MOVE_MOUSE]

addon = xbmcaddon.Addon()

class ThemeColors():
    def __init__(self):
        self.colorsPath = getThemeColorPath()
        self.colors()

    def colors(self):
        tree = ET.parse(os.path.join(self.colorsPath, 'colors.xml'))
        root = tree.getroot()
        for item in root.findall('color'):
            self.dh_color = item.find('dialogheader').text
            self.dt_color = item.find('dialogtext').text
            self.mh_color = item.find('menuheader').text
            self.mt_color = item.find('menutext').text
            self.link_color = item.find('link').text
            self.focus_textcolor = item.find('focustext').text
            self.btn_focus = item.find('focusbutton').text


class ThemeSounds():
    def __init__(self):
        self.soundPath = getThemeSoundPath()
        self.sounds()

    def sounds(self):
        if addon.getSetting('notifyvoice') == 'true':
            sound_root = 'voice_'
        else:
            sound_root = 'system_'

        tree = ET.parse(os.path.join(self.soundPath, 'sounds.xml'))
        root = tree.getroot()

        for item in root.findall(sound_root + 'actions'):
            self.select = os.path.join(self.soundPath, item.find('select').text)
            self.parentdir = os.path.join(self.soundPath, item.find('parentdir').text)
            self.previusmenu = os.path.join(self.soundPath, item.find('previusmenu').text)
            self.screenshot = os.path.join(self.soundPath, item.find('screenshot').text)
        for item in root.findall(sound_root + 'windows'):
            self.notifyerror = os.path.join(self.soundPath, item.find('notifyerror').text)
            self.notifyinfo = os.path.join(self.soundPath, item.find('notifyinfo').text)
            self.notifywarning = os.path.join(self.soundPath, item.find('notifywarning').text)


def getCurrentTheme():
    theme = addon.getSetting('theme.control').lower()
    if theme in ['-', '']:
        return
    else:
        return theme


def getThemeModulePath():
    return addon.getAddonInfo('path')


def getThemeRootPath():
    theme = getCurrentTheme()
    if theme in ['-', '']:
        return
    else:
        return os.path.join(addon.getAddonInfo('path'), 'resources', 'skins', theme)


def getThemeXMLPath():
    theme = getCurrentTheme()
    if theme in ['-', '']:
        return
    else:
        return os.path.join(addon.getAddonInfo('path'), 'resources', 'skins', theme, 'xml')


def getThemeArtworkPath():
    theme = getCurrentTheme()
    if theme in ['-', '']:
        return
    else:
        return os.path.join(addon.getAddonInfo('path'), 'resources', 'skins', theme, 'media')


def getThemeColorPath():
    theme = getCurrentTheme()
    if theme in ['-', '']:
        return
    else:
        return os.path.join(addon.getAddonInfo('path'), 'resources', 'skins', theme, 'colors')


def getThemeSoundPath():
    theme = getCurrentTheme()
    if theme in ['-', '']:
        return
    else:
        return os.path.join(addon.getAddonInfo('path'), 'resources', 'skins', theme, 'sounds')
