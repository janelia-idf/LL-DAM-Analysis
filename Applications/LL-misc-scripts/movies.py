# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 12:10:05 2016

@author: laughreyl
"""

import cv2, cv, os, wx
import numpy as np

"""
def showimg(title, img):
        img_nparry = np.asarray(img )
        cv2.imshow(title,img_nparry)
        cv2.waitKey()

"""

class mainFrame(wx.Frame):
    def __init__(self):

        self.source = 'c:\\Users\\Lori\\Documents\\GitHub\\LL-DAM-Analysis\\Input\\fly_movie.avi'

        self.size = (500,500)
        wx.Frame.__init__(self, wx.ID_ANY, size=self.size, name='main frame')

        self.interval = 1000 # fps determines refresh interval in ms
        self.mon_name = 'Monitor 1'

        print("movie name = ", self.source)
        print('file exists? %s',os.path.isfile(self.source))
        print( self.size, self.interval)

#        cv.NamedWindow('Monitor Panel', cv2.WINDOW_NORMAL | wx.NO_BORDER)

        mysizer = wx.BoxSizer(wx.HORIZONTAL)

        panel1 = thumbnail(self.source)
        panel2 = thumbnail(self.source)

        mysizer.Add(panel1, 0, wx.ALL, 5)
        mysizer.Add(panel2, 0, wx.ALL, 5)

        SetSizer(mysizer, 0, wx.ALL, 5)


#        self.playVideo('Monitor Panel')

class thumbnail(wx.Panel):

    def __init__(self, source):
        capture = cv2.VideoCapture()
        for k in range(0, 10):
            if not capture.isOpened():
                capture = cv2.VideoCapture()
                cv2.waitKey(1000)

        if capture.isOpened():
            print('Capture successful')
            retval, imgFrame = capture.read()
            capture.release()

        else:
            print('could not open file')

# ---------------------------------------------------------------



    def playVideo(self, mon_panel):
        capture = cv2.VideoCapture(self.source)
        for k in range(0, 10):
            if not capture.isOpened():
                capture = cv2.VideoCapture(self.source)
                cv2.waitKey(1000)

        if capture.isOpened():
            print('Capture successful')
            retval, imgFrame = capture.read()
            while retval:

                cv2.resizeWindow(mon_panel, 200,200)
                imgSized = cv2.resize(imgFrame, (200,200))
                cv2.imshow(mon_panel,imgSized)
                cv2.waitKey(self.interval)
                retval, imgFrame = capture.read()
            capture.release()

        else:
            print('could not open file')

if __name__ == "__main__":
    app = wx.App()
    wx.InitAllImageHandlers()

    frame_1 = mainFrame()           # Create the main window.
    app.SetTopWindow(frame_1)                   # Makes this window the main window
    frame_1.Show()                              # Shows the main window
    app.MainLoop()                              # Begin user interactions.
