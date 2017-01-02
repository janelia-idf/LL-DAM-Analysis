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

"""
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% imports
"""
import wx, os
import cv2, cv
import wx.lib.newevent
import wx.calendar
import wx.lib.masked as masked
import datetime
from inspect import currentframe                                                                     # debug
import pvg_common as cmn


ThumbnailClickedEvt, EVT_THUMBNAIL_CLICKED = wx.lib.newevent.NewCommandEvent()
from wx.lib.filebrowsebutton_LL import FileBrowseButton, DirBrowseButton


"""
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Settings
"""
pgm = 'pvg_panel_one.py'
start_datetime = (2016, 11, 13, 3, 47, 38)


# -------------------------------------------------------------------------------------------  Mask Maker Functions
class maskMakerFunctions():

    def __init__(self):

        print('mask maker functions called')
        # %%                                                                    # TODO: not needed for displaying the video image?  put these somewhere else
        """
        self.start_datetime = self.configDict[mon_name + ', start_datetime']           # date & time of start of video
        self.track = self.configDict[mon_name + ', track']
        self.trackType = self.configDict[mon_name + ', tracktype']              # distance tracking

    # ------------------------------------------------for cameras               # TODO: check what kind of device is the source & whether this was called by Mask Maker
        self.timestamp = False
        self.camera = None
        self.resolution = None
        self.recording = False

    # ------------------------------------------------for mask making
        self.isPlaying = False
        self.drawROI = True
        self.allowEditing = True
        self.dragging = None        # Set to True while dragging
        self.startpoints = None     # Set to (x,y) when mouse starts drag
        self.track_window = None    # Set to rect when the mouse drag finishes
        self.selection = None
        self.selROI = -1
        self.polyPoints = []
        self.keymode = keymode

        self.ACTIONS = {
                        'a': [self.AutoMask, 'Automatically create the mask'],
                        'c': [self.ClearLast, 'Clear last selected area of interest'],
                        't': [self.Calibrate, 'Calibrate the mask after selecting two points distant 1cm from each other'],
                        'x': [self.ClearAll, 'Clear all marked region of interest'],
                        'j': [self.SaveCurrentSelection, 'Save last marked area of interest'],
                        's': [self.SaveMask, 'Save mask to file'],
                        'q': [self.Stop, 'Close connection to camera']
                        }

        self.Bind( wx.EVT_LEFT_DOWN, self.onLeftDown )
        self.Bind( wx.EVT_LEFT_UP, self.onLeftUp )
        #self.Bind( wx.EVT_LEFT_DCLICK, self.AddPoint )
        self.Bind( wx.EVT_LEFT_DCLICK, self.SaveCurrentSelection )
        self.Bind( wx.EVT_MOTION, self.onMotion )
        self.Bind( wx.EVT_RIGHT_DOWN, self.ClearLast )
        #self.Bind( wx.EVT_MIDDLE_DOWN, self.SaveCurrentSelection )

        if keymode:
            self.Bind( wx.EVT_CHAR, self.onKeyPressed )
            self.SetFocus()
        """
    if cmn.call_tracking:  cmn.debugprt(self, currentframe(), pgm, 'end   ')

    def ClearAll(self, event=None):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        Clear all ROIs
        """
        self.mon.delROI(-1)
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def ClearLast(self, event=None):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        Cancel current drawing
        """

        if self.allowEditing:
            self.selection = None
            self.polyPoints = []

            if self.selROI >= 0:
                self.mon.delROI(self.selROI)
                self.selROI = -1
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def SaveCurrentSelection(self, event=None):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        save current selection
        """
        if self.allowEditing and self.selection:
            self.mon.addROI(self.selection, 1)
            self.selection = None
            self.polyPoints = []
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def AddPoint(self, event=None):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        Add point
        """

        if self.allowEditing:
            if len(self.polyPoints) == 4:
                self.polyPoints = []

            #This is to avoid selecting a neigh. area when drawing point
            self.selection = None
            self.selROI = -1

            x = event.GetX()
            y = event.GetY()
            self.polyPoints.append( (x,y) )
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')


    def onLeftDown(self, event=None):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """

        if self.allowEditing and self.mon:
            x = event.GetX()
            y = event.GetY()
            r = self.mon.isPointInROI ( (x,y) )

            if r < 0:
                self.startpoints = (x, y)
            else:
                self.selection = self.mon.getROI(r)
                self.selROI = r
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def onLeftUp(self, event=None):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        if self.allowEditing:
            self.dragging = None
            self.track_window = self.selection

            if len(self.polyPoints) == 4:
                self.selection = self.polyPoints
                self.polyPoints = []
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def onMotion(self, event=None):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                 # debug
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

                x1, y1, x2, y2  = (xmin, ymin, xmax, ymax)
                self.selection = (x1,y1), (x2,y1), (x2,y2), (x1, y2)
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def prinKeyEventsHelp(self, event=None):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        for key in self.ACTIONS:
            print '%s\t%s' % (key, self.ACTIONS[key][1])
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def onKeyPressed(self, event):                      # TODO: is this function working?
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        Regulates key pressing responses:
        """
        key = chr(event.GetKeyCode())

        if key == 'g' and self.mon.writer: self.mon.grabMovie = not self.mon.grabMovie

        if self.ACTIONS.has_key(key):
            self.ACTIONS[key][0]()
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def Calibrate(self, event=None):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        if len(self.polyPoints) > 2:
            print 'You need only two points for calibration. I am going to use the first two'

        if len(self.polyPoints) > 1:
            pt1, pt2 = self.polyPoints[0], self.polyPoints[1]
            r = self.mon.calibrate(pt1, pt2)
            self.polyPoints = []
        else:
            print 'You need at least two points for calibration.'

        print '%spixels = 1cm' % r
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def AutoMask(self, event=None):                                                 # TODO: replace with my maskmaker
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        if len(self.polyPoints > 1):
            pt1, pt2 = self.polyPoints[0], self.polyPoints[1]
            self.mon.autoMask(pt1, pt2)
        else:
            print 'Too few points to automask'
        self.polyPoints = []
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def SaveMask(self, event=None):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        self.mon.saveROIS()
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def setMonitor(self, camera, resolution=None):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """

        if not resolution: resolution = self.size

        self.camera = camera
        self.resolution = resolution
        self.mon = cmn.Monitor()

        frame = cv.CreateMat(self.size[1], self.size[0], cv.CV_8UC3)
        self.bmp = wx.BitmapFromBuffer(self.size[0], self.size[1], frame.tostring())

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.playTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onNextFrame)
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')


    def paintImg(self, img):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        if img:
            depth, channels = img.depth, img.nChannels
            datatype = cv.CV_MAKETYPE(depth, channels)

            frame = cv.CreateMat(self.size[1], self.size[0], datatype)
            cv.Resize(img, frame)

            cv.CvtColor(frame, frame, cv.CV_BGR2RGB)
            #cv.CvtColor(frame, frame, cv.CV_GRAY2RGB)

            self.bmp.CopyFromBuffer(frame.tostring())
            self.Refresh()

        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def onPaint(self, evt):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        if self.bmp:
            dc = wx.BufferedPaintDC(self)
            #self.PrepareDC(dc)
            dc.DrawBitmap(self.bmp, 0, 0, True)
        evt.Skip()
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def onNextFrame(self, evt):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        img = self.mon.GetImage(drawROIs = self.drawROI, selection=self.selection, crosses=self.polyPoints, timestamp=self.timestamp)
        self.paintImg( img )
        if evt: evt.Skip()
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def Play(self, status=True, showROIs=True):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """

        if self.camera is not None and self.resolution is not None and not self.mon.hasSource():
            self.mon.setSource(self.camera, self.resolution)

        if self.mon:
            self.drawROI = showROIs
            self.isPlaying = status

            if status:
                self.playTimer.Start(self.interval)
            else:
                self.playTimer.Stop()
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def Stop(self):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        self.Play(False)
        self.mon.close()
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

    def hasMonitor(self):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        a = (self.mon is not None)
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')
        return a

