#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#       pvg_panel_one.py
#
#       Copyright 2011 Giorgio Gilestro <giorgio@gilest.ro>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
#       Revisions by Caitlin Laughrey and Loretta E Laughrey in 2016.

# %%                                                            for debugging
"""
Prints file, class, and function names and line number for each definition.
- turn this on/off by replacing 'debugprt(' with 'prt(' or vice versa.
"""
#                                                             imports
import wx, os
import wx.lib.newevent
import pysolovideo as pv
import pvg_common as cmn
import cv2, cv
ThumbnailClickedEvt, EVT_THUMBNAIL_CLICKED = wx.lib.newevent.NewCommandEvent()
# from wx.lib.filebrowsebutton import FileBrowseButton, DirBrowseButton
from wx.lib.filebrowsebutton_LL import FileBrowseButton, DirBrowseButton

class previewPanel(wx.Panel):
    """
    A panel showing the video images.
    Used for thumbnails
    """

    def __init__(self, parent, cfg, mon_num=1, cam_size=(300, 300), fps=1, keymode=True):

        self.cfg = cfg
        self.config_obj = self.cfg.config_obj
        self.configDict = self.cfg.configDict

        self.parent = parent

        #                                   TODO: mon_num should not be zero
        if mon_num == 0:
            mon_num = 1
            print('$$$$$$  why was mon_num == 0?')
        self.mon_num = mon_num
        self.mon_name = 'Monitor%d' % self.mon_num

        self.sourceType = self.configDict[self.mon_name + ', sourcetype']
        self.source = self.configDict[self.mon_name + ', source']
        self.resolution = self.cam_size = cam_size
        self.fps = fps
        self.track = self.configDict[self.mon_name + ', track']
        self.isSDMonitor = self.configDict[self.mon_name + ', issdmonitor']
        self.trackType = self.configDict[self.mon_name + ', tracktype']

        wx.Panel.__init__(self, parent, wx.ID_ANY, style=wx.WANTS_CHARS)
        self.SetMinSize(self.cam_size)

        self.interval = 1000 / self.fps  # fps determines refresh interval in ms

        self.SetBackgroundColour('#A9A9A9')

        # determine the monitor class and generate the monitor object accordingly
        if self.sourceType == 0:  # source is a real camera:
            source_obj = pv.realCam()
        elif self.sourceType == 1:  # source is a video file
            source_obj = pv.virtualCamMovie(path=os.path.split(self.source)[0], resolution=self.cam_size)
        elif self.sourceType == 2:
            source_obj = pv.virtualCamFrames(path=os.path.split(self.source)[0], resolution=self.cam_size)
        else:
            print('$$$$$$ why is there no sourceType?')
            source_obj = None

        self.mon = pv.Monitor(cfg=self.cfg, mon_name=self.mon_name, cam_size=self.cam_size, fps=self.fps)

        self.drawROI = True
        self.timestamp = False
        self.recording = False
        self.isPlaying = False

        self.allowEditing = True  # TODO: mask variable initialization
        self.dragging = None  # Set to True while dragging
        self.startpoints = None  # Set to (x,y) when mouse starts drag
        self.track_window = None  # Set to rect when the mouse drag finishes
        self.selection = None
        self.selROI = -1
        self.polyPoints = []
        self.keymode = keymode

        self.ACTIONS = {
            "a": [self.AutoMask, "Automatically create the mask"],
            "c": [self.ClearLast, "Clear last selected area of interest"],
            "t": [self.Calibrate, "Calibrate the mask after selecting two points distant 1cm from each other"],
            "x": [self.ClearAll, "Clear all marked region of interest"],
            "j": [self.SaveCurrentSelection, "Save last marked area of interest"],
            "s": [self.SaveMask, "Save mask to file"],
            "q": [self.Stop, "Close connection to camera"]
        }

        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        # self.Bind( wx.EVT_LEFT_DCLICK, self.AddPoint )
        self.Bind(wx.EVT_LEFT_DCLICK, self.SaveCurrentSelection)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        self.Bind(wx.EVT_RIGHT_DOWN, self.ClearLast)
        # self.Bind( wx.EVT_MIDDLE_DOWN, self.SaveCurrentSelection )

        if keymode:
            self.Bind(wx.EVT_CHAR, self.onKeyPressed)
            self.SetFocus()

    def ClearAll(self, event=None):

        """
        Clear all ROIs
        """
        self.mon.delROI(-1)

    def ClearLast(self, event=None):

        """
        Cancel current drawing
        """

        if self.allowEditing:
            self.selection = None
            self.polyPoints = []

            if self.selROI >= 0:
                self.mon.delROI(self.selROI)
                self.selROI = -1

    def SaveCurrentSelection(self, event=None):

        """
        save current selection
        """
        if self.allowEditing and self.selection:
            self.mon.addROI(self.selection, 1)
            self.selection = None
            self.polyPoints = []

    def AddPoint(self, event=None):

        """
        Add point
        """

        if self.allowEditing:
            if len(self.polyPoints) == 4:
                self.polyPoints = []

            # This is to avoid selecting a neigh. area when drawing point
            self.selection = None
            self.selROI = -1

            x = event.GetX()
            y = event.GetY()
            self.polyPoints.append((x, y))

    def onLeftDown(self, event=None):

        """
        """

        if self.allowEditing and self.mon:
            x = event.GetX()
            y = event.GetY()
            r = self.mon.isPointInROI((x, y))

            if r < 0:
                self.startpoints = (x, y)
            else:
                self.selection = self.mon.getROI(r)
                self.selROI = r

    def onLeftUp(self, event=None):

        """
        """
        if self.allowEditing:
            self.dragging = None
            self.track_window = self.selection

            if len(self.polyPoints) == 4:
                self.selection = self.polyPoints
                self.polyPoints = []

    def onMotion(self, event=None):

        """
        """
        if self.allowEditing:
            x = event.GetX()
            y = event.GetY()

            self.dragging = event.Dragging()

            if self.dragging:
                xmin = min(x, self.startpoints[0])
                ymin = min(y, self.startpoints[1])
                xmax = max(x, self.startpoints[0])
                ymax = max(y, self.startpoints[1])

                x1, y1, x2, y2 = (xmin, ymin, xmax, ymax)
                self.selection = (x1, y1), (x2, y1), (x2, y2), (x1, y2)

    def prinKeyEventsHelp(self, event=None):

        """
        """
        for key in self.ACTIONS:
            print "%s\t%s" % (key, self.ACTIONS[key][1])

    def onKeyPressed(self, event):

        """
        Regulates key pressing responses:
        """
        key = chr(event.GetKeyCode())

        if key == "g" and self.mon.writer: self.mon.grabMovie = not self.mon.grabMovie

        if self.ACTIONS.has_key(key):
            self.ACTIONS[key][0]()

    def Calibrate(self, event=None):

        """
        """
        if len(self.polyPoints) > 2:
            print "You need only two points for calibration. I am going to use the first two"

        if len(self.polyPoints) > 1:
            pt1, pt2 = self.polyPoints[0], self.polyPoints[1]
            r = self.mon.calibrate(pt1, pt2)
            self.polyPoints = []
        else:
            print "You need at least two points for calibration."

        print "%spixels = 1cm" % r

    def AutoMask(self, event=None):

        """
        """
        if len(self.polyPoints) > 1:
            pt1, pt2 = self.polyPoints[0], self.polyPoints[1]
            self.mon.autoMask(pt1, pt2)
        else:
            print "Too few points to automask"
        self.polyPoints = []

    def SaveMask(self, event=None):

        """
        """
        self.mon.saveROIS()

    def setMonitor(self, camera, size=(300,300)):
        """
        """
        self.camera = camera
        self.size = size
        self.mon = pv.Monitor(self.cfg, self.mon_name, self.size, self.fps)

        frame = cv.CreateMat(self.size[1], self.size[0], cv.CV_8UC3)
        self.bmp = wx.BitmapFromBuffer(self.size[0], self.size[1], frame.tostring())

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.playTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onNextFrame)


    def paintImg(self, img):

        """
        """
        if img:
            depth, channels = img.depth, img.nChannels
            datatype = cv.CV_MAKETYPE(depth, channels)

            frame = cv.CreateMat(self.size[1], self.size[0], datatype)
            cv.Resize(img, frame)

            cv.CvtColor(frame, frame, cv.CV_BGR2RGB)
            # cv.CvtColor(frame, frame, cv.CV_GRAY2RGB)

            self.bmp.CopyFromBuffer(frame.tostring())
            self.Refresh()

    def onPaint(self, evt):

        """
        """
        if self.bmp:
            dc = wx.BufferedPaintDC(self)
            # self.PrepareDC(dc)
            dc.DrawBitmap(self.bmp, 0, 0, True)
        evt.Skip()

    def onNextFrame(self, evt):

        """
        """
        img = self.mon.GetImage(drawROIs=self.drawROI, selection=self.selection, crosses=self.polyPoints,
                                timestamp=self.timestamp)
        self.paintImg(img)
        if evt: evt.Skip()

    def Play(self, status=True, showROIs=True):

        """
        """

