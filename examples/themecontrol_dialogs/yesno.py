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

import themecontrol

addon = xbmcaddon.Addon()


'''
Example on how to call the Yes/No Dialog from within your addon
    from path.to.the.changelog.python.file import yesno
    yesno.YN_Dialog(title='My Yes/No Window', msg='Choose wisely')
'''
def YN_Dialog(title, msg, yestext='Yes', notext='No'):
    class YN_Box(xbmcgui.WindowXMLDialog):
        # until now we have a blank window, the onInit function will parse your xml file
        def onInit(self):
            self.colors = themecontrol.ThemeColors()

            # Title/Header Label's ID from the XML
            self.lbl_title = 1
            # Textbox control's ID from the XML for the "message"
            self.tbox_body = 2

            # Yes button control's ID from the XML
            self.btn_yes = 5
            # No button control's ID from the XML
            self.btn_no = 6

            self.getControl(self.lbl_title).setLabel(title)
            self.setProperty('dhtext', self.colors.dh_color)
            self.setProperty('btnfocus', self.colors.btn_focus)
            self.getControl(self.tbox_body).setText(msg)
            self.getControl(self.btn_yes).setLabel(yestext)
            self.getControl(self.btn_no).setLabel(notext)

            xbmc.sleep(100)
            # this puts the focus on the top item of the container
            self.setFocusId(self.getCurrentContainerId())
            self.setFocus(self.getControl(self.btn_no))
            xbmc.executebuiltin("Dialog.Close(busydialog)")

        def onClick(self, controlId):
            if (controlId == self.btn_no):
                self.close()
            if (controlId == self.btn_yes):
                self.close()

        def onAction(self, action):
            if action == themecontrol.ACTION_PREVIOUS_MENU or action == themecontrol.ACTION_NAV_BACK:
                self.close()

    '''
        Breakdown: OK_Box(xmlFilename, addon_path, theme_root_path, xml_path, <additional variables>)

        Note:
            The xml_path folder is where the xmls is located. You could technically have one for 720p, one for 1080i, etc. then in your
            dialog code check the Kodi resolution being used and load different xmls based on that.

            ** Using the folder name of 'xml' in Kodi 17 makes it look at the Skin for Kodi itself, ignoring the module.
    '''
    yn = YN_Box('Dialog_YesNo.xml', themecontrol.getThemeModulePath(), themecontrol.getCurrentTheme(), '1080i', title=title, msg=msg, yestext=yestext, notext=notext)
    yn.doModal()
    '''
    In the XML, we use the onclick entity to set the btnret property 'false' and 'true' based on no/yes buttons. That way, we can read them
    here after the button is pressed (and doModal() is completed). Properties should be read before you delete the object.

    You can make any button set any text value to a Property, then read it in the script to execute items based on the button. Then only reason it finishes the doModal()
    execution here, is because we have the onClick() function above closing it when either button is pressed.

    We do the "else" instead of seeing if the property is 'false' is because if they hit Previous, Back, etc. then it never gets set at all. So it is either
    true, false, or something else. Since our logic is 'true' or 'anything else', we keep it simple.
    '''
    ret = yn.getProperty('btnret')
    del yn
    if ret == 'true':
        return True
    else:
        return False
