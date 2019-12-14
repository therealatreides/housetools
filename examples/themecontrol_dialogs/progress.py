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
try:
    from threading import Thread
except ImportError:
    from dummy_threading import Thread

import xbmc
import xbmcgui
import xbmcaddon

import themecontrol

addon = xbmcaddon.Addon()


'''
Example on how to call the Progress Dialog from within your addon
    from path.to.the.changelog.python.file import progress
    progress.Progress_Dialog(title='My Progress Window', msg='Click the button to close the OK window')

Note** You will want to run progress windows in threads so that the script can continue to run after calling it.
    Calling progress updates will work as normal if the progress control is in the window.
'''
class Progress_Dialog():
    def __init__(self):
        pass

    def create(self, title, msg):
        self.cprog = self.Progress_Box('Dialog_Progress.xml', themecontrol.getThemeModulePath(), themecontrol.getCurrentTheme(), '1080i', title=title, msg=msg)
        self.cprog.doModal()
        ret = self.cprog.getProperty('btnret')
        del self.cprog
        '''
        In the XML, we use the onclick entity to set the btnret property 'true' so we can know if Cancel was pressed.

        We do this, so scripts can handle specific checks based on if the dialog was cancelled or allowed to complete.
        '''
        if ret == 'true':
            return False
        else:
            return True

    class Progress_Box(xbmcgui.WindowXMLDialog):
        # until now we have a blank window, the onInit function will parse your xml file
        def onInit(self):
            self.colors = themecontrol.ThemeColors()

            # Title/Header Label's ID from the XML
            self.lbl_title = 1
            # Textbox control's ID from the XML for the "message"
            self.tbox_body = 2
            # Cancel button control's ID from the XML
            self.btn_cancel = 5

            # Set the Title Label's text
            self.getControl(self.lbl_title).setLabel(title)
            # Set the Text for the Textbox next
            self.getControl(self.tbox_body).setText(msg)
            # Example XML uses properties for the color of text, so we add it now
            self.setProperty('dhtext', self.colors.dh_color)
            # We add another Property that the XML uses for adjusting the Button on focus
            self.setProperty('btnfocus', self.colors.btn_focus)

            xbmc.sleep(100)
            # this puts the focus on the top item of the container
            self.setFocusId(self.getCurrentContainerId())
            self.setFocus(self.getControl(self.btn_cancel))
            # Kill any busy dialog that may be open and we are done
            xbmc.executebuiltin("Dialog.Close(busydialog)")

        def onClick(self, controlId):
            # If the control clicked is the Cancel Button, close out the window and handle the cancel
            if (controlId == self.btn_cancel):
                self.close()

        def onAction(self, action):
            # Actions checked here are the previous menu and navigation back in order to close the
            # window from Back buttons, escape, etc.
            if action == themecontrol.ACTION_PREVIOUS_MENU or action == themecontrol.ACTION_NAV_BACK:
                self.close()


'''
Class borrowed from Jen core. All credit to original developer
'''
class threadWithReturn(Thread):
    def __init__(self, *args, **kwargs):
        super(threadWithReturn, self).__init__(*args, **kwargs)

        self._return = None

    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args,
                                                **self._Thread__kwargs)

    def join(self, *args, **kwargs):
        super(threadWithReturn, self).join(*args, **kwargs)

        return self._return