"""
class monitorPanel(singleVideoImage):
    """"""
    A preview Panel to be used as thumbnail or full-size to show video
    """"""
    def __init__( parent, mon_name, fps, size, cfg):               # monitor_number is 1-indexed
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug

        singleVideoImage.__init__(self, parent, mon_name, fps, size, cfg)

        self.cfg = cfg
        self.config_obj = self.cfg.config_obj
        self.configDict = self.cfg.configDict
        self.full_filename = self.cfg.full_filename

        self.mon_num = mon_num
        self.size = size                   #  TODO: what if this is the Mask Maker panel?
        self.allowEditing = False

        self.displayNumber()

        self.Bind(wx.EVT_LEFT_UP, self.onLeftClick)

        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                Show Monitor Numbers
    def displayNumber(self):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """"""
        Displays the monitor number over top of the thumbnail
        """"""
        # font type: wx.DEFAULT, wx.DECORATIVE, wx.ROMAN, wx.SCRIPT, wx.SWISS, wx.MODERN
        # slant: wx.NORMAL, wx.SLANT or wx.ITALIC
        # weight: wx.NORMAL, wx.LIGHT or wx.BOLD
        # font1 = wx.Font(10, wx.SWISS, wx.ITALIC, wx.NORMAL)
        # use additional fonts this way ...
        pos = int(self.size[0]/2 - 20), int(self.size[1]/2 - 20),
        font1 = wx.Font(35, wx.SWISS, wx.NORMAL, wx.NORMAL)
        text1 = wx.StaticText( self, wx.ID_ANY, '%s' % (self.mon_num), pos)
        text1.SetFont(font1)

        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        Left Click
    def onLeftClick(self, evt):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """"""
        Event handler for thumbnail being clicked on
        Send signal around that the thumbnail was clicked
        """"""
        event = ThumbnailClickedEvt(self.GetId())

        event.id = self.GetId()
        event.number = self.mon_num
        event.thumbnail = self

        self.GetEventHandler().ProcessEvent(event)
        
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

"""
# ------------------------------------------------------------------------------------------- configuration panel

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Panel Configuration
class configPanel(wx.Panel):
    """
    The lower half of panel one with the configuration settings
    """
    def __init__(self, parent, mon_num, cfg):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug

        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(-1,300),
            style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)

        self.cfg = cfg
        self.config_obj = self.cfg.config_obj
        self.configDict = self.cfg.configDict
        self.full_filename = self.cfg.full_filename
        self.mon_num = mon_num
        self.mon_name = 'Monitor%d' % mon_num

        self.parent = parent

        lowerSizer = wx.BoxSizer(wx.HORIZONTAL)
            # has lowLeftSizer, lowRightSizer
