#!/usr/bin/env python

import numpy
import sys, os
import wx, cv2, cv
import wx.lib.scrolledpanel as scrolled
from PIL import Image



class  WinFrame(wx.Frame):
    def __init__(self, parent, title, width, height):
        super(WinFrame, self).__init__(parent,
                                       title=title,
                                       size=(width, height))
        self.Panel = wx.Panel(self,size=(width/4,height),
                                  pos=(0,0),
                                  style=wx.BORDER)

        self.imgPanel = wx.Panel(parent=self,
                                 size=(width, height),
                                 pos=(0,0),
                                 style=wx.BORDER)

        self.bitMap = wx.StaticBitmap(parent=self.imgPanel)

        wxImg = self.makeBitMap()
#        img=img.resize([1280, 1280], Image.ANTIALIAS)

#        wxImg = wx.EmptyImage(img.size[0], img.size[1])
#        wxImg.SetData(img.tostring())
#        wxImg = wxImg.ConvertToBitmap()
        self.bitMap.SetBitmap(wxImg)

        self.Centre()
        self.Show(True)

    def makeBitMap(self):

        source = 'c:\\Users\\Lori\\Documents\\GitHub\\LL-DAM-Analysis\\Input\\fly_movie.avi'
        count = 0
        self.capture = cv2.VideoCapture()
        self.capture.open(source)
        itworked = self.capture.isOpened()
        while not itworked and count > 20:
            count = count + 1
            self.capture = cv2.VideoCapture()
            cv2.waitKey(1000)
            itworked = self.capture.isOpened()

        if not itworked:
            print('applySource() unable to open file')
            self.imageFrame = cv.CreateImage(thumbsize, cv.IPL_DEPTH_8U, 3)
            cv.Zero(self.imageFrame)
        else:

            start = currentFrame = 0
            step = 1

            # finding the input properties
            capImg = self.capture.read()
            end = int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
            #            w = self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
            #            h = self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
            #            in_size = (int(w), int(h))
            #            datatype = capImg[1].dtype.num

            #            for frameNum in range(start, end, step):
            # make bitmap of current frame
            bmp = wx.BitmapFromBuffer(200, 250,
                                      capImg[1].tostring())  # element 0 is bool, element 1 is ndarray
            return bmp

    def __del__(self):
        super(WinFrame, self).__del__()

class myApp(wx.App):
    def __init__(self, width, height):
        super(myApp, self).__init__(0)

        self.width = width
        self.height = height

    def createFrame(self):
        self.frame = WinFrame(None, "show_img", self.width, self.height)
        self.SetTopWindow(self.frame)

    def __del__(self):
        super(myApp, self).__del__()


def mainFrame():
    app = myApp(480, 480)
    app.createFrame()
    app.MainLoop()

if "__main__" == __name__ :
    mainFrame()


