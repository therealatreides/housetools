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
This one is NOT USABLE right now. Need to wrap it into a thread and make all
the create, update, close, etc. functions needed to interact with it so that
other code can run along side it like core
'''

import os
import re

import themecontrol
import xbmc
import xbmcaddon
import xbmcgui

try:
    from threading import Thread
except ImportError:
    from dummy_threading import Thread


addon = xbmcaddon.Addon()


'''
Example on how to call the Progress Dialog from within your addon
    from path.to.the.progress.python.file import progress
    dialog = progress.Progress_Dialog()
    dialog.create('My Title', 'This is my message for it')

Note** This is still a Work in Progress. Not suitable for use, as progress not
    increasing as of yet. Something I am overlooking or too dumb to see.
'''
class Progress_Dialog():
    def close(self):
        self.progress.close()

    def create(self, title, msg):
        self.progress = Progress_Box('Dialog_Progress.xml', themecontrol.getThemeModulePath(), themecontrol.getCurrentTheme(), '1080i')
        self.progress.show()
        self.progress.create(title, msg)

    '''
    This is used to see if the dialog is closed
    '''
    def iscancelled(self):
        ret = self.progress.getProperty('btnret')
        if ret == 'true':
            return True
        else:
            return False

    def update(self, percentage, msg=None):
        self.progress.update(percentage, msg)

'''
Due to the XML Interaction for skins using onInit and outter functions not being
able to access self.attributes like onClick() and other internal XML Window functions
we need to set up globals within the class to handle this. Dirty dirty little duck
'''
class Progress_Box(xbmcgui.WindowXMLDialog):
    colors = themecontrol.ThemeColors()
    lbl_title = 1
    tbox_body = 2
    btn_cancel = 5
    cntrl_progress = 11

    # until now we have a blank window, the onInit function will parse your xml file
    def onInit(self):
        xbmc.sleep(100)

    def create(self, title='Progress', msg=''):
        # Example XML uses properties for the color of text, so we add it now
        self.setProperty('dhtext', self.colors.dh_color)
        # We add another Property that the XML uses for adjusting the Button on focus
        self.setProperty('btnfocus', self.colors.btn_focus)
        # Initial progress is 0.
        self.setProperty('progress', '1')
        # Set the Title Label's text
        self.getControl(self.lbl_title).setLabel(title)
        # Set the Text for the Textbox next
        self.getControl(self.tbox_body).setText(msg)
        # this puts the focus on the top item of the container
        self.setFocusId(self.getCurrentContainerId())
        self.setFocus(self.getControl(self.btn_cancel))
        # Kill any busy dialog that may be open and we are done
        xbmc.executebuiltin("Dialog.Close(busydialog)")

    def update(self, percentage, msg):
        # Set the Percentage passed
        # We use the width it should be when full width and use division to set it
        # based on the percentage passed.
        # Passed / 100 * Width
        perc = int(percentage / 100 * 890)
        if perc == 0:
            perc = 1
        self.getControl(self.cntrl_progress).setWidth(perc)
        # Set the Text for the Textbox next
        if not msg is None:
            self.getControl(self.tbox_body).setText(msg)

    def onClick(self, controlId):
        # If the control clicked is the Cancel Button, close out the window and handle the cancel
        if (controlId == self.btn_cancel):
            self.close()

    def onAction(self, action):
        # Actions checked here are the previous menu and navigation back in order to close the
        # window from Back buttons, escape, etc.
        if action == themecontrol.ACTION_PREVIOUS_MENU or action == themecontrol.ACTION_NAV_BACK:
            self.close()
