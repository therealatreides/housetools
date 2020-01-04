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
Work in Progress, NOT USABLE RIGHT NOW
I am porting the one from Atreides and Marauder over to this system so will
take just a little time (since my time is limited).
'''

import os
import re

import xbmc
import xbmcgui
import xbmcaddon

import themecontrol

LOG_PATH = xbmc.translatePath('special://logpath/')
addon = xbmcaddon.Addon()


'''
Example on how to call the Kodi Log Viewer Dialog from within your addon
    from path.to.the.changelog.python.file import logviewer
    logviewer.LogViewer(logfile=None)
'''
def LogViewer(logfile=None):
    class LogViewver_Window(xbmcgui.WindowXMLDialog):
        # until now we have a blank window, the onInit function will parse your xml file
        def onInit(self):
            self.colors = themecontrol.ThemeColors()

            # Title/Header Label's ID from the XML
            self.lbl_title = 101
            # ID for the text control that will display the logfile contents
            self.txtbox_log = 102
            self.scrollbar = 103
            self.btn_upload = 201
            self.btn_kodi = 202
            self.btn_kodiold = 203
            self.btn_ok = 205

            self.logfile = os.path.join(log_utils.LOGPATH, logfile)

            self.logmsg = log_utils.readLog(self.logfile)
            self.lbl_titlemsg = "%s: %s" % (control.addonName(), logfile)
            self.showdialog()

        def showdialog(self):
            self.setProperty('dhtext', self.colors.dh_color)
            self.getControl(self.lbl_title).setLabel(self.lbl_titlemsg)
            self.getControl(self.txtbox_log).setText(log_utils.highlightText(self.logmsg))
            self.setFocusId(self.scrollbar)

        def onClick(self, controlId):
            if controlId == self.btn_ok:
                self.close()
            elif controlId == self.btn_upload:
                self.close()
                upload_check = log_utils.uploadLog(self.logmsg)
                if upload_check[0]:
                    data = 'Post this url or scan QRcode for your log, together with a problem description, in the Bug Report tool: %s' % (upload_check[1])
                    log_utils.showResult(data, upload_check[1])
            elif controlId == self.btn_kodi:
                filename = 'kodi.log'
                self.logfile = os.path.join(log_utils.LOGPATH, filename)
                self.logmsg = log_utils.readLog(self.logfile)

                if len(self.logmsg) < 10:
                    self.lbl_titlemsg = "%s: View Log Error" % control.addonName()
                    self.getControl(self.txtbox_log).setText("Log File Does Not Exists Or Is Too Large!")
                else:
                    self.lbl_titlemsg = "%s: %s" % (control.addonName(), filename.replace(log_utils.LOGPATH, ''))
                    self.getControl(self.lbl_title).setLabel(self.lbl_titlemsg)
                    self.getControl(self.txtbox_log).setText(log_utils.highlightText(self.logmsg))
                    self.setFocusId(self.scrollbar)
            elif controlId == self.btn_kodiold:
                filename = 'kodi.old.log'
                self.logfile = os.path.join(log_utils.LOGPATH, filename)
                self.logmsg = log_utils.readLog(self.logfile)

                if len(self.logmsg) < 10:
                    self.lbl_titlemsg = "%s: View Log Error" % control.addonName()
                    self.getControl(self.txtbox_log).setText("Log File Does Not Exists!")
                else:
                    self.lbl_titlemsg = "%s: %s" % (control.addonName(), filename.replace(log_utils.LOGPATH, ''))
                    self.getControl(self.lbl_title).setLabel(self.lbl_titlemsg)
                    self.getControl(self.txtbox_log).setText(log_utils.highlightText(self.logmsg))
                    self.setFocusId(self.scrollbar)

        def onAction(self, action):
            if action == themecontrol.ACTION_PREVIOUS_MENU or action == themecontrol.ACTION_NAV_BACK:
                self.close()


    viewer = LogViewver_Window('LogViewer.xml', themecontrol.getThemeModulePath(), themecontrol.getCurrentTheme(), '1080i', logfile=logfile)
    viewer.doModal()
    del viewer
