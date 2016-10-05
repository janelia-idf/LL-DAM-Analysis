# -*- coding: utf-8 -*-
#
#       pvg_common.py
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

import inspect
import wx, cv, os
import pysolovideo as pv
import ConfigParser, threading

DEFAULT_CONFIG = 'pysolo_video'

class myConfig():
    """
    Handles program configuration
    Uses ConfigParser to store and retrieve
    From gg's toolbox
    """
    def __init__(self, filename=None, temporary=False, defaultOptions=None):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        filename    the name of the configuration file
        temporary   whether we are reading and storing values temporarily
        defaultOptions  a dict containing the defaultOptions
        """

        filename = filename or DEFAULT_CONFIG
        pDir = os.getcwd()
        if not os.access(pDir, os.W_OK): pDir = os.environ['HOME']
        print(pDir + filename)
        self.filename = os.path.join (pDir, filename)
        self.filename_temp = '%s~' % self.filename

        self.config = None

        if defaultOptions != None:
            self.defaultOptions = defaultOptions
        else:
            self.defaultOptions = { "option_1" : [0, "Description"],
                                    }

        self.Read(temporary)

    def New(self, filename):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        self.filename = filename
        self.Read()

    def Read(self, temporary=False):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        read the configuration file. Initiate one if does not exist

        temporary       True                Read the temporary file instead
                        False  (Default)     Read the actual file
        """

        if temporary: filename = self.filename_temp
        else: filename = self.filename

        if os.path.exists(filename):
            self.config = ConfigParser.RawConfigParser()
            self.config.read(filename)

        else:
            self.Save(temporary, newfile=True)


    def Save(self, temporary=False, newfile=False, filename=None):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """

        if temporary and not filename: filename = self.filename_temp
        elif not temporary and not filename: filename = self.filename

        if newfile:
            self.config = ConfigParser.RawConfigParser()
            self.config.add_section('Options')

            for key in self.defaultOptions:
                self.config.set('Options', key, self.defaultOptions[key][0])

        with open(filename, 'wb') as configfile:
            self.config.write(configfile)

        if not temporary: self.Save(temporary=True)


    def SetValue(self, section, key, value):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """

        if not self.config.has_section(section):
            self.config.add_section(section)

        self.config.set(section, key, value)

    def GetValue(self, section, key):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        get value from config file
        Does some sanity checking to return tuple, integer and strings
        as required.
        """
        r = self.config.get(section, key)

        if type(r) == type(0) or type(r) == type(1.0): #native int and float
            return r
        elif type(r) == type(True): #native boolean
            return r
        elif type(r) == type(''):
            r = r.split(',')

        if len(r) == 2: #tuple
            r = tuple([int(i) for i in r]) # tuple

        elif len(r) < 2: #string or integer
            try:
                r = int(r[0]) #int as text
            except:
                if len(r) > 0:
                    r = r[0] #string
                else:
                    r = ""

        if r == 'False' or r == 'True':
            r = (r == 'True') #bool

        return r


    def GetOption(self, key):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        return self.GetValue('Options', key)

class acquireObject():
    def __init__(self, monitor, source, resolution, mask_file, track, track_type, dataFolder):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        self.monitor = monitor
        self.keepGoing = False
        self.verbose = True                                                        # false turns off debug
        self.track = track
        dataFolder = options.GetOption("Data_Folder")
        outputFile = os.path.join(dataFolder, 'Monitor%02d.txt' % monitor)

        self.mon = pv.Monitor()
        self.mon.setSource(source, resolution)
        self.mon.setTracking(True, track_type, mask_file, outputFile)

        if self.verbose: print ( "Verbose - Setting monitor %s with source %s and mask %s. Output to %s " % (monitor, source, os.path.split(mask_file)[1], os.path.split(outputFile)[1] ) )

    def run(self, kbdint=False):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        while self.keepGoing:
            self.mon.GetImage()

    def start(self):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        self.keepGoing = True
        self.run()

    def halt(self):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        self.keepGoing = False
        if self.verbose: print ( "Verbose: Stopping capture" )




class acquireThread(threading.Thread):

    def __init__(self, monitor, source, resolution, mask_file, track, track_type, dataFolder):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        threading.Thread.__init__(self)
        self.monitor = monitor
        self.keepGoing = False
        self.verbose = True
        self.track = track
        outputFile = os.path.join(dataFolder, 'Monitor%02d.txt' % monitor)

        self.mon = pv.Monitor()
        self.mon.setSource(source, resolution)
        self.mon.setTracking(True, track_type, mask_file, outputFile)

        if self.verbose: print ( "Verbose2: Setting monitor %s with source %s and mask %s. Output to %s " % (monitor, source, os.path.split(mask_file)[1], os.path.split(outputFile)[1] ) )

    def run(self, kbdint=False):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """

        if kbdint:

            while self.keepGoing:
                try:
                    self.mon.GetImage()
                except KeyboardInterrupt:
                    self.halt()

        else:
            while self.keepGoing:
                self.mon.GetImage()

    def doTrack(self):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        self.keepGoing = True
        self.start()

    def halt(self):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        self.keepGoing = False
        if self.verbose: print ( "Verbose3: Stopping capture" )

