import pvg_common as cmn
import pvg_panel_one as p1
import wx, os, cv, cv2
import pysolovideo as pv
import subprocess
ThumbnailClickedEvt, EVT_THUMBNAIL_CLICKED = wx.lib.newevent.NewCommandEvent()

class mainFrame(wx.Frame):

    def __init__(self, parent, id, title):

    # test program settings --------------------------------------------------------------------------------------
        sources = []            # '','','','','',''
        n_mons = 6
        for i in range(0, n_mons):                              # sources will be 0-indexed
            sources.append('c:\\Users\\Lori\\Documents\\GitHub\\LL-DAM-Analysis\\Input\\fly_movie.avi')
        thumbsize = (320,250)
        windowsize = (int(thumbsize[0]*3), int(thumbsize[0]*n_mons/3))

    # main test program ------------------------------------------------------------------------------------------
        wx.Frame.__init__(self, parent, wx.ID_ANY, title='main frame', size=windowsize, style=wx.DEFAULT_FRAME_STYLE, name='mainFrame' )  # makes the main frame

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        pgv = panelGridView(self, n_mons, sources, windowsize, thumbsize)               # window of thumbnail panels
        mainSizer.Add(pgv.grid_mainSizer , 0, wx.EXPAND, 0)
        self.SetSizer(mainSizer)

# --------------------------------------------------------------------------------------- panelGridView
class panelGridView(wx.ScrolledWindow):                                         #  makes scrolling window of thumbnails

    def __init__(self, parent, n_mons, sources, windowsize, thumbsize):
        self.parent = parent
        self.n_mons = n_mons
        self.windowsize = windowsize
        self.thumbsize = thumbsize
        self.sources = sources

        wx.ScrolledWindow.__init__(self, self.parent, wx.ID_ANY, size=windowsize, name='scrolledWindow')
        self.SetScrollbars(1, 1, 1, 1)
        self.SetScrollRate(10, 10)
        self.grid_mainSizer = wx.GridSizer(6,3,2,2)

        # Populate the thumbnail grid
        self.thumbnailList = []
        for i in range(0,n_mons):                   # thumbnailList will be 0-indexed

            currentThumbPanel = thumbPanel(self, mon_num=i+1, thumbsize=self.thumbsize)  # create 1-indexed panel for thumbnail
            self.thumbnailList.append (currentThumbPanel)                              # put the panel in the list
            self.thumbnailList[i].applySource(self.sources[i], self.thumbsize)                         # apply the source to the panel
            self.grid_mainSizer.Add(self.thumbnailList[i], 0, wx.EXPAND, 0)                 # add to sizer

#        self.use_ffmpeg(self.thumbnailList, self.windowsize, self.thumbsize)                   # not working

        self.Bind(EVT_THUMBNAIL_CLICKED, self.onThumbnailClicked)



    def onThumbnailClicked(self, evt):
        """
        Picking thumbnail by clicking on it, and change currentThumbPanel
        """
        self.mon_num = evt.number
        self.currentThumbPanel = self.thumbnailList[self.mon_num]
#        self.updateThumbnail()

    def use_ffmpeg(self, thumbnailList, framesize, thumbsize):
        # """---------------------------------------------------------------------------------------- # using ffmpeg

        subprocess.call(
            'ffmpeg - i %s - i %s ' \
            ' - filter_complex " ' \
            'nullsrc=size=%s [base]; ' \
            '[0:v] setpts=PTS-STARTPTS, scale=%s [upperleft]; ' \
            '[1:v] setpts=PTS-STARTPTS, scale=%s [upperright]; ' \
            '[base][upperleft] overlay=shortest=1 [tmp1]; ' \
            '[tmp1][upperright] overlay=shortest=1:x=%s [tmp2]; ' \
            ' - c:v libx264 output.mkv'
            % ( thumbnailList[0], thumbnailList[1], tuple(framesize,), tuple(thumbsize,), tuple(thumbsize,), str(thumbsize[0]) ),
            shell=True
        )

        # """



class thumbPanel(wx.Panel):
    def __init__(self, parent, mon_num=1, thumbsize=(200,200)):   # id, pos, size, style, name

        wx.Panel.__init__(self, parent, wx.ID_ANY, size=thumbsize, style=wx.WANTS_CHARS, name='thumbPanel')
        self.parent = parent
        self.mon_num = mon_num
        self.thumbsize = thumbsize
        self.fps = 1                            # TODO:  set this to the frame rate from the config file
        self.interval = 1000/self.fps # fps determines refresh interval in ms

        self.SetMinSize(self.thumbsize)

        # display monitor number on panel
        pos = int(self.thumbsize[0]/8 - 20), int(self.thumbsize[1]/8 - 20),
        font1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        text1 = wx.StaticText( self, wx.ID_ANY, '%s' % (self.mon_num), pos)
        text1.SetFont(font1)

        self.Bind(wx.EVT_LEFT_UP, self.onLeftClick)



    def onLeftClick(self, evt):
        """
        Send signal around that the thumbnail was clicked
        """
        event = ThumbnailClickedEvt(self.GetId())

        event.id = self.GetId()
        event.number = self.mon_num
        event.thumbnail = self

        self.GetEventHandler().ProcessEvent(event)

    def applySource(self, source, thumbsize, loop=True):
        """
        apply image of source to the matching panel space in the grid.
        """
        count=0
        self.capture = cv2.VideoCapture()
        self.capture.open(source)
        itworked = self.capture.isOpened()
        while not itworked and count >20:
            count = count +1
            self.capture = cv2.VideoCapture()
            cv2.waitKey(1000)
            itworked = self.capture.isOpened()

        if not itworked:
            print('applySource() unable to open file')
            self.imageFrame = cv.CreateImage(thumbsize, cv.IPL_DEPTH_8U, 3)
            cv.Zero(self.imageFrame)
        else:

            start = currentFrame = 0
            step = self.fps

            # step through the first few frames to get a better picture
#            for count in range(0,50):
                # finding the input properties
            capImg = self.capture.read()
            end = int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

            #            for frameNum in range(start, end, step):
            """ --------------------------------------------------------------------------------------  this shows the image in a separate window
            cv2.imshow('thumbPanel', capImg[1])
            self.Show(True)
            """
            """-------------------------------------------------------------------------------------- this shows images in panel but they are corrupted
            bmp = wx.BitmapFromBuffer(self.thumbsize[0], self.thumbsize[1], capImg[1].tostring())     # output element 0 is bool, element 1 is ndarray
            self.bitMap = wx.StaticBitmap(self)
            self.bitMap.SetBitmap(bmp)
            """
            """---------------------------------------------------------------------------------------- # just not working
            # scale the image, preserving the aspect ratio
            self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                             wx.BitmapFromImage(capImg[1]))
            self.imageCtrl.SetBitmap(wx.BitmapFromImage(capImg[1]))
            self.Refresh()
            """



            # TODO:  also update lower panel information




# -------------------------------------------------------------------------------------
if __name__ == "__main__":

    app = wx.App()
    wx.InitAllImageHandlers()

    frame_1 = mainFrame(None, -1, "")           # Create the main window.
    app.SetTopWindow(frame_1)                   # Makes this window the main window
    frame_1.Show()                              # Shows the main window
    app.MainLoop()                              # Begin user interactions.
    print('Done.')
