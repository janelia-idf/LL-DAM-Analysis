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

#       Revisions by Caitlin Laughrey and Loretta E Laughrey in 2016.

"""
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    imports
"""
import wx, cv, os        
import ConfigParser
from inspect import currentframe                                                                     # debug
from db import debugprt
import datetime
from dateutil import parser
import ctypes.wintypes     # gets root directory info


"""
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Settings
"""
call_tracking = False  # if True each function will report it's beginning and end
show_imgs = False  # if true, show images


pgm = 'pvg_common.py'

# get root dir name for all file operations & default configuration information
#

CSIDL_PERSONAL = 5  # My Documents
SHGFP_TYPE_CURRENT = 0  # Get current, not default value
buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)  # get user document folder path
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
root_dir = buf.value + '\\GitHub\\LL-DAM-Analysis\\'
data_dir = root_dir + 'Data\\Working_files\\'

DEFAULT_CONFIG = 'pysolo_video.cfg'

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  MyConfig
class myConfig():
    """
    Handles program configuration
    Uses ConfigParser to store and retrieve
    From gg's toolbox
    """
    def __init__(self, filename=None, temporary=False, defaultOptions=None):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')        
        """
        filename    the name of the configuration file
        temporary   whether we are reading and storing values temporarily
        defaultOptions  a dict containing the defaultOptions
        """

        filename = filename or DEFAULT_CONFIG
        pDir = data_dir
#        if not os.access(pDir, os.W_OK): pDir = os.environ['HOME']
        
        self.filename = os.path.join (pDir, filename)
        self.filename_temp = '%s~' % self.filename

        self.config = None

        if defaultOptions != None:
            self.defaultOptions = defaultOptions
        else:
            self.defaultOptions = { "option_1" : [0, "Description"],
                                    }

        self.Read(temporary)
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        New config file
    def New(self, filename):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        self.filename = filename
        self.Read()
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        Read config file
    def Read(self, temporary=False):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
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
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')


# %%                                                        Save config file
    def Save(self, temporary=False, newfile=False, filename=None):                  # saves options configuration
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')        
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
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')


# %%                                                     Set Values in Config
    def SetValue(self, section, key, value):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                # debug
        """
        puts configuration values in config file
        """
        if not self.config.has_section(section):
            self.config.add_section(section)

        self.config.set(section, key, value)
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')

# %%                                                    Get values from config
    def GetValue(self, section, key):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                # debug
        """
        get value from config file
        Does some sanity checking to return tuple, integer and strings
        as required.
        """
        r = self.config.get(section, key)

        if key == 'start_datetime' and type(r) == type(''):         # datetime values
            r = parser.parse(r)
            return r
        elif type(r) == datetime.datetime:
            return r

        if type(r) == type(0) or type(r) == type(1.0):  # native int and float
            if call_tracking: debugprt(self,currentframe(),pgm,'end   ')
            return r
        elif type(r) == type(True):                     # native boolean
            if call_tracking: debugprt(self,currentframe(),pgm,'end   ')
            return r
        elif type(r) == type(''):
            r = r.split(',')

        if len(r) == 2:                                 # tuple
            r = tuple([int(i) for i in r]) 

        elif len(r) < 2:                                # string or integer
            try:
                r = int(r[0])                           # int as text
            except:
                if len(r) > 0:
                    r = r[0]                            # string
                else:
                    r = ""

        if r == 'False' or r == 'True':
            r = (r == 'True')                           # bool

        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')
        return r


# %%                                   Get value from options section of config

    def GetOptions(self):
        self.opt_names = [webcams, monitors, data_folder, fullsize, thumbnailsize, fps_recording, fps_preview]
        opts = []
        if self.config.has_section('Options'):
            for key in self.opt_names:
                opts.append(self.GetValue('Options', key))
        return opts

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Acquire Object        
class acquireObject():
    def __init__(self, monitor, source, start_datetime, resolution, mask_file, track, track_type, dataFolder):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """

        print("$$$$$$ pvg_common; 193; acquireObject_init; mask_file = ", mask_file)
        self.monitor = monitor
        self.keepGoing = False
        self.verbose = True                                                        # false turns off debug
        self.track = track
        dataFolder = options.GetValue("Options","Data_Folder")
        outputFile = os.path.join(dataFolder, 'Monitor%d.txt' % monitor)

        self.mon = Monitor()
        self.mon.setSource(source, resolution)
        self.mon.setTracking(True, track_type, start_datetime, mask_file, outputFile)

        print("$$$$$$ pvg_common; 205; acquireObject_init; mask_file = ", mask_file)

        if self.verbose: print("Verbose 247 - Monitor %s, track %s, track type %d, \n source %s, \n start_datetime, \n mask %s,  \n output file %s  "
                               % (monitor, track, track_type,
                                  source,
                                  start_datetime,
                                  mask_file,
                                  outputFile) )
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')
        
# %%                                                        Run
    def run(self, kbdint=False):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        checks to see if program should keep going.
        """
        while self.keepGoing:
            self.keepGoing = self.mon.GetImage()
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        Start
    def start(self):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        self.keepGoing = True
        self.run()
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')