#        if self.mon is not None and self.resolution is not None and self.mon is not None:
#            self.mon.setSource(self.camera, self.resolution)

        if self.mon:
            self.drawROI = showROIs
            self.isPlaying = status

            if status:
                self.playTimer.Start(self.interval)
            else:
                self.playTimer.Stop()

    def Stop(self):

        """
        """
        self.Play(False)
        self.mon.close()

    def hasMonitor(self):

        """
        """
        a = (self.mon is not None)

        return a



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Thumbnail Panel
class thumbnailPanel(previewPanel):
    """
    A small preview Panel to be used as thumbnail
    """
    def __init__( self, parent, cfg, mon_num=1, cam_size=(300,300), fps=5 ):

        self.cfg = cfg
        self.config_obj = self.cfg.config_obj
        self.configDict = self.cfg.configDict
        self.size = cam_size
        self.fps = fps

        previewPanel.__init__(self, parent, cfg, mon_num, self.size, self.fps, keymode=False)

        self.number = int(mon_num)
        self.allowEditing = False

        self.displayNumber()

        self.Bind(wx.EVT_LEFT_UP, self.onLeftClick)


# %%                                                Show Monitor Numbers
    def displayNumber(self):

        """
        Displays the monitor number over top of the thumbnail
        """
        # font type: wx.DEFAULT, wx.DECORATIVE, wx.ROMAN, wx.SCRIPT, wx.SWISS, wx.MODERN
        # slant: wx.NORMAL, wx.SLANT or wx.ITALIC
        # weight: wx.NORMAL, wx.LIGHT or wx.BOLD
        # font1 = wx.Font(10, wx.SWISS, wx.ITALIC, wx.NORMAL)
        # use additional fonts this way ...
        pos = int(self.size[0]/2 - 20), int(self.size[1]/2 - 20),
        font1 = wx.Font(35, wx.SWISS, wx.NORMAL, wx.NORMAL)
        text1 = wx.StaticText(self, wx.ID_ANY, '%s' % self.number, pos)
        text1.SetFont(font1)