class pvg_config(myConfig):
    """
    Inheriting from myConfig
    """
    def __init__(self, filename=None, temporary=False):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
#        print(' inspect not working in pvg_config __init__')                                   # debug

        defaultOptions = { "Monitors" : [9, "Select the number of monitors connected to this machine"],
                            "Webcams"  : [1, "Select the number of webcams connected to this machine"],
                            "ThumbnailSize" : ['320, 240', "Specify the size for the thumbnail previews"],
                            "FullSize" : ['640, 480', "Specify the size for the actual acquisition from the webcams.\nMake sure your webcam supports this definition"],
                            "FPS_preview" : [5, "Refresh frequency (FPS) of the thumbnails during preview.\nSelect a low rate for slow computers"],
                            "FPS_recording" : [5, "Actual refresh rate (FPS) during acquisition and processing"],
                            "Data_Folder" : ['', "Folder where the final data are saved"]
                           }

        self.monitorProperties = ['sourceType', 'source', 'track', 'maskfile', 'trackType', 'isSDMonitor']
#        print(self.monitorProperties)

        myConfig.__init__(self, filename, temporary, defaultOptions)

    def SetMonitor(self, monitor, *args):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        mn = 'Monitor%s' % monitor
        for v, vn in zip( args, self.monitorProperties ):
            self.SetValue(mn, vn, v)

    def GetMonitor(self, monitor):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        mn = 'Monitor%s' % monitor
        md = []
        if self.config.has_section(mn):
            for vn in self.monitorProperties:
                md.append ( self.GetValue(mn, vn) )
        return md

    def HasMonitor(self, monitor):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        mn = 'Monitor%s' % monitor
        return self.config.has_section(mn)

    def getMonitorsData(self):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        return a list containing the monitors that we need to track
        based on info found in configfile
        """
        monitors = {}

        ms = self.GetOption('Monitors')
        resolution = self.GetOption('FullSize')
        dataFolder = self.GetOption('Data_Folder')

        for mon in range(0,ms):
            if self.HasMonitor(mon):
                _,source,track,mask_file,track_type,isSDMonitor = self.GetMonitor(mon)
                monitors[mon] = {}
                monitors[mon]['source'] = source
                monitors[mon]['resolution'] = resolution
                monitors[mon]['mask_file'] = mask_file
                monitors[mon]['track_type'] = track_type
                monitors[mon]['dataFolder'] = dataFolder
                monitors[mon]['track'] = track
                monitors[mon]['isSDMonitor'] = isSDMonitor

        return monitors



class previewPanel(wx.Panel):
    """
    A panel showing the video images.
    Used for thumbnails
    """
    def __init__(self, parent, size, keymode=True):
        print inspect.currentframe().f_back.f_locals['self']                                    # debug

        wx.Panel.__init__(self, parent, wx.ID_ANY, style=wx.WANTS_CHARS)

        self.parent = parent

        self.size = size
        self.SetMinSize(self.size)
        fps = options.GetOption('FPS_preview') or 25
        self.interval = 1000/fps # fps determines refresh interval in ms

        self.SetBackgroundColour('#A9A9A9')

        self.sourceType = 0
        self.source = ''
        self.mon = None
        self.track = False
        self.isSDMonitor = False
        self.trackType = 1
        self.drawROI = True
        self.timestamp = False
        self.camera = None
        self.resolution = None

        self.recording = False
        self.isPlaying = False

        self.allowEditing = True
        self.dragging = None        # Set to True while dragging
        self.startpoints = None     # Set to (x,y) when mouse starts drag
        self.track_window = None    # Set to rect when the mouse drag finishes
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

    def ClearAll(self, event=None):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Clear all ROIs
        """
        self.mon.delROI(-1)

    def ClearLast(self, event=None):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
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
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        save current selection
        """
        if self.allowEditing and self.selection:
            self.mon.addROI(self.selection, 1)
            self.selection = None
            self.polyPoints = []

    def AddPoint(self, event=None):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
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


    def onLeftDown(self, event=None):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
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

    def onLeftUp(self, event=None):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        if self.allowEditing:
            self.dragging = None
            self.track_window = self.selection

            if len(self.polyPoints) == 4:
                self.selection = self.polyPoints
                self.polyPoints = []

    def onMotion(self, event=None):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
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

    def prinKeyEventsHelp(self, event=None):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        for key in self.ACTIONS:
            print "%s\t%s" % (key, self.ACTIONS[key][1])

    def onKeyPressed(self, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Regulates key pressing responses:
        """
        key = chr(event.GetKeyCode())

        if key == "g" and self.mon.writer: self.mon.grabMovie = not self.mon.grabMovie

        if self.ACTIONS.has_key(key):
            self.ACTIONS[key][0]()

    def Calibrate(self, event=None):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
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
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        if len(self.polyPoints > 1):
            pt1, pt2 = self.polyPoints[0], self.polyPoints[1]
            self.mon.autoMask(pt1, pt2)
        else:
            print "Too few points to automask"
        self.polyPoints = []

    def SaveMask(self, event=None):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        self.mon.saveROIS()

    def setMonitor(self, camera, resolution=None):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """

        if not resolution: resolution = self.size

        self.camera = camera
        self.resolution = resolution
        self.mon = pv.Monitor()

        frame = cv.CreateMat(self.size[1], self.size[0], cv.CV_8UC3)
        self.bmp = wx.BitmapFromBuffer(self.size[0], self.size[1], frame.tostring())

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.playTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onNextFrame)


    def paintImg(self, img):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        if img:
            depth, channels = img.depth, img.nChannels
            # print('common, ln 527, cv.cv_maketype')
            datatype = cv.CV_MAKETYPE(depth, channels)

            frame = cv.CreateMat(self.size[1], self.size[0], datatype)
            cv.Resize(img, frame)

            cv.CvtColor(frame, frame, cv.CV_BGR2RGB)
            #cv.CvtColor(frame, frame, cv.CV_GRAY2RGB)

            self.bmp.CopyFromBuffer(frame.tostring())
            self.Refresh()

    def onPaint(self, evt):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        if self.bmp:
            dc = wx.BufferedPaintDC(self)
            #self.PrepareDC(dc)
            dc.DrawBitmap(self.bmp, 0, 0, True)
        evt.Skip()

    def onNextFrame(self, evt):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        img = self.mon.GetImage(drawROIs = self.drawROI, selection=self.selection, crosses=self.polyPoints, timestamp=self.timestamp)
        self.paintImg( img )
        if evt: evt.Skip()

    def Play(self, status=True, showROIs=True):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """

        if self.camera != None and self.resolution != None and not self.mon.hasSource():
            self.mon.setSource(self.camera, self.resolution)

        if self.mon:
            self.drawROI = showROIs
            self.isPlaying = status

            if status:
                self.playTimer.Start(self.interval)
            else:
                self.playTimer.Stop()

    def Stop(self):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        self.Play(False)
        self.mon.close()

    def hasMonitor(self):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        return (self.mon != None)

#################

options = pvg_config(DEFAULT_CONFIG)
