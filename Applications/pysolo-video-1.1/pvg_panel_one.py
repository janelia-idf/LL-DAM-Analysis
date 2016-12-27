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
import wx.lib.newevent
import wx.calendar
import wx.lib.masked as masked
import datetime
from inspect import currentframe                                                                     # debug
import pvg_common as cmn

ThumbnailClickedEvt, EVT_THUMBNAIL_CLICKED = wx.lib.newevent.NewCommandEvent()
from wx.lib.filebrowsebutton import FileBrowseButton, DirBrowseButton


"""
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Settings
"""
pgm = 'pvg_panel_one.py'
start_datetime = (2016, 11, 13, 3, 47, 38)

"""
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Thumbnail Panel
"""
class previewPanel(wx.Panel):
    """
    A panel showing the video images.
    Used for thumbnails
    """
    def __init__(self, parent, mon_num,  config_obj, configDict, keymode=True):
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'begin     ')                                            # debug

        wx.Panel.__init__(self, parent, wx.ID_ANY, style=wx.WANTS_CHARS)
        self.config_obj = config_obj
        self.configDict = configDict

        self.parent = parent
        mon_name =  'Monitor%d' % mon_num

        self.size = configDict['Options, thumbnailsize']
#        self.SetMinSize(self.size)
        fps = configDict['Options, fps_preview']
        self.interval = 1000/fps # fps determines refresh interval in ms

        self.SetBackgroundColour('#A9A9A9')

#        self.mon = None
        self.sourceType = configDict[mon_name + ', sourcetype']
        self.source = configDict[mon_name + ', source']
        self.start_datetime = configDict[mon_name + ', start_datetime']           # date & time of start of video
        self.track = configDict[mon_name + ', track']
        self.isSDMonitor = configDict[mon_name + ', issdmonitor']
        self.trackType = configDict[mon_name + ', tracktype']              # distance tracking

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
        if cmn.call_tracking:  cmn.debugprt(self,currentframe(),pgm,'end   ')

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

    def AutoMask(self, event=None):
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