# %%                                                        Left Click
    def onLeftClick(self, event):

        """
        Event handler for thumbnail being clicked on
        Send signal around that the thumbnail was clicked
        """
        event = ThumbnailClickedEvt(self.GetId())

        event.id = self.GetId()
        event.number = self.number
        event.thumbnail = self

        self.GetEventHandler().ProcessEvent(event)



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Panel Grid View
class panelGridView(wx.ScrolledWindow):
    """
    The scrollable grid of monitor thumbnails on panel one                      # number in monitors not always there
    """
    def __init__(self, parent, cfg):

        self.cfg = cfg
        self.config_obj = self.cfg.config_obj
        self.configDict = self.cfg.configDict
        self.ThumbnailSize = self.configDict['Options, thumbnailsize']
        self.n_mons = gridSize = self.configDict['Options, monitors']
        self.fps = self.configDict['Options, fps_preview']

# %%                                                  Set up scrolling window
        wx.ScrolledWindow.__init__(self, parent, wx.ID_ANY, size=(-1,600))
        self.SetScrollbars(1, 1, 1, 1)
        self.SetScrollRate(10, 10)

        self.parent = parent
        self.ThumbnailSize = self.configDict['Options, thumbnailsize']
        self.fps = self.configDict['Options, fps_preview']
        self.gridSize = gridSize
        self.grid_mainSizer = wx.GridSizer(6,3,2,2)                         # TODO:  can (should?) the row numbers be variable?

# %%                                              Populate the thumbnail grid
        self.previewPanels = []
        for i in range(0, int(self.gridSize)):
            self.previewPanels.append ( thumbnailPanel(self, self.cfg, mon_num=i+1,        # mon_num should be 1-indexed
                                                       cam_size=self.ThumbnailSize, fps=self.fps))
            self.grid_mainSizer.Add(self.previewPanels[i])

        # %%                                              Make elements visible in UI
        self.SetSizer(self.grid_mainSizer)
        # Set up listener for clicking on thumbnails
        self.Bind(EVT_THUMBNAIL_CLICKED, self.onThumbnailClicked)


