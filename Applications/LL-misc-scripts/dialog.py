# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 21:36:57 2016

@author: laughreyl
"""

import wx, os
from win32api import GetSystemMetrics  # to get screen resolution

class mainFrame(wx.Frame):
    """
    Creates the main window of the application.
    """
    def __init__(self, *args, **kwds):

        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)


        wildcard = "pySolo Video config file (*.cfg)|*.cfg|" \
                   " All files (*.*)|*.*"    # don't add any spaces!
        dlg = wx.FileDialog(                    # make an open-file window
            self, message="Choose a configuration file.",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )
        print("before ShowModal")
        if dlg.ShowModal() == wx.ID_OK:         # show the open-file window
            configfile = dlg.GetPath()
#            options.New(path)
        dlg.Destroy()
        print("after ShowModal")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%         Main Program
screen_width = GetSystemMetrics(0)   # get the screen resolution of this monitor
screen_height = GetSystemMetrics(1) 

if __name__ == "__main__":
    configfile = "C:\\Users\\laughreyl\\Documents\\test.txt"

    app = wx.App()
    wx.InitAllImageHandlers()
    
    frame_1 = mainFrame(None, -1, "")           # Create the main window.
    app.SetTopWindow(frame_1)
    frame_1.Show()                              # Show the main window
    print("before MainLoop")
    app.MainLoop()                              # Begin user interactions.
    print("after MainLoop")
