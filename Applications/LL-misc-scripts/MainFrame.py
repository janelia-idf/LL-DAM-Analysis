# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 21:36:57 2016

@author: laughreyl
"""

import numpy as np
import cv2
import wx, os
import datetime, time
from win32api import GetSystemMetrics  # to get screen resolution

class mainFrame(wx.Frame):
    """
    Creates the main window of the application.
    """
    def __init__(self, *args, **kwds):

        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   CODE TO BE USED IN FRAME        

        self.monitor1 = 'C:\\Users\\laughreyl\\Documents\\DAM_Analysis\\Data\\__20160823-135217__\\bias_video_cam_0_date_2016_08_23_time_13_52_17_v001.avi'


        dateindex = self.monitor1.find("date_")
        date = monitor1[dateindex+5:dateindex+15]
        print(date)
        
        timeindex = self.monitor1.find("time_")
        date = monitor1[timeindex+5:timeindex+14]
        print(time)
        




                

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   MAIN PROGRAM
screen_width = GetSystemMetrics(0)   # get the screen resolution of this monitor
screen_height = GetSystemMetrics(1) 

if __name__ == "__main__":

    app = wx.App()
    wx.InitAllImageHandlers()
    
    frame_1 = mainFrame(None, -1, "")           # Create the main window.
    app.SetTopWindow(frame_1)
    frame_1.Show()                              # Show the main window
    app.MainLoop()                              # Begin user interactions.