# %%                                                    Thumbnail Clicked
    def onThumbnailClicked(self, event):

        """
        Event handler that makes clicking a thumbnail update the dropdown menu
        Relay event to sibling panel
        """
        wx.PostEvent(self.parent.lowerPanel, event)
        event.Skip()


# %%                                                        Update Monitors
    # Should be working
    def updateMonitors(self, old, now):

        """
        Changes number of monitor thumbnails.
        """
        diff = old - now
        i = diff
        while i != 0:                   # Adding monitors to grid
            if diff < 0:
                i += 1
                # Make a new thumbnail and add to list
                self.previewPanels.append ( thumbnailPanel(self, self.cfg, mon_num=old,        # mon_num should be 1-indexed
                                                           cam_size=self.ThumbnailSize, fps=self.fps))
                # Add thumbnail to layout
                self.grid_mainSizer.Add(self.previewPanels[old])
                self.grid_mainSizer.Layout()
                old += 1
            elif diff > 0:
                # Removing monitors from grid
                i -= 1
                # Remove last thumbnail from list
                self.previewPanels.pop(len(self.previewPanels)-1)
                # Remove last thumbnail from layout
                self.grid_mainSizer.Hide(old-1)
                self.grid_mainSizer.Remove(old-1)
                self.grid_mainSizer.Layout()
                old -= 1



# %%                                                    Change Thumbnail size
    def updateThumbs(self, new):

        self.ThumbnailSize = new

        for i in range(0, self.gridSize):
            self.previewPanels[i].SetThumbnailSize(new)
            self.grid_mainSizer.Layout()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Panel Configuration