# ------------------------------------------------------------------------------------Low Left Sizer
        lowLeftSizer = wx.BoxSizer(wx.VERTICAL)
        # has savebtn, monitor select combobox, play & stop btns, current source, monButtonSizer, sourceSelectGrid,
        # applybtn

    # ---------------------------------------------------------------------------  Monitor selection
    # monitor selection combobox
        # Select Monitor Sizer named section
        self.sb_selectmonitor = wx.StaticBox(self, wx.ID_ANY, 'Select Monitor')
        sbSizer_selectmonitor = wx.StaticBoxSizer(self.sb_selectmonitor, wx.VERTICAL)

        if self.configDict['Options, monitors'] >0 :                        # there are monitors in the config file
            n_mons = self.configDict['Options, monitors']                   # how many?
            self.monitorList = ['Monitor %s' % (int(m)) for m in range( 1, n_mons+1 )]    # make list

            self.source = self.configDict['Monitor1, source']
            self.currentSource = wx.TextCtrl (self, wx.ID_ANY, os.path.split(self.source)[1],
                                              style=wx.TE_READONLY | wx.EXPAND)    # get current source

        else:
            self.monitorList = ['Monitor 1']                                # if there are no monitors in the config
            # file, create an empty monitor 1
            self.currentSource = wx.TextCtrl (self, wx.ID_ANY, 'No source selected', style=wx.TE_READONLY | wx.EXPAND)

        self.monitor_names = wx.ComboBox(self, wx.ID_ANY, choices=self.monitorList,
                                         style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.monitor_names.Selection = self.mon_num -1
        self.Bind ( wx.EVT_COMBOBOX, self.onChangingMonitor, self.monitor_names)

    # Monitor comboxbox & control buttons
        btnSizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        self.btnPlay = wx.Button( self, wx.ID_FORWARD, label="Play")
        self.Bind(wx.EVT_BUTTON, self.onPlay, self.btnPlay)
        self.btnStop = wx.Button( self, wx.ID_STOP, label="Stop")
        self.Bind(wx.EVT_BUTTON, self.onStop, self.btnStop)
        self.btnSave = wx.Button( self, wx.ID_ANY, label='Save')
        self.Bind(wx.EVT_BUTTON, self.cfg.onFileSaveAs, self.btnSave)                   # TODO: this should only save one monitor, not all

        self.btnPlay.Enable(False); self.btnStop.Enable(False)

        # enable buttons
        if self.currentSource != '':
            self.btnPlay.Enable(True)
            self.btnSave.Enable(True)

        btnSizer_1.Add ( self.monitor_names, 2, wx.EXPAND | wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        btnSizer_1.Add ( self.btnPlay , 1, wx.ALIGN_LEFT|wx.ALL, 5 )
        btnSizer_1.Add ( self.btnStop , 1, wx.ALIGN_CENTER|wx.ALL, 5 )
        btnSizer_1.Add (self.btnSave, 1, wx.ALIGN_RIGHT | wx.ALL, 5 )

        sbSizer_selectmonitor.Add (btnSizer_1, 0, wx.EXPAND|wx.ALIGN_BOTTOM|wx.TOP, 5 )
        sbSizer_selectmonitor.Add(self.currentSource, 0, wx.EXPAND | wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        lowLeftSizer.Add (sbSizer_selectmonitor, 0, wx.EXPAND|wx.ALL, 5)

        lowLeftSizer.AddSpacer(20)
    # -------------------------------------------------------------------------------------  Video Input Selection
        # Select source Sizer named section
        sb_videofile = wx.StaticBox(self, wx.ID_ANY, "Select Video input")
        sbSizer_videofile = wx.StaticBoxSizer(sb_videofile, wx.VERTICAL)

        sourceGridSizer = wx.FlexGridSizer(0, 2, 0, 0)

        self.rb1 = wx.RadioButton(self, wx.ID_ANY, 'Camera', style=wx.RB_GROUP)          # select camera source
        self.n_cams = self.configDict['Options, webcams']
        self.WebcamsList = ['Webcam %s' % (int(w) + 1) for w in range(self.n_cams)]
        self.source1 = wx.ComboBox(self, wx.ID_ANY, choices=self.WebcamsList,
                              style= wx.EXPAND | wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind(wx.EVT_COMBOBOX, self.sourceCallback, self.source1)

        self.rb2 = wx.RadioButton(self, wx.ID_ANY, 'File')                               # select video file source
        self.source2 = FileBrowseButton(self, id = wx.ID_ANY,
                                labelText = '', buttonText = 'Browse',
                                toolTip = 'Type filename or click browse to choose video file',
                                dialogTitle = 'Choose a video file',
                                startDirectory = os.path.split(self.configDict[self.mon_name + ', source'])[0],
                                initialValue = os.path.split(self.source)[1],
                                fileMask = '*.*', fileMode = wx.ALL,
                                changeCallback=self.sourceCallback, name = 'videoBrowseButton'  )

        # select folder                                                 TODO: what does select folder do?
#        self.rb3 = wx.RadioButton(self, wx.ID_ANY, 'Folder')
        #                                                               TODO: does this start in right directory?
#        self.source3 = DirBrowseButton(self, style=wx.DD_DIR_MUST_EXIST, labelText='Source 3',
#                                  changeCallback=self.sourceCallback)

        self.controls = []
        self.controls.append((self.rb1, self.source1))
        self.controls.append((self.rb2, self.source2))
#        self.controls.append((self.rb3, self.source3))

        for radio, source in self.controls:
            sourceGridSizer.Add(radio, wx.ID_ANY, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
            sourceGridSizer.Add(source, 2, wx.EXPAND | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
            self.Bind(wx.EVT_RADIOBUTTON, self.onChangeSource, radio)
            self.Bind(wx.EVT_TEXT, self.onChangeSource, source)
#            self.source.Enable(False)

        self.controls[0][1].Enable(True)                    # TODO: only enable buttons for radio that is true

        sbSizer_videofile.Add(sourceGridSizer, 0, wx.EXPAND | wx.ALIGN_CENTER, 5)

        # ------------------------------------------------------------------------  apply button
        self.applyButton = wx.Button( self, wx.ID_APPLY)
        self.applyButton.SetToolTip(wx.ToolTip("Apply to Monitor"))
        self.Bind(wx.EVT_BUTTON, self.onApplySource, self.applyButton)

        sbSizer_videofile.Add(self.applyButton, 0,wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2 )

        lowLeftSizer.Add(sbSizer_videofile, 0, wx.EXPAND|wx.BOTTOM|wx.ALL, 5)

        sbSizer_videofile.AddSpacer(10)

        lowerSizer.Add(lowLeftSizer, 0, wx.EXPAND|wx.ALL, 5)
# ---------------------------------------------------------------------------------Low Right Sizer
        lowRightSizer = wx.BoxSizer(wx.VERTICAL)
        # has lowRightTop and lowRightBottom

# ---------------------------------------------------------------------------------Low Right Top Sizer
        lowRightTopSizer = wx.BoxSizer(wx.HORIZONTAL)
        # has time controls and tracking options
        # ---------------------------------------------------------------------  datetime sizer
        # Select date time named section
        sb_datetime = wx.StaticBox(self, wx.ID_ANY, "Video Start Date and Time")
        date_time_sizer = wx.StaticBoxSizer (sb_datetime, wx.VERTICAL)

        # Date
        dateSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_date = wx.StaticText(self, wx.ID_ANY, "Date:")
        self.start_date = wx.DatePickerCtrl(self, wx.ID_ANY, style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.Bind(wx.EVT_DATE_CHANGED, self.onDateTimeChanged, self.start_date)                                                                            # $$$$$$ - set default date to start_datetime

        dateSizer.Add(self.txt_date, 0, wx.ALL, 5)
        dateSizer.Add(self.start_date, 0, wx.ALL, 5)

        date_time_sizer.Add(dateSizer, 0, wx.ALL, 5)

        # time
        self.txt_time = wx.StaticText(self, wx.ID_ANY, "Time (24-hour format):")
        self.spinbtn = wx.SpinButton(self, wx.ID_ANY, wx.DefaultPosition, (-1, 20), wx.SP_VERTICAL)
        self.start_time = masked.TimeCtrl(self, wx.ID_ANY, name='time: \n24 hour control', fmt24hr=True, spinButton=self.spinbtn)
        self.Bind(masked.EVT_TIMEUPDATE, self.onDateTimeChanged, self.start_time)                                                                            # $$$$$$ - set default date to start_datetime

        self.addWidgets(date_time_sizer, [self.txt_time, self.start_time, self.spinbtn])

        # fps
        fpsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fpsTxt = wx.StaticText(self, wx.ID_ANY, 'Speed in frames per second:')
        self.fps = self.configDict['Options, fps_preview']
        self.fps = wx.TextCtrl(self, 0, style=wx.EXPAND | wx.ALIGN_RIGHT, size=(50, -1), value=str(self.fps))          # get current source
        fpsSizer.Add(self.fpsTxt, 0, wx. wx.EXPAND | wx.ALL, 2)
        fpsSizer.Add(self.fps, 0, wx.EXPAND | wx.ALL, 2)

        date_time_sizer.Add(fpsSizer, 0, wx.EXPAND | wx.ALL, 5)

        lowRightTopSizer.Add(date_time_sizer, 0, wx.EXPAND | wx.TOP | wx.ALL, 5)

        lowRightTopSizer.AddSpacer(5)
        # ----------------------------------------------------------------------------- Static box   TRACKING OPTIONS
        sb_track_txt = wx.StaticBox(self, wx.ID_ANY, "Set Tracking Parameters")
        sbSizer_trackoptions = wx.StaticBoxSizer (sb_track_txt, wx.VERTICAL)


        #  tracking options
        sbSizer_trackactive = wx.BoxSizer (wx.HORIZONTAL)

        self.track = wx.CheckBox(self, wx.ID_ANY, 'Activate Tracking')
        self.track.SetValue(False)
        self.track.Bind ( wx.EVT_CHECKBOX, self.ontrack)

        sbSizer_trackactive.Add (self.track, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        self.isSDMonitor = wx.CheckBox(self, wx.ID_ANY, 'Sleep Deprivation Monitor')
        self.isSDMonitor.SetValue(False)
        self.isSDMonitor.Bind ( wx.EVT_CHECKBOX, self.onSDMonitor)
        self.isSDMonitor.Enable(False)

        sbSizer_trackactive.Add (self.isSDMonitor, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        sbSizer_trackoptions.Add ( sbSizer_trackactive , 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        sbSizer_trackoptions.AddSpacer(10)

        # ------------------------------------------------------------------------------ fly activity options
        sb_calcbox = wx.StaticBox( self, wx.ID_ANY, 'Calculate fly activity as...')
        calcbox_sizer = wx.StaticBoxSizer(sb_calcbox, wx.VERTICAL)

        self.trackDistance = wx.RadioButton(self, wx.ID_ANY, 'Activity as distance traveled', style=wx.RB_GROUP)
        self.trackVirtualBM = wx.RadioButton(self, wx.ID_ANY, 'Activity as midline crossings count')
        self.trackPosition = wx.RadioButton(self, wx.ID_ANY, 'Only position of flies')
                                                                                             # add to right panel lower sizer
        calcbox_sizer.Add (self.trackDistance, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
        calcbox_sizer.Add (self.trackVirtualBM, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
        calcbox_sizer.Add (self.trackPosition, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )

        sbSizer_trackoptions.Add (calcbox_sizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        lowRightTopSizer.Add(sbSizer_trackoptions, wx.ID_ANY, wx.EXPAND|wx.ALL, 5)       # ---- add to lowRightTopSizer

        lowRightSizer.Add(lowRightTopSizer, 1, wx.ALIGN_BOTTOM | wx.EXPAND | wx.ALL, 5)
# ---------------------------------------------------------------------------------  Low Right Bottom Sizer

        sb_mask_txt = wx.StaticBox(self, wx.ID_ANY, "Select Mask File")
        lowRightBottomSizer = wx.StaticBoxSizer (sb_mask_txt, wx.HORIZONTAL)

        # choose mask file
        wildcard = 'PySolo Video mask file (*.msk)|*.msk|' \
                   'All files (*.*)|*.*'                # adding space in here will mess it up!
        self.pickMaskBrowser = FileBrowseButton(self,id =  wx.ID_ANY,
                                        labelText = 'Select Mask File:', buttonText = 'Browse',
                                        toolTip = 'Type filename or click browse to choose mask file',
                                        dialogTitle = 'Choose a mask file',
                                        startDirectory = os.path.split(self.configDict[self.mon_name + ', maskfile'])[0],
                                        initialValue = os.path.split(self.source)[1][0:-4] + '.msk',
                                        fileMask = wildcard, fileMode = wx.ALL,
                                        changeCallback = None,
                                        name = 'maskBrowseButton')


        lowRightBottomSizer.Add ( self.pickMaskBrowser , wx.EXPAND | wx.TOP | wx.ALL, 5 )
        # add to right panel lower sizer

        lowRightSizer.Add(lowRightBottomSizer, 1, wx.ALIGN_BOTTOM | wx.EXPAND | wx.ALL, 5)

        lowerSizer.Add(lowRightSizer, 2, wx.ALIGN_BOTTOM | wx.EXPAND | wx.ALL, 5)

        self.SetSizer(lowerSizer)


        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

    # %%                                                        Save file as
    """
    def onFileSaveAs(self, event):
        if  cmn.call_tracking: cmn.debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """"""
        Opens the save file window
        """"""
        filename = cmn.DEFAULT_CONFIG  # see pvg_common.py
        print("$$$$$$ pvg_panel_one; default_config = ", filename)

        # set file types for find dialog
        wildcard = "PySolo Video config file (*.cfg)|*.cfg|" \
                   "All files (*.*)|*.*"  # adding space in here will mess it up!

        dlg = wx.FileDialog(  # make a save window
            self, message="Save file as ...", defaultDir=cmn.data_dir,
            defaultFile=filename, wildcard=wildcard,
            style=(wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        )

        if dlg.ShowModal() == wx.ID_OK:  # show the save window
            path = dlg.GetPath()  # gets the path from the save dialog
            options.Save(filename=path)

        dlg.Destroy()
        if  cmn.call_tracking: cmn.debugprt(self, currentframe(), pgm, 'end   ')
    """

    #----------------------------------------------------------------------  used for datetime widgets
    def addWidgets(self, mainSizer ,widgets):
        """
        """
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for widget in widgets:
            if isinstance(widget, wx.StaticText):
                sizer.Add(widget, 0, wx.ALL|wx.CENTER, 5),
            else:
                sizer.Add(widget, 0, wx.ALL, 5)
        mainSizer.Add(sizer)

# %%                                                     Input source
    def __getSource(self):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        check which source is ticked and what is the associated value
        Returns the selected source type and its value
        """

        for (r, s), st in zip(self.controls,range(3)):
            if r.GetValue():
                source = s.GetValue()
                sourceType = st
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

        return source, sourceType

# %%                                                Input tracking type
    def __getTrackingType(self):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        return which type of tracking we are chosing
        ['DISTANCE','VBS','XY_COORDS']
        """
        if self.trackDistanceRadio.GetValue(): trackType = 0  #  'DISTANCE'
        elif self.trackVirtualBM.GetValue(): trackType = 1    #  'VBS'
        elif self.trackPosition.GetValue(): trackType = 2     #  'XY_COORDS'

        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')
        return trackType                                                        # $$$$$$ this isn't getting written to config file correctly

# %%                                                            play button
    def onPlay (self, mon_num, event=None):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        # Event handler for the play button
        """
        self.videoPanelList.Play()
        self.btnStop.Enable(True)

        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                            Stop Button
    def onStop (self, event=None):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Event handler for the stop button
        """
        if self.thumbnail and self.thumbnail.isPlaying:
            self.thumbnail.Stop()
            self.btnStop.Enable(False)
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                    Click Thumbnail
    def onThumbnailClicked(self, evt):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Picking thumbnail by clicking on it
        Event handler for changing monitor via clicking on thumbnail
        """
        self.mon_num = evt.number 
        self.current_thumbnail = evt.thumbnail
        self.thumbnailnumber.SetValue(self.MonitorList[self.monitor_number])
        self.updateThumbnail(self.mon_num)

        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')


# %%                                                    Monitor dropdown box
    def onChangingMonitor(self, evt):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Picking thumbnail by using the dropbox
        Event handler for changing monitor via dropdown box
        """
        self.mon_num = evt.EventObject.Selection +1  # EventObject is 0-indexed
        self.updateLowerPanel(self.mon_num)

        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                            Refresh thumbnail and controls
    def updateLowerPanel(self, mon_num):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Updates the lower panel controls with selected monitor info
        """
        # If monitor exists, get info. Else, set to null/default values.
        self.mon_name = 'Monitor%d' % mon_num
        if self.config_obj.has_section(self.mon_name):

        # update monitor selection
            self.sourceType =               (self, self.configDict[self.mon_name + ', sourcetype'])
            self.source =                   (self, self.configDict[self.mon_name + ', source'])
            try:
                text = os.path.split(str(self.source))[1]
            except:
                text = "No Source Selected"
            self.currentSource.SetValue(text)

        # update Video Selection
            for radio, src in self.controls:
                src.Enable(False)
#                src.SetPath('')

            radio, src = self.controls[self.sourceType]
            radio.SetValue(True)
            src.Enable(True)
            src.SetValue(self.source)

        # update date time
            self.start_datetime =           (self.configDict[self.mon_name + ', start_datetime'] )
            self.start_date.SetValue        (self, self.start_datetime.Date())
            self.start_date.SetValue        (self, self.start_datetime.Time())

        # update tracking parameters
            self.pickMaskBrowser.SetPath   (self, self.configDict[self.mon_name + ', maskfile'])

            self.isSDMonitor.SetValue       (self, self.configDict[self.mon_name + ', issdmonitor'])

            self.track.SetValue             (self, self.configDict[self.mon_name + ', track'])
            self.trackType =                (self, self.configDict[self.mon_name + ', tracktype'])
            self.trackDistance.SetValue     (self, False)       # set all 3 to False, then change one to true
            self.trackVirtualBM.SetValue    (self, False)
            self.trackPosition.SetValue     (self, False)
            if self.trackType == 0:
                self.trackDistance.SetValue (self, True)
            elif self.trackType == 1:
                self.trackVirtualBM.SetValue(self, True)
            elif self.trackType == 2:
                self.trackPosition.SetValue (self, True)


        # enabled buttons
            active = self.config_obj.has_section(self.mon_name)
            self.applyButton.Enable ( active )
            self.btnPlay.Enable ( active )
            self.btnStop.Enable ( not active )



# %%
    def sourceCallback (self, event):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        self.applyButton.Enable(True)
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        Radio buttons
    def onChangeSource(self, event):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        # Determine which radio button was selected
        radio_selected = event.GetEventObject()

        # Enable the selected source, disable all others
        for radio, source in self.controls:
            if radio is radio_selected:
                source.Enable(True)
            else:
                source.Enable(False)

        self.applyButton.Enable(True)
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                    Apply Button
    def onApplySource(self, event):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Get source filename from the user's selections
        Event handler for the Apply button on the lower left of panel one
        """

        # update the current source value in the monitor selection box
        if self.rb1.GetValue():
            self.currentSource.SetValue(self.source1.GetValue())
        elif self.rb2.GetValue():
            self.currentSource.SetValue(self.source2.textControl.Value)
#        elif self.rb3:
#            self.currentSource.SetValue(self.source3)

        # Enable buttons
        self.btnPlay.Enable(True)
        self.track.Enable(True)
        self.pickMaskBrowser.Enable(True)

        self.cfg.save_Config(new=False)

        self.setMonitor(self.source, self.size)


        if  cmn.call_tracking: cmn.debugprt(self, currentframe(),pgm,'end   ')

    def onDateTimeChanged(self,event):
        date_wx = self.start_date.GetValue()
        date_py = datetime.date(*map(int, date_wx.FormatISODate().split('-')))
        time_wx = self.start_time.GetValue(self)
        time_py = datetime.time(*map(int, time_wx.FormatISOTime().split(':')))
        self.start_datetime = datetime.datetime.combine(date_py, time_py)

        # %%                                                Save Monitor Config

        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        Activate Tracking
    def ontrack(self, event):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        if self.thumbnail:
            self.thumbnail.track = event.IsChecked()
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%
    def onSDMonitor(self, event):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        if self.thumbnail:
            self.thumbnail.mon.isSDMonitor = event.IsChecked()
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                Update monitor dropdown box
    def updateMonitorList(self, now):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Updates the dropdown box of monitors on lower half of panel one
        """
        # Generate new list of monitors
        self.MonitorList = ['Monitor %d' % m for m in range(now)]

        # Create a new combobox with the correct number of monitors
        self.thumbnailnumber = wx.ComboBox(self, wx.ID_ANY,
            choices=self.MonitorList, style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind (wx.EVT_COMBOBOX, self.onChangingMonitor, self.thumbnailnumber)

        # Remove the old combobox and replace it with this new one
        self.sbSizer_selectmonitor.Hide(0)
        self.sbSizer_selectmonitor.Remove(0)
        self.sbSizer_selectmonitor.Insert(0, self.thumbnailnumber, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        # Display UI changes
        self.sbSizer_selectmonitor.Layout()
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                Update webcam dropdown box
    def updateWebcams(self, old, now):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Updates the dropdown box of cameras on lower half of panel one
        """
        # Generate the list of webcams
        self.WebcamsList = [ 'Webcam %s' % (int(w) +1) for w in range(new) ]

        # Create a new combobox with correct number of webcams
        source1 = wx.ComboBox(self, wx.ID_ANY, size=(285,-1) , choices = self.WebcamsList,
            style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind(wx.EVT_COMBOBOX, self.sourceCallback, source1)
        source1.Enable(True)

        # Create a new radio button to go with the combobox
        self.controls.remove(self.controls[0])
        rb1 = wx.RadioButton(self, wx.ID_ANY, 'Camera', style=wx.RB_GROUP)
        self.Bind(wx.EVT_RADIOBUTTON, self.onChangeSource, rb1)

        # Add the button and combobox to the controls list
        self.controls.insert(0, (rb1,source1))

        # Remove the old ones from the layout and add the new ones
        sourceGridSizer.Hide(0)
        sourceGridSizer.Remove(0)
        sourceGridSizer.Insert(0, rb1)
        sourceGridSizer.Hide(1)
        sourceGridSizer.Remove(1)
        sourceGridSizer.Insert(1, source1)

        # Show changes to UI
        sourceGridSizer.Layout()
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')


# --------------------------------------------------------------------------------------  Scrollable Thumbnail Panel
class panelOne(wx.Panel):
    """
    Panel number One:  All the thumbnails
    """
    def __init__(self, parent, cfg):                                     # TODO: fix the configDict keys
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug

        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(-1,300),
            style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)

        self.cfg = cfg
        self.config_obj = self.cfg.config_obj
        self.configDict = self.cfg.configDict
        self.full_filename = self.cfg.full_filename
        self.mon_num = 1                                                # opens with monitor 1
        self.parent = parent

        # Create a grid of thumbnails and a configure panel
        self.upperPanel = scrollableGrid(self, cfg)
        self.lowerPanel = configPanel(self, self.mon_num, self.cfg)
        
        # Display elements
        self.panelOneSizer = wx.BoxSizer(wx.VERTICAL)
        self.panelOneSizer.Add(self.upperPanel, 1, wx.EXPAND, 0)
        self.panelOneSizer.Add(self.lowerPanel, 0, wx.EXPAND, 0)
        self.SetSizer(self.panelOneSizer)
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

class scrollableGrid(wx.ScrolledWindow):
    """
    The scrollable grid of monitor thumbnails on upper panel one                      # number in monitors not always there
    """
    def __init__(self, parent, cfg):
        if cmn.call_tracking: cmn.debugprt(self, currentframe(), pgm, 'begin     ')  # debug

        # %%                                                  Set up scrolling window
        self.cfg = cfg
        self.config_obj = self.cfg.config_obj
        self.configDict = self.cfg.configDict
        self.full_filename = self.cfg.full_filename
        size = self.configDict['Options, thumbnailsize']
        fps = self.configDict['Options, fps_preview']
        n_mons = self.configDict['Options, monitors']

        wx.ScrolledWindow.__init__(self, parent, wx.ID_ANY, size=(-1,-1))
        self.SetScrollbars(1, 1, 1, 1)
        self.SetScrollRate(10, 10)

        self.grid_mainSizer = wx.GridSizer(6, 3, 2, 2)          # TODO: adjust based on n_mons

        self.videoPanelList = []
        for mon_num in range(1, n_mons+1):
            self.videoPanelList.append(cmn.blankPanel(self, mon_num, fps, size))
            # the videoPanelList list will be 0-indexed
#            self.videoPanelList[mon_num-1].showThumbnail()                    # TODO:  helpful?
            self.grid_mainSizer.Add(self.videoPanelList[mon_num-1], 0, wx.EXPAND | wx.CENTER| wx.ALL, 0)
            self.SetSizer(self.grid_mainSizer)

        # Set up listener for clicking on thumbnails
        self.Bind(EVT_THUMBNAIL_CLICKED, self.onThumbnailClicked)


    def updateGrid(self):
        # %%                                              Populate the thumbnail grid
        size = self.configDict['Options, thumbnailsize']
        fps = self.configDict['Options, fps_preview']
        n_mons = self.configDict['Options, monitors']
        self.videoPanelList = []
        for mon_num in range(1, n_mons+1):
            self.videoPanelList.append(cmn.singleVideoImage(self, self.cfg, mon_num, fps, size))
            # the videoPanelList list will be 0-indexed
            self.grid_mainSizer.Add(self.videoPanelList[mon_num-1], 0, wx.EXPAND | wx.CENTER| wx.ALL, 0)


        # %%                                              Make elements visible in GUI
        self.SetSizer(self.grid_mainSizer)

        # Set up listener for clicking on thumbnails
        self.Bind(EVT_THUMBNAIL_CLICKED, self.onThumbnailClicked)

        if cmn.call_tracking: cmn.debugprt(self, currentframe(), pgm, 'end   ')

    # %%                                                    Thumbnail Clicked
    def onThumbnailClicked(self, event=None):
        if cmn.call_tracking: cmn.debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Event handler that makes clicking a thumbnail update the dropdown menu
        Relay event to sibling panel
        """
        wx.PostEvent(self.parent.lowerPanel, event)             # relay event to monitor dropdown menu
        event.Skip()

        if cmn.call_tracking: cmn.debugprt(self, currentframe(), pgm, 'end   ')


    """
# %%                                                       Old Update Monitors
    def updateMonitors(self, parent, old, now, size, cfg):
        if cmn.call_tracking: cmn.debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """"""
        Changes number of monitor thumbnails.
        """"""
        diff = old - now
        i = diff
        while i != 0:  # Adding monitors to grid
            if diff < 0:
                i += 1
                # Make a new thumbnail and add to list
                self.videoPanelList.append(cmn.singlevideoimage(self, mon_name, fps, size, cfg))
                # Add thumbnail to layout
                self.grid_mainSizer.Add(self.videoPanelList[old])
                self.grid_mainSizer.Layout()
                old += 1
            elif diff > 0:
                # Removing monitors from grid
                i -= 1
                # Remove last thumbnail from list
                self.videoPanelList.pop(len(self.videoPanelList) - 1)
                # Remove last thumbnail from layout
                self.grid_mainSizer.Hide(old - 1)
                self.grid_mainSizer.Remove(old - 1)
                self.grid_mainSizer.Layout()
                old -= 1

        if cmn.call_tracking: cmn.debugprt(self, currentframe(), pgm, 'end   ')

        # %%                                                    Change Thumbnail size


    def updateThumbs(self, old, new):
        if cmn.call_tracking: cmn.debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        self.ThumbnailSize = new


        #        for i in range(0, self.gridSizer):                                                  # TODO: not working
        #            self.videoPanelList[i].SetThumbnailSize(new)
        #            self.grid_mainSizer.Layout()

    # %%                                                         Stop Playing
    def StopPlaying(self):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        self.lowerPanel.onStop()

        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                            Refresh
    def onRefresh(self):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """"""
        Checks for changes to be made to UI and implements them.
        """"""
        # Check number of monitors
        if self.monitor_number != self.configDict['Options, monitors']:
            self.upperPanel.updateMonitors(self.monitor_number, self.configDict['Options, monitors'])
            self.lowerPanel.updateMonitors(self.monitor_number, self.configDict['Options, monitors'])
            self.monitor_number = self.configDict['Options, monitors']

        # Check thumbnail size
        if self.tn_size != self.configDict['Options, thumbnailsize']:
            self.upperPanel.updateThumbs(self.tn_size, self.configDict['Options, thumbnailsize'])
            self.tn_size = self.configDict['Options, thumbnailsize']

        # Check number of webcams
        if self.n_cams != self.configDict['Options, webcams']:
            self.lowerPanel.updateWebcams(self.n_cams, self.configDict['Options, webcams'])
            self.n_cams = self.configDict['Options, webcams']

        # Show changes to UI
        self.upperPanelSizer.Layout()

        """