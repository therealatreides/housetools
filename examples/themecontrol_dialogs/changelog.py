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

import xbmcgui
import xbmcaddon

from themelib import themecontrol, tools

addon = xbmcaddon.Addon()

'''
Example on how to call the changelog window from within your addon
    from path.to.the.changelog.python.file import changelog
    changelog.ChangelogViewer()
'''
def ChangelogViewer(cl_text=None):
    class Changelog_Window(xbmcgui.WindowXMLDialog):
        def onInit(self):
            self.colors = themecontrol.ThemeColors()

            # changelog text from the file or remote url
            self.cl_text = cl_text

            # Textbox control's ID from the XML
            self.textbox_cl = 102
            # Close button control's ID from the XML
            self.btn_close = 202

            self.showdialog()

        def showdialog(self):
            # We can't pass variables to an Addon's Skin so we set properties that we read in the XML
            self.setProperty('dhtext', self.colors.dh_color)
            # This will set the text to display in the Textbox Control
            self.getControl(self.textbox_cl).setText(self.cl_text)
            # Adjust focus to the close button in the window displayed
            self.setFocusId(self.btn_close)

        def onClick(self, controlId):
            if controlId == self.btn_close:
                self.close()

        def onAction(self, action):
            if action == themecontrol.ACTION_PREVIOUS_MENU or action == themecontrol.ACTION_NAV_BACK:
                self.close()

    cl_text = tools.getDialogText(os.path.join(addon.getAddonInfo('path'), 'changelog.txt'))
    '''
        Breakdown: Changelog_Window(xmlFilename, addon_path, theme_root_path, xml_path, <additional variables>)

        Note:
            The xml_path folder is where the xmls is located. You could technically have one for 720p, one for 1080i, etc. then in your
            dialog code check the Kodi resolution being used and load different xmls based on that.
    '''
    viewer = Changelog_Window('Changelog.xml', themecontrol.getThemeModulePath(), themecontrol.getThemeRootPath(), 'xml', cl_text=cl_text)
    viewer.doModal()
    del viewer