class panelConfigure(wx.Panel):
    """
    The lower half of panel one with the configuration settings                 # this panel could be shorter to cover less of the monitors
    """
    def __init__(self, parent, cfg, mon_num=1):

        self.cfg = cfg
        self.config_obj = self.cfg.config_obj
        self.configDict = self.cfg.configDict
        self.pDir = self.configDict['Options, pDir']

        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(-1,300),
            style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)
        self.parent = parent

        self.mon_num = mon_num                          # TODO: replace lower sizer with my version
        self.mon_name = 'Monitor%d' % self.mon_num
        self.track = False
        self.source = self.configDict[self.mon_name + ', source']
        self.sourceType = self.configDict[self.mon_name + ', sourcetype']
        self.mask_file = self.configDict[self.mon_name + ', maskfile']
        self.trackType = self.configDict[self.mon_name + ', tracktype']
        self.cam_size = self.configDict['Options, thumbnailsize']
        self.fps = self.configDict[self.mon_name + ', fps_recording']

        lowerSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Static box1 (LEFT)
        sb_1 = wx.StaticBox(self, -1, "Select Monitor")#, size=(250,-1))
        self.sbSizer_1 = wx.StaticBoxSizer (sb_1, wx.VERTICAL)

        # ----------- reset if options change
        n_monitors = self.configDict['Options, monitors']                                                               # n_monitors (monitors)
        self.MonitorList = ['Monitor %s' % (int(m) + 1) for m in range( n_monitors )]
        # ----------- can reset by button                                                                               # thumbnail number (mon_num)
        self.thumbnailNumber = wx.ComboBox(self, -1, size=(-1,-1) , choices=self.MonitorList,
                                           style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.thumbnailNumber.SetValue(self.MonitorList[0])
        # ----------- can reset by button                                                                               # displays filename only.  don't GetValue
        self.currentSource = wx.TextCtrl (self, -1, os.path.split(self.source)[1], style=wx.TE_READONLY)
        self.currentSource.Value = '<path>\\' + os.path.split(self.source)[1]
        # -----------
        self.Bind ( wx.EVT_COMBOBOX, self.onChangingMonitor, self.thumbnailNumber)

        btnSizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.btnPlay = wx.Button( self, wx.ID_FORWARD, label="Play")
        self.btnStop = wx.Button( self, wx.ID_STOP, label="Stop")
        self.Bind(wx.EVT_BUTTON, self.onPlay, self.btnPlay)
        self.Bind(wx.EVT_BUTTON, self.onStop, self.btnStop)
        self.btnPlay.Enable(False); self.btnStop.Enable(False)
        self.applyButton = wx.Button( self, wx.ID_APPLY )
        self.applyButton.SetToolTip(wx.ToolTip("Apply and Save to file"))
        self.Bind(wx.EVT_BUTTON, self.onApplySource, self.applyButton)

        btnSizer_1.Add ( self.btnPlay , 0, wx.ALIGN_LEFT|wx.ALL, 5 )
        btnSizer_1.Add ( self.btnStop , 0, wx.ALIGN_CENTER|wx.LEFT|wx.TOP|wx.DOWN, 5 )
        btnSizer_1.Add ( self.applyButton, 0, wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        self.sbSizer_1.Add ( self.thumbnailNumber, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        self.sbSizer_1.Add ( self.currentSource, 0, wx.EXPAND|wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        self.sbSizer_1.Add ( btnSizer_1, 0, wx.EXPAND|wx.ALIGN_BOTTOM|wx.TOP, 5 )

        lowerSizer.Add (self.sbSizer_1, 0, wx.EXPAND|wx.ALL, 5)

        # Static box2 (CENTER)
        sb_2 = wx.StaticBox(self, -1, "Select Video input" )
        self.sbSizer_2 = wx.StaticBoxSizer (sb_2, wx.VERTICAL)
        self.grid2 = wx.FlexGridSizer( 0, 2, 0, 0 )

        # ----------- can reset in options
        self.n_cams = self.configDict['Options, webcams']
        self.WebcamsList = [ 'Webcam %s' % (int(w) +1) for w in range( self.n_cams ) ]

        rb1 = wx.RadioButton(self, -1, 'Camera', style=wx.RB_GROUP)
        if self.sourceType == 0:  rb1.Value = True
        else: rb1.Value = False
        source1 = wx.ComboBox(self, -1, size=(285,-1) , choices = self.WebcamsList, style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        source1.Value = self.WebcamsList[0]
        self.Bind(wx.EVT_COMBOBOX, self.sourceCallback, source1)

        rb2 = wx.RadioButton(self, -1, 'File' )
        if self.sourceType == 1:  rb2.Value = True
        else: rb2.Value = False
        source2 = FileBrowseButton(self,
                        id = wx.ID_ANY,
                        pos = wx.DefaultPosition,
                        size = (300,-1),
                        style = wx.TAB_TRAVERSAL,
                        labelText = '',
                        buttonText = "Browse",
                        toolTip = "Type filename or click browse to choose file",
                        # following are the values for a file dialog box
                        dialogTitle = "Choose a file",
                        startDirectory = self.pDir,
                        initialValue = self.source,
                        fileMask = "*.*",
                        fileMode = wx.FD_OPEN,
                        # callback for when value changes (optional)
                        changeCallback = self.sourceCallback,
                        labelWidth = 0,
                        name = 'fileBrowseButton')
        source2.Value = self.source

        rb3 = wx.RadioButton(self, -1, 'Folder' )
        if self.sourceType == 2:  rb3.Value = True
        else: rb3.Value = False
        source3 = DirBrowseButton (self,
                        id = wx.ID_ANY,
                        pos = wx.DefaultPosition, size = (300,-1),
                        style=wx.DD_DIR_MUST_EXIST,
                        labelText = '',
                        buttonText = 'Browse',
                        toolTip = 'Type directory name or browse to select',
                        dialogTitle = '',
                        startDirectory = self.pDir,
                        changeCallback = self.sourceCallback,
                        dialogClass = wx.DirDialog,
                        newDirectory = False,
                        name = 'dirBrowseButton')
        source3.SetValue(self.pDir)

        self.controls = []
        self.controls.append((rb1, source1))
        self.controls.append((rb2, source2))
        self.controls.append((rb3, source3))

        for radio, source in self.controls:
            self.grid2.Add( radio , 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2 )
            self.grid2.Add( source , 0, wx.ALIGN_CENTRE|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2 )
            self.Bind(wx.EVT_RADIOBUTTON, self.onChangeSource, radio )
            source.Enable(False)

        self.controls[self.sourceType][1].Enable(True)

        # grid2.Add(wx.StaticText(self, -1, ""))

        self.sbSizer_2.Add( self.grid2 )
        lowerSizer.Add(self.sbSizer_2, 0, wx.EXPAND|wx.ALL, 5)

        # Static box3 (RIGHT)
        sb_3 = wx.StaticBox(self, -1, 'Set Tracking Parameters')
        sbSizer_3 = wx.StaticBoxSizer (sb_3, wx.VERTICAL)

        sbSizer_31 = wx.BoxSizer (wx.HORIZONTAL)
        # --------- can reset by button                                                                                 # activateTracking (track)
        self.activateTracking = wx.CheckBox(self, -1, 'Activate Tracking')
        self.activateTracking.SetValue(False)
        self.activateTracking.Bind ( wx.EVT_CHECKBOX, self.onActivateTracking)
        # --------- can reset by button                                                                                 # sleepDepMon (isSDMonitor)
        self.sleepDepMon = wx.CheckBox(self, -1, 'Sleep Deprivation Monitor')
        self.sleepDepMon.SetValue(False)
        self.sleepDepMon.Bind ( wx.EVT_CHECKBOX, self.onSDMonitor)
        self.sleepDepMon.Enable(False)

        sbSizer_31.Add (self.activateTracking, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        sbSizer_31.Add (self.sleepDepMon, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        # --------- can reset by button                                                                                 # pickMaskBrowser (maskfile)
        self.pickMaskBrowser = FileBrowseButton(self, -1, labelText='Mask File')

        # sbSizer_3.Add ( self.activateTracking , 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        sbSizer_3.Add ( sbSizer_31 , 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        sbSizer_3.Add ( self.pickMaskBrowser , 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
        # ---------- can reset by button                                                                                # trackTypeList (trackType)
        self.trackRB1 = (wx.RadioButton(self, -1, 'Activity as distance traveled', style=wx.RB_GROUP))
        self.trackRB2 = (wx.RadioButton(self, -1, 'Activity as midline crossings count'))
        self.trackRB3 = (wx.RadioButton(self, -1, 'Only position of flies'))

        self.trackTypeList = []             # True/False depending on enabled radio buttons
        self.trackTypeList.append(self.trackRB1)
        self.trackTypeList.append(self.trackRB2)
        self.trackTypeList.append(self.trackRB3)

        sbSizer_3.Add (wx.StaticText ( self, -1, 'Calculate fly activity as...'), 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        for t_type in range(len(self.trackTypeList)):
            sbSizer_3.Add (self.trackTypeList[t_type], 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )

        lowerSizer.Add(sbSizer_3, -1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(lowerSizer)
        self.Bind(EVT_THUMBNAIL_CLICKED, self.onThumbnailClicked)


# %%                                                     Input source
    def __getSource(self):

        """
        check which source is ticked and what is the associated value
        Returns the selected source type and its value
        """

        for (r, s), st in zip(self.controls,range(3)):
            if r.GetValue():
                source = s.GetValue()
                sourceType = st
        return source, sourceType

# %%                                                Input tracking type
    def __getTrackingType(self):

        """
        return which type of tracking we are chosing
        ['DISTANCE','VBS','XY_COORDS']
        """
        count = 1                               # gets trackType value (only one will be true
        for t_type in zip(self.trackTypeList,range(3)):
            if self.trackTypeList[t_type].GetValue():
                trackType = count
            else:
                trackType = count
            count = count +1
        return trackType

# %%                                                            play button
    def onPlay (self, event=None):

        """
        # Event handler for the play button
        """
        self.thumbnail = self.parent.scrollThumbnails.previewPanels[self.mon_num-1]         # mon_num is 1-indexed, but previewPanels is a 0-indexed list. #this is not very elegant
        if self.thumbnail:
            self.thumbnail.Play()
            self.btnStop.Enable(True)


# %%                                                            Stop Button
    def onStop (self, event):

        """
        Event handler for the stop button
        """
        if self.thumbnail and self.thumbnail.isPlaying:
            self.thumbnail.Stop()
            self.btnStop.Enable(False)


# %%                                                    Click Thumbnail
    def onThumbnailClicked(self, event):

        """
        Picking thumbnail by clicking on it
        Event handler for changing monitor via clicking on thumbnail
        """
        self.mon_num = event.number
        self.thumbnail = event.thumbnail
        self.thumbnailNumber.SetValue(self.MonitorList[self.mon_num -1])
        self.updateThumbnail(self.thumbnail, 'Monitor%d' % self.mon_num)


# %%                                                    Monitor dropdown box
    def onChangingMonitor(self, event):

        """
        Picking thumbnail by using the dropbox
        Event handler for changing monitor via dropdown box
        """
        sel = event.GetString()
        self.mon_num = self.MonitorList.index(sel)  +1    # keep mon_num as 1-indexed
        self.thumbnail = self.parent.scrollThumbnails.previewPanels[self.mon_num-1]         # mon_num is 1-indexed, but previewPanels is a 0-indexed list. #this is not very elegant
        self.updateThumbnail(self.thumbnail, 'Monitor%d' % self.mon_num)



# %%                                            Refresh thumbnail and controls
    def updateThumbnail(self, thumbnail, mon_name):

        """
        Reset thumbnail data based on last saved configuration
        """

        sourceType = self.configDict[mon_name + ', sourcetype']
        source = self.configDict[mon_name + ', source']
        if sourceType == 0 and source != '':
            source = self.WebcamsList[source]

        # Ensure source and type match throughout program
        self.source = self.thumbnail.source = source
        self.sourceType = self.thumbnail.sourceType = sourceType
        track = self.configDict[mon_name + ', track']
        self.thumbnail.track = track
        isSDMonitor = self.configDict[mon_name + ', issdmonitor']
        if self.thumbnail.hasMonitor():
                self.thumbnail.mon.isSDMonitor = isSDMonitor

        #update first static box
        active = self.thumbnail.hasMonitor()
        self.applyButton.Enable ( active )
        self.btnPlay.Enable ( active )
        self.btnStop.Enable ( active and self.thumbnail.isPlaying )

        self.currentSource.Value = '<path>\\' + os.path.split(self.source)[1]                # only filename is shown in currentSource textctrl

        #update second static box
        for radio, src in self.controls:
            src.Enable(False); src.SetValue('')

        radio, src = self.controls[self.sourceType]
        radio.SetValue(True); src.Enable(True)
        src.SetValue(self.source)

        #update third static box
        self.activateTracking.SetValue(self.thumbnail.track)
        self.sleepDepMon.SetValue(isSDMonitor)
        mask_file = self.configDict[mon_name + ', maskfile']
        self.pickMaskBrowser.SetValue(mask_file or '')
        trackType = self.configDict[mon_name + ', tracktype']

        for t_type in range(len(self.trackTypeList)):
            if self.trackTypeList[t_type] :
                trackType = True

        radio, src = self.controls[self.sourceType]
        radio.SetValue(True); src.Enable(True)
        src.SetValue(self.source)


# %%
    def sourceCallback (self):

        self.applyButton.Enable(True)


# %%                                                        Radio buttons
    def onChangeSource(self, event):

        # Determine which radio button was selected
        radio_selected = event.GetEventObject()

        # Enable the selected source, disable all others
        for radio, source in self.controls:
            if radio is radio_selected:
                source.Enable(True)
            else:
                source.Enable(False)

        self.applyButton.Enable(True)


# %%                                                    Apply Button
    def onApplySource(self, event):

        """
        Get source and mask info from the user's selections
        Event handler for the Apply button on the lower left of panel one
        """

        # Update the source settings
        count = 1                                   # used to determine sourceType
        for radio, src in self.controls:
            if radio.GetValue():                              # if the radio button is enabled
                self.source = src.GetValue()
                self.currentSource.Value = '<path>\\' + os.path.split(self.source)[1]             # currentSource shows only filename
                self.sourcetype = count
            count = count + 1

        # set thumbnail's monitor
        self.thumbnail = self.parent.scrollThumbnails.previewPanels[self.mon_num-1]         # mon_num is 1-indexed, but previewPanels is a 0-indexed list. #this is not very elegant
        self.thumbnail.setMonitor(self.source)

        # Enable buttons
        self.btnPlay.Enable(True)
        self.activateTracking.Enable(True)
        self.pickMaskBrowser.Enable(True)

        self.cfg.save_Config(new=False)  # TODO: just save settings for this monitor instead of everything?

#        self.thumbnail.setMonitor(self.source, size=self.cam_size)

    # %%                                                        Activate Tracking
    def onActivateTracking(self, event):

        if self.thumbnail:
            self.thumbnail.track = event.IsChecked()


# %%
    def onSDMonitor(self, event):

        if self.thumbnail:
            self.thumbnail.mon.isSDMonitor = event.IsChecked()


# %%                                                Update monitor dropdown box
    def updateMonitors(self, now):

        """
        Updates the dropdown box of monitors on lower half of panel one
        """
        # Generate new list of monitors
        self.MonitorList = ['Monitor %s' % (int(m) + 1) for m in range(now)]

        # Create a new combobox with the correct number of monitors
        self.thumbnailNumber = wx.ComboBox(self, -1, size=(-1,-1) ,
            choices=self.MonitorList, style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind (wx.EVT_COMBOBOX, self.onChangingMonitor, self.thumbnailNumber)

        # Remove the old combobox and replace it with this new one
        self.sbSizer_1.Hide(0)
        self.sbSizer_1.Remove(0)
        self.sbSizer_1.Insert(0, self.thumbnailNumber, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        # Display UI changes
        self.sbSizer_1.Layout()


# %%                                                Update webcam dropdown box
    def updateWebcams(self, now):

        """
        Updates the dropdown box of cameras on lower half of panel one
        """
        # Generate the list of webcams
        self.WebcamsList = [ 'Webcam %s' % (int(w) +1) for w in range(now) ]

        # Create a new combobox with correct number of webcams
        source1 = wx.ComboBox(self, -1, size=(285,-1) , choices = self.WebcamsList,
            style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind(wx.EVT_COMBOBOX, self.sourceCallback, source1)
        source1.Enable(True)

        # Create a new radio button to go with the combobox
        self.controls.remove(self.controls[0])
        rb1 = wx.RadioButton(self, -1, 'Camera', style=wx.RB_GROUP)
        self.Bind(wx.EVT_RADIOBUTTON, self.onChangeSource, rb1)

        # Add the button and combobox to the controls list
        self.controls.insert(0, (rb1,source1))

        # Remove the old ones from the layout and add the new ones
        self.grid2.Hide(0)
        self.grid2.Remove(0)
        self.grid2.Insert(0, rb1)
        self.grid2.Hide(1)
        self.grid2.Remove(1)
        self.grid2.Insert(1, source1)

        # Show changes to UI
        self.grid2.Layout()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Panel One
class panelOne(wx.Panel):
    """
    Panel number One:  All the thumbnails
    """
    def __init__(self, parent, cfg):

        self.cfg = cfg
        self.config_obj = self.cfg.config_obj
        self.configDict = self.cfg.configDict

        wx.Panel.__init__(self, parent)

        # Retrieve settings
        self.n_mons = self.configDict['Options, monitors']
        self.tn_size = self.configDict['Options, thumbnailsize']
        self.n_cams = self.configDict['Options, webcams']

        self.temp_source  = ''                                          # TODO: what's temp_source?
        self.source = self.configDict['Monitor1, source']               # initialize with monitor 1 settings
        self.sourceType = self.configDict['Monitor1, sourcetype']

        # Create a grid of thumbnails and a configure panel

        self.scrollThumbnails = panelGridView(self, self.cfg)
        self.lowerPanel = panelConfigure(self, self.cfg, mon_num=1)
        # Display elements
        self.PanelOneSizer = wx.BoxSizer(wx.VERTICAL)
        self.PanelOneSizer.Add(self.scrollThumbnails, 1, wx.EXPAND, 0)
        self.PanelOneSizer.Add(self.lowerPanel, 0, wx.EXPAND, 0)
        self.SetSizer(self.PanelOneSizer)


# %%                                                         Stop Playing
    def StopPlaying(self, event):

        self.lowerPanel.onStop(event)



# %%                                                            Refresh
    def onRefresh(self, event):

        """
        Checks for changes to be made to UI and implements them.
        """
        # Check number of monitors
        now_n_mons = self.configDict['Options, monitors']
        if self.n_mons != now_n_mons:
            self.scrollThumbnails.updateMonitors(self.n_mons, now_n_mons)
            self.lowerPanel.updateMonitors(self.n_mons)
            self.n_mons = now_n_mons

        # Check thumbnail size
        thumbnailSize = self.configDict['Options, thumbnailsize']
        if self.tn_size != thumbnailSize:
            self.scrollThumbnails.updateThumbs(thumbnailSize)
            self.tn_size = thumbnailSize

        # Check number of webcams
        webcams = self.configDict['Options, webcams']
        if self.n_cams != webcams:
            self.lowerPanel.updateWebcams(webcams)
            self.n_cams = webcams

        # Show changes to UI
        self.PanelOneSizer.Layout()