# %%                                                            Halt
    def halt(self):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        self.keepGoing = False
        if self.verbose: print ( "Verbose: Stopping capture" )
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')


        


class pvg_config(myConfig):
    """
    Inheriting from myConfig
    """
    def __init__(self, filename=None, temporary=False):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                      # debug

        defaultOptions = { 
            "Monitors" :      [9, "Select the number of monitors connected to this machine"],
            "Webcams"  :      [1, "Select the number of webcams connected to this machine"],
            "ThumbnailSize" : ['320, 240', "Specify the size for the thumbnail previews"],
            "FullSize" :      ['640, 480', "Specify the size for the actual acquisition from the webcams.\nMake sure your webcam supports this definition"],
            "FPS_preview" :   [5, "Refresh frequency (FPS) of the thumbnails during preview.\nSelect a low rate for slow computers"],
            "FPS_recording" : [.5, "Actual refresh rate (FPS) during acquisition and processing"],
            "Data_Folder" :   [data_dir, "Folder where the final data are saved"],

             }

        self.monitorProperties = ['sourceType', 'source', 'start_datetime', 'track', 'mask_file', 'trackType', 'isSDMonitor']

        myConfig.__init__(self, filename, temporary, defaultOptions)
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')

    def SetMonitor(self, monitor, *args):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                            # debug

        mon_name = 'Monitor%s' % (monitor +1)                         # monitor is 0-indexed, mon_name is 1-indexed
        for v, vn in zip( args, self.monitorProperties ):
            self.SetValue(mon_name, vn, v)

            print("$$$$$$ pvg_common; 328; setmonitor; mon_name = ", mon_name)
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')


    def GetMonitor(self, monitor):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                           # debug
        """
        """
        mon_name = 'Monitor%s' % (monitor +1)                        # monitor is 0-indexed, mon_name is 1-indexed
        print("$$$$$$ pvg_common; 336; GetMonitor; mon_name = ", mon_name)

        md = []
        if self.config.has_section(mon_name):
            for vn in self.monitorProperties:
                md.append ( self.GetValue(mon_name, vn) )                               # mon_name is 1-indexed
                print("$$$$$$ pvg_common; 340; GetMonitor; mon_name = ", mon_name)
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')
        return md

    def HasMonitor(self, monitor):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                            # debug
        """
        """
        mon_name = 'Monitor%s' % (monitor +1)                        # monitor is 0-indexed, mon_name is 1-indexed

        a = self.config.has_section(mon_name)
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')
        return a

    def getMonitorsData(self):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                           # debug
        """
        return a list containing the monitors that we need to track
        based on info found in configfile
        """
        monitors = {}

        ms = self.GetValue('Options','Monitors')
        resolution = self.GetValue('Options','FullSize')
        dataFolder = self.GetValue('Options','Data_Folder')
        
        for mon in range(0,ms):                           # mon is 0-indexed
            if self.HasMonitor(mon):                        # HasMonitor expects a 0-indexed monitor number
                _,source,start_datetime,track,mask_file,track_type,isSDMonitor = self.GetMonitor(mon)
                monitors[mon] = {}
                monitors[mon]['source'] = source
                monitors[mon]['start_datetime'] = start_datetime
                monitors[mon]['resolution'] = resolution
                monitors[mon]['mask_file'] = mask_file
                monitors[mon]['track_type'] = track_type
                monitors[mon]['dataFolder'] = dataFolder
                monitors[mon]['track'] = track
                monitors[mon]['isSDMonitor'] = isSDMonitor

        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')
        return monitors



#################

options = pvg_config(DEFAULT_CONFIG)
