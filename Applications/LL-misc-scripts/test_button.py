# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 21:36:57 2016

@author: laughreyl
"""

import wx, os
from win32api import GetSystemMetrics  # to get screen resolution
from wx.lib.filebrowsebutton import FileBrowseButton, DirBrowseButton

class mainFrame(wx.Frame):
    """
    Creates the main window of the application.
    """
    def __init__(self, *args, **kwds):

        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        self.pickMaskBrowser = FileBrowseButton(self, -1, labelText='Mask File')

#    def onBrowse(self, *args, **kwds):
#        configfile = "c:\Users\laughreyl\Documents\DAM_Analysis\Output\myconfig.cfg"
#        print(configfile)                                                           # debug
#        if ~os.path.isfile(configfile + ".cfg"):
#            wildcard = "pySolo Video config file (*.cfg)|*.cfg|" \
#                       " All files (*.*)|*.*"    # don't add any spaces!
#            dlg = wx.FileDialog(                    # make an open-file window
#                self, message="Choose a configuration file.",
#                defaultDir=os.getcwd(),
#                defaultFile="",
#                wildcard=wildcard,
#                style=wx.OPEN | wx.CHANGE_DIR
#                )
#    
#            if dlg.ShowModal() == wx.ID_OK:         # show the open-file window
#                configfile = dlg.GetPath()
#                options.New(path)
#            print(configfile)
#            dlg.Destroy()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%         Main Program
screen_width = GetSystemMetrics(0)   # get the screen resolution of this monitor
screen_height = GetSystemMetrics(1) 

if __name__ == "__main__":

    app = wx.App()
    wx.InitAllImageHandlers()
    
    frame_1 = mainFrame(None, -1, "")           # Create the main window.
    app.SetTopWindow(frame_1)
    frame_1.Show()                              # Show the main window
    app.MainLoop()                              # Begin user interactions.
