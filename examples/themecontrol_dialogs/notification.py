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
To-Do: Need to split part of the init into a function and call it withing the infoDialog() after
       creating the modal. This is so it doesn't "halt" the addon while the timer elapses. Maybe?
'''

import os
import re

import xbmc
import xbmcgui
import xbmcaddon

from themelib import themecontrol, tools

addon = xbmcaddon.Addon()


def infoDialog(title='', msg='', style='INFO', timer=3000):
    class Notify_Box(xbmcgui.WindowXMLDialog):
        # until now we have a blank window, the onInit function will parse your xml file
        def onInit(self):
            self.colors = themecontrol.ThemeColors()
            self.sounds = themecontrol.ThemeSounds()

            # This is where we use style variable to decide which sound clip to use later.
            notifyAudio = self.sounds.notifyinfo
            if style == 'INFO':
                notifyAudio = self.sounds.notifyinfo
            elif style == 'WARNING':
                notifyAudio = self.sounds.notifywarning
            elif style == 'ERROR':
                notifyAudio = self.sounds.notifyerror

            '''
            Save the IDs used for the title and textbox controls in the XML
            We do the ID instead of the getControl() reference so we can use the
            IDs for more than just getControl(). Such as when checking onClick()
            since it passes the ID only and not the object reference.
            '''
            self.title = 401
            self.msg = 402

            # Get the control reference for the Title/Header Label and set it's text/label
            self.getControl(self.title).setLabel(title)
            # Here we set the property for the header color so that the control can use it
            # in the XML
            self.setProperty('dhtext', self.colors.dh_color)
            # Get the control reference for the Label used for the message. I used a label
            # for this control because it would allow for a nicer scroll.
            self.getControl(self.msg).setLabel(msg)
            # Here we set the property for the message color so that the control can use it
            # in the XML
            self.setProperty('dttext', self.colors.dt_color)

            # This will play the sound, without the Player controls popping up, in the background
            xbmc.playSFX(notifyAudio)
            # slight sleep cuz we can
            xbmc.sleep(100)
            # this puts the focus on the top item of the container
            self.setFocusId(self.getCurrentContainerId())
            # Kill any busy dialog if it popped up
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            # sleep for the duration of the timer that passed
            xbmc.sleep(timer)
            # Auto close the dialog once time elapses
            self.close()

        def onClick(self, controlId):
            pass

        def onAction(self, action):
            pass

    '''
        Breakdown: Changelog_Window(xmlFilename, addon_path, theme_root_path, xml_path, <additional variables>)

        Note:
            The xml_path folder is where the xmls is located. You could technically have one for 720p, one for 1080i, etc. then in your
            dialog code check the Kodi resolution being used and load different xmls based on that.
    '''
    ok = Notify_Box('Dialog_Notification.xml', themecontrol.getThemeModulePath(), themecontrol.getThemeRootPath(), 'xml', title=title, msg=msg, style=style, timer=timer)
    ok.doModal()
    del ok