class thumbnailPanel(previewPanel):
    """
    A small preview Panel to be used as thumbnail
    """
    def __init__( self, parent, monitor_number,  config_obj, configDict ):               # monitor_number is 1-indexed
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug

        previewPanel.__init__(self, parent, monitor_number, config_obj, configDict)
        self.config_obj = config_obj
        self.configDict = configDict

        self.mon_num = monitor_number
        self.size = configDict['Options, thumbnailsize']                    #  TODO: what if this is the Mask Maker panel?
        self.allowEditing = False

        self.displayNumber()

        self.Bind(wx.EVT_LEFT_UP, self.onLeftClick)
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                Show Monitor Numbers
    def displayNumber(self):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
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
        text1 = wx.StaticText( self, wx.ID_ANY, '%s' % (self.mon_num), pos)
        text1.SetFont(font1)

        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        Left Click
    def onLeftClick(self, evt):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Event handler for thumbnail being clicked on
        Send signal around that the thumbnail was clicked
        """
        event = ThumbnailClickedEvt(self.GetId())

        event.id = self.GetId()
        event.number = self.mon_num
        event.thumbnail = self

        self.GetEventHandler().ProcessEvent(event)
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')


# ------------------------------------------------------------------------------------------- Panel Grid View
class panelGridView(wx.ScrolledWindow):
    """
    The scrollable grid of monitor thumbnails on panel one                      # number in monitors not always there
    """
    def __init__(self, parent,  config_obj, configDict ):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug

# %%                                                  Set up scrolling window
        wx.ScrolledWindow.__init__(self, parent, wx.ID_ANY, size=(-1,600))
        self.SetScrollbars(1, 1, 1, 1)
        self.SetScrollRate(10, 10)

        self.config_obj = config_obj
        self.configDict = configDict

        self.parent = parent
        n_mons = configDict['Options, monitors']
        self.grid_mainSizer = wx.GridSizer(6,3,2,2)

# %%                                              Populate the thumbnail grid
        self.previewPanels = []
        for mon_num in range(0, n_mons):                                                # counts 0 to n_mons-1 which will match 0-indexed previewPanels list
            self.previewPanels.append ( thumbnailPanel(self, mon_num +1, config_obj, configDict) )
            self.grid_mainSizer.Add(self.previewPanels[mon_num])                      # the previewPanels list will be 0-indexed

# %%                                              Make elements visible in UI
        self.SetSizer(self.grid_mainSizer)
        # Set up listener for clicking on thumbnails
        self.Bind(EVT_THUMBNAIL_CLICKED, self.onThumbnailClicked)
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                    Thumbnail Clicked
    def onThumbnailClicked(self, event):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Event handler that makes clicking a thumbnail update the dropdown menu
        Relay event to sibling panel
        """
        wx.PostEvent(self.parent.lowerPanel, event)
        event.Skip()
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        Update Monitors
    # Should be working
    def updateMonitors(self, old, now, parent, configDict):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Changes number of monitor thumbnails.
        """
        diff = old - now
        i = diff
        while i != 0:                   # Adding monitors to grid
            if diff < 0:
                i += 1
                # Make a new thumbnail and add to list
                self.previewPanels.append ( thumbnailPanel(self, parent, old, configDict) )
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

        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                    Change Thumbnail size
    def updateThumbs(self, old, new):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        self.ThumbnailSize = new


#        for i in range(0, self.gridSizer):                                                  # TODO: not working
#            self.previewPanels[i].SetThumbnailSize(new)
#            self.grid_mainSizer.Layout()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Panel Configuration
class lowerPanel(wx.Panel):
    """
    The lower half of panel one with the configuration settings
    """
    def __init__(self, parent,  config_obj, configDict):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug

        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(-1,300),
            style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)

        self.config_obj = config_obj
        self.configDict = self.configDict

        self.parent = parent

        lowerSizer = wx.BoxSizer(wx.HORIZONTAL)

        # --------------------------------------------------------------------------- Static box   MONITOR SELECTION
        # ---------------------------------------------------------------------------  Monitor selection
        # start up with monitor 1 if it exists
        if configDict['Options, monitors'] >0 :
            n_mons = configDict['Options, monitors']
            self.MonitorList = ['Monitor %s' % (int(m)) for m in range( 1, n_mons )]
            self.currentSource = wx.TextCtrl (self, wx.ID_ANY, configDict['Monitor1, source'], style=wx.TE_READONLY)
        else:
            self.MonitorList = ['Monitor 1']
            self.currentSource = wx.TextCtrl (self, wx.ID_ANY, 'No source selected', style=wx.TE_READONLY)
        self.thumbnailNames = wx.ComboBox(self, wx.ID_ANY, choices=self.MonitorList, style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind ( wx.EVT_COMBOBOX, self.onChangingMonitor, self.thumbnailNames)

    # Select Monitor Sizer
        sb_selectmonitor = wx.StaticBox(self, wx.ID_ANY, 'Select Monitor')
        self.sbSizer_selectmonitor = wx.StaticBoxSizer (sb_selectmonitor, wx.VERTICAL)

        self.sbSizer_selectmonitor.Add ( self.thumbnailNames, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        self.sbSizer_selectmonitor.Add ( self.currentSource, 0, wx.EXPAND|wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    # Monitor control buttons
        btnSizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.btnPlay = wx.Button( self, wx.ID_FORWARD, label="Play")
        self.btnStop = wx.Button( self, wx.ID_STOP, label="Stop")
        self.Bind(wx.EVT_BUTTON, self.onPlay, self.btnPlay)
        self.Bind(wx.EVT_BUTTON, self.onStop, self.btnStop)
        self.btnPlay.Enable(False); self.btnStop.Enable(False)

        btnSizer_1.Add ( self.btnPlay , 0, wx.ALIGN_LEFT|wx.ALL, 5 )
        btnSizer_1.Add ( self.btnStop , 0, wx.ALIGN_CENTER|wx.LEFT|wx.TOP|wx.DOWN, 5 )

        self.sbSizer_selectmonitor.Add ( btnSizer_1, 0, wx.EXPAND|wx.ALIGN_BOTTOM|wx.TOP, 5 )

        lowerSizer.Add (self.sbSizer_selectmonitor, 0, wx.EXPAND|wx.ALL, 5)

    # -------------------------------------------------------------------------------------  Video Input Selection

        sb_videofile = wx.StaticBox(self, wx.ID_ANY, "Select Video input")
        self.sbSizer_videofile = wx.StaticBoxSizer(sb_videofile, wx.VERTICAL)

        self.grid2 = wx.FlexGridSizer(0, 2, 0, 0)

        self.n_cams = configDict['Options, webcams']
        self.WebcamsList = ['Webcam %s' % (int(w) + 1) for w in range(self.n_cams)]

        rb1 = wx.RadioButton(self, wx.ID_ANY, 'Camera', style=wx.RB_GROUP)
        source1 = wx.ComboBox(self, wx.ID_ANY, size=(285, -1), choices=self.WebcamsList,
                              style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind(wx.EVT_COMBOBOX, self.sourceCallback, source1)

        rb2 = wx.RadioButton(self, wx.ID_ANY, 'File')
        source2 = FileBrowseButton(self, -1, labelText='', size=(300, -1), changeCallback=self.sourceCallback)

        rb3 = wx.RadioButton(self, wx.ID_ANY, 'Folder')
        source3 = DirBrowseButton(self, style=wx.DD_DIR_MUST_EXIST, labelText='', size=(300, -1),
                                  changeCallback=self.sourceCallback)

        self.controls = []
        self.controls.append((rb1, source1))
        self.controls.append((rb2, source2))
        self.controls.append((rb3, source3))

        for radio, source in self.controls:
            self.grid2.Add(radio, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
            self.grid2.Add(source, 0, wx.ALIGN_CENTRE | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
            self.Bind(wx.EVT_RADIOBUTTON, self.onChangeSource, radio)
            source.Enable(False)

        self.controls[0][1].Enable(True)
        self.sbSizer_videofile.Add(self.grid2)

        # ------------------------------------------------------------------------  apply button
        self.applyButton = wx.Button( self, wx.ID_APPLY)
        self.applyButton.SetToolTip(wx.ToolTip("Apply to Monitor"))
        self.Bind(wx.EVT_BUTTON, self.onApplySource, self.applyButton)

        self.sbSizer_videofile.Add(self.applyButton, 0, wx.ALIGN_LEFT, 5 )


        # ---------------------------------------------------------------------  date picker
        sb_datetime = wx.StaticBox(self, wx.ID_ANY, "Video Start Date and Time")
        self.date_time_sizer = wx.StaticBoxSizer (sb_datetime, wx.HORIZONTAL)

        self.txt_date = wx.StaticText(self, wx.ID_ANY, "Date:")
        self.start_date = wx.DatePickerCtrl(self, wx.ID_ANY, style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)

        self.Bind(wx.EVT_DATE_CHANGED, self.onDateTimeChanged, self.start_date)                                                                            # $$$$$$ - set default date to start_datetime

        self.date_time_sizer.Add(self.txt_date, 0, wx.ALL, 5)  # --- add to datetime row, center panel, lower sizer
        self.date_time_sizer.Add(self.start_date, 0, wx.ALL, 5)

        # ---------------------------------------------------------------------  time picker
        self.txt_time = wx.StaticText(self, wx.ID_ANY, "Time (24-hour format):")
        self.spinbtn = wx.SpinButton(self, wx.ID_ANY, wx.DefaultPosition, (-1, 20), wx.SP_VERTICAL)
        self.start_time = masked.TimeCtrl(self, wx.ID_ANY, name="24 hour control", fmt24hr=True, spinButton=self.spinbtn)
        self.Bind(masked.EVT_TIMEUPDATE, self.onDateTimeChanged, self.start_time)                                                                            # $$$$$$ - set default date to start_datetime

        self.addWidgets(self.date_time_sizer, [self.txt_time, self.start_time, self.spinbtn])

        self.sbSizer_videofile.AddSpacer(50)
        self.sbSizer_videofile.Add(self.date_time_sizer, 0, wx.EXPAND | wx.ALL, 5)


        lowerSizer.Add(self.sbSizer_videofile, 0, wx.ALIGN_BOTTOM | wx.EXPAND | wx.ALL, 5)  # ---- add to lower sizer


        # ----------------------------------------------------------------------------- Static box   TRACKING OPTIONS
        sb_trackopt = wx.StaticBox(self, wx.ID_ANY, "Set Tracking Parameters")
        sbSizer_trackopt = wx.StaticBoxSizer (sb_trackopt, wx.VERTICAL)

        # --------------------------------------------------------------------------------  choose mask file
        self.pickMaskBrowser = FileBrowseButton(self, wx.ID_ANY, labelText='Mask File')

        sbSizer_trackopt.Add ( self.pickMaskBrowser , 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )           # add to right panel lower sizer

        # ------------------------------------------------------------------------------ tracking options
        sbSizer_trackopt1 = wx.BoxSizer (wx.HORIZONTAL)

        self.activateTracking = wx.CheckBox(self, wx.ID_ANY, "Activate Tracking")
        self.activateTracking.SetValue(False)
        self.activateTracking.Bind ( wx.EVT_CHECKBOX, self.onActivateTracking)

        self.isSDMonitor = wx.CheckBox(self, wx.ID_ANY, "Sleep Deprivation Monitor")
        self.isSDMonitor.SetValue(False)
        self.isSDMonitor.Bind ( wx.EVT_CHECKBOX, self.onSDMonitor)
        self.isSDMonitor.Enable(False)

        sbSizer_trackopt1.Add (self.activateTracking, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        sbSizer_trackopt1.Add (self.isSDMonitor, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        sbSizer_trackopt.Add ( sbSizer_trackopt1 , 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )


        # ------------------------------------------------------------------------------ fly activity options
        # trackingTypeSizer = wx.Sizer(wx.HORIZONTAL)
        self.trackDistanceRadio = wx.RadioButton(self, wx.ID_ANY, "Activity as distance traveled", style=wx.RB_GROUP)
        self.trackVirtualBM = wx.RadioButton(self, wx.ID_ANY, "Activity as midline crossings count")
        self.trackPosition = wx.RadioButton(self, wx.ID_ANY, "Only position of flies")

                                                                                             # add to right panel lower sizer
        sbSizer_trackopt.AddSpacer(10)
        sb_calcbox = wx.StaticBox( self, wx.ID_ANY, "Calculate fly activity as...")
        calcbox_sizer = wx.StaticBoxSizer(sb_calcbox, wx.VERTICAL)

        calcbox_sizer.Add (self.trackDistanceRadio, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
        calcbox_sizer.Add (self.trackVirtualBM, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
        calcbox_sizer.Add (self.trackPosition, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )

        sbSizer_trackopt.Add (calcbox_sizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        self.btnSave = wx.Button( self, wx.ID_ANY, label="Save Configuration")          # save configuration button
        self.Bind(wx.EVT_BUTTON, config_obj.onFileSaveAs, self.btnSave)

        sbSizer_trackopt.Add (self.btnSave, 0, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM |wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        lowerSizer.Add(sbSizer_trackopt, wx.ID_ANY, wx.EXPAND|wx.ALL, 5)                       # ---- add to lower sizer


        self.SetSizer(lowerSizer)
        self.Bind(EVT_THUMBNAIL_CLICKED, self.onThumbnailClicked)

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
    #----------------------------------------------------------------------
    def addWidgets(self, mainSizer ,widgets):
        """"""
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
        if self.trackDistanceRadio.GetValue(): trackType = 0  #  "DISTANCE"
        elif self.trackVirtualBM.GetValue(): trackType = 1    #  "VBS"
        elif self.trackPosition.GetValue(): trackType = 2     #  "XY_COORDS"

        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')
        return trackType                                                        # $$$$$$ this isn't getting written to config file correctly

# %%                                                            play button
    def onPlay (self, event=None):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        # Event handler for the play button
        """

        if self.thumbnail:
            self.thumbnail.Play()
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
    def onThumbnailClicked(self, evt, config_obj, configDict):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Picking thumbnail by clicking on it
        Event handler for changing monitor via clicking on thumbnail
        """
        self.mon_num = evt.number #+ 1
        self.thumbnail = evt.thumbnail
        self.thumbnailNumber.SetValue(self.MonitorList[self.monitor_number])
        self.updateThumbnail(self.mon_num, config_obj, configDict)
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                    Monitor dropdown box
    def onChangingMonitor(self, evt, config_obj, configDict):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Picking thumbnail by using the dropbox
        Event handler for changing monitor via dropdown box
        """
        sel = evt.GetString()
        self.monitor_number = self.MonitorList.index(sel) #+ 1
        self.thumbnail = self.parent.scrollThumbnails.previewPanels[self.monitor_number]         #this is not very elegant
        self.updateThumbnail(self.monitor_number, configDict, config_obj)
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                            Refresh thumbnail and controls
    def updateThumbnail(self, mon_num, config_obj, configDict ):                # TODO:  this should be in Configuration if it isn't already
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Updates the lower panel controls with new thumbnail info
        """
        # If monitor exists, get info. Else, set to null/default values.
        mon_name = 'Monitor%d' % mon_num
        if self.config_obj.has_section(mon_name):
            self.sourceType.setValue(self, configDict[mon_name + ', sourcetype'])
            self.currentSource.setValue(self, configDict[mon_name + ', source'])
            self.start_datetime.setValue(self, configDict[mon_name + ', start_datetime']) # date & time of start of video
            self.start_date.setValue(self, self.start_datetime.Date())
            self.start_date.setValue(self, self.start_datetime.Time())
            self.activateTracking.setValue(self, configDict[mon_name + ', track'])
            self.isSDMonitor.setValue(self, configDict[mon_name + ', issdmonitor'])
            self.trackType.setValue(self, configDict[mon_name + ', tracktype'])  # distance tracking
            self.pickMaskBrowser.setValue(self, configDict[mon_name + ', maskfile'])

            self.trackDistanceRadio.setValue(self, False)
            self.trackVirtualBM.setValue(self, False)
            self.tracktrackPosition.setValue(self, False)
            if configDict[mon_name + ', tracktype'] == 0:
                self.trackDistanceRadio = True
            elif configDict[mon_name + ', tracktype'] == 1:
                self.trackVirtualBM = True
            elif configDict[mon_name + ', tracktype'] == 2:
                self.trackPosition = True

        # If monitor is playing a camera
        if self.sourceType == 0 and self.source != '':
            self.source.setValue = self.WebcamsList[self.source]

        # Ensure source and type match throughout program              TODO:  what's going on with matching source & type throughout program?
        self.thumbnail.source = self.source
        self.thumbnail.sourceType = self.sourceType
        self.thumbnail.track = self.track
        if self.thumbnail.hasMonitor():
            self.isSDMonitor = self.thumbnail.mon.isSDMonitor

        #update first static box
        active = self.thumbnail.hasMonitor()
        self.applyButton.Enable ( active )
        self.btnPlay.Enable ( active )
        self.btnStop.Enable ( active and self.thumbnail.isPlaying )

        text = os.path.split(str(self.source))[1] or "No Source Selected"
        self.currentSource.SetValue( text )

        #update second static box
        for radio, src in self.controls:
            src.Enable(False); src.SetValue('')

        radio, src = self.controls[self.sourceType]
        radio.SetValue(True); src.Enable(True)
        src.SetValue(self.source)

        #update third static box
        self.activateTracking.SetValue(self.thumbnail.track)
        self.isSDMonitor.SetValue(self.isSDMonitor)
        self.pickMaskBrowser.SetValue(self.mask_file or '')
        [self.trackDistanceRadio, self.trackVirtualBM, self.trackPosition][self.trackType].SetValue(True)
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

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
        Get source and mask info from the user's selections
        Event handler for the Apply button on the lower left of panel one
        """
        source, sourceType = self.__getSource()
        track = self.activateTracking.GetValue()
        self.mask_file = self.pickMaskBrowser.GetValue()
        self.trackType = self.__getTrackingType()

        # If there exists a thumbnail
        # Else statement belongs to inner if statement, not sure why it keeps dedenting
        if self.thumbnail:
            if sourceType > 0:
                camera = source # If source is a file, get file
            else:
                camera = self.WebcamsList.index(source) # Otherwise, check webcam list

            # Set the thumbnail's source to the source we have chosen
            # Specify if it is webcam, file, etc
            self.thumbnail.source = camera
            self.thumbnail.sourceType = sourceType

            #Change the source text
            self.currentSource.SetValue( os.path.split(source)[1] )

            #Set thumbnail's monitor
            self.thumbnail.setMonitor(camera)

            #Enable buttons
            self.btnPlay.Enable(True)
            self.activateTracking.Enable(True)
            self.pickMaskBrowser.Enable(True)

            self.saveMonitorConfiguration()
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

    def onDateTimeChanged(self,event):
        date_wx = self.start_date.GetValue()
        date_py = datetime.date(*map(int, date_wx.FormatISODate().split('-')))
        time_wx = self.start_time.GetValue(self)
        time_py = datetime.time(*map(int, time_wx.FormatISOTime().split(':')))
        print("$$$$$$ pvg_panel_one; 593; start date = ", date_wx)
        print("$$$$$$ pvg_panel_one; start time = ", time_py)
        self.start_datetime = datetime.datetime.combine(date_py, time_py)
        print("$$$$$$ pvg_panel_one; start time = ", self.start_datetime)

        # %%                                                Save Monitor Config
    def saveMonitorConfiguration(self):

        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        options.SetMonitor(self.monitor_number,          # monitor_number is 0-indexed
                           self.thumbnail.sourceType,
                           self.thumbnail.source,           #self.thumbnail.source+1 in dev code
                           self.start_datetime,
                           self.thumbnail.track,
                           self.mask_file,
                           self.trackType,                                      # this is not being saved correctly                             self.thumbnail.mon.isSDMonitor
                           )
        print("$$$$$$ pvg_panel_one; 609; saveMonitorConfiguration; mask_file = ", self.mask_file)
        options.Save()
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        Activate Tracking
    def onActivateTracking(self, event):
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
    def updateMonitors(self, old, now):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Updates the dropdown box of monitors on lower half of panel one
        """
        # Generate new list of monitors
        self.MonitorList = ['Monitor %s' % (int(m)) for m in range(now)]

        # Create a new combobox with the correct number of monitors
        self.thumbnailNumber = wx.ComboBox(self, wx.ID_ANY,
            choices=self.MonitorList, style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind (wx.EVT_COMBOBOX, self.onChangingMonitor(config_obj, configDict), self.thumbnailNumber)

        # Remove the old combobox and replace it with this new one
        self.sbSizer_selectmonitor.Hide(0)
        self.sbSizer_selectmonitor.Remove(0)
        self.sbSizer_selectmonitor.Insert(0, self.thumbnailNumber, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP, 5)

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
        self.grid2.Hide(0)
        self.grid2.Remove(0)
        self.grid2.Insert(0, rb1)
        self.grid2.Hide(1)
        self.grid2.Remove(1)
        self.grid2.Insert(1, source1)

        # Show changes to UI
        self.grid2.Layout()
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')


# --------------------------------------------------------------------------------------  Thumbnail Panel
class panelOne(wx.Panel):
    """
    Panel number One:  All the thumbnails
    """
    def __init__(self, parent,  config_obj, configDict):                                     # TODO: fix the configDict keys
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug

        wx.Panel.__init__(self, parent)
        self.config_obj = config_obj
        self.configDict = configDict

        # Create a grid of thumbnails and a configure panel

        self.scrollThumbnails = panelGridView(self, configDict)
        self.lowerPanel = lowerPanel(self, config_obj, configDict)
        # Display elements
        self.PanelOneSizer = wx.BoxSizer(wx.VERTICAL)
        self.PanelOneSizer.Add(self.scrollThumbnails, 1, wx.EXPAND, 0)
        self.PanelOneSizer.Add(self.lowerPanel, 0, wx.EXPAND, 0)
        self.SetSizer(self.PanelOneSizer)
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                         Stop Playing
    def StopPlaying(self):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        self.lowerPanel.onStop()

        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                            Refresh
    def onRefresh(self):
        if  cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """ 
        Checks for changes to be made to UI and implements them.
        """
        # Check number of monitors
        if self.monitor_number != configDict['Options, monitors']:
            self.scrollThumbnails.updateMonitors(self.monitor_number, configDict['Options, monitors'])
            self.lowerPanel.updateMonitors(self.monitor_number, configDict['Options, monitors'])
            self.monitor_number = configDict['Options, monitors']

        # Check thumbnail size
        if self.tn_size != configDict['Options, thumbnailsize']:
            self.scrollThumbnails.updateThumbs(self.tn_size, configDict['Options, thumbnailsize'])
            self.tn_size = configDict['Options, thumbnailsize']

        # Check number of webcams
        if self.n_cams != configDict['Options, webcams']:
            self.lowerPanel.updateWebcams(self.n_cams, configDict['Options, webcams'])
            self.n_cams = configDict['Options, webcams']

        # Show changes to UI
        self.PanelOneSizer.Layout()

