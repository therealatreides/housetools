# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################


import os
import re

import xbmc
import xbmcgui
import xbmcaddon

from themelib import themecontrol

addon = xbmcaddon.Addon()


'''
Example on how to call the OK Dialog from within your addon
    from path.to.the.changelog.python.file import ok
    ok.OK_Dialog(title='My OK Window', msg='Click the button to close the OK window')
'''
def OK_Dialog(title, msg):
    class OK_Box(xbmcgui.WindowXMLDialog):
        # until now we have a blank window, the onInit function will parse your xml file
        def onInit(self):
            self.colors = themecontrol.ThemeColors()

            # Title/Header Label's ID from the XML
            self.lbl_title = 1
            # Textbox control's ID from the XML for the "message"
            self.tbox_body = 2
            # Ok button control's ID from the XML
            self.btn_ok = 5

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
            self.setFocus(self.getControl(self.btn_ok))
            # Kill any busy dialog that may be open and we are done
            xbmc.executebuiltin("Dialog.Close(busydialog)")

        def onClick(self, controlId):
            # If the control clicked is the OK Button, close out the window
            if (controlId == self.btn_ok):
                self.close()

        def onAction(self, action):
            # Actions checked here are the previous menu and navigation back in order to close the
            # window from Back buttons, escape, etc.
            if action == themecontrol.ACTION_PREVIOUS_MENU or action == themecontrol.ACTION_NAV_BACK:
                self.close()

    '''
        Breakdown: OK_Box(xmlFilename, addon_path, theme_root_path, xml_path, <additional variables>)

        Note:
            The xml_path folder is where the xmls is located. You could technically have one for 720p, one for 1080i, etc. then in your
            dialog code check the Kodi resolution being used and load different xmls based on that.

            ** Using the folder name of 'xml' in Kodi 17 makes it look at the Skin for Kodi itself, ignoring the module.
    '''
    ok = OK_Box('Dialog_OK.xml', themecontrol.getThemeModulePath(), themecontrol.getCurrentTheme(), '1080i', title=title, msg=msg)
    ok.doModal()
    del ok