# -*- coding: utf-8 -*-
"""
       pvg_common.py

       Copyright 2011 Giorgio Gilestro <giorgio@gilest.ro>

       This program is free software; you can redistribute it and/or modify
       it under the terms of the GNU General Public License as published by
       the Free Software Foundation; either version 2 of the License, or
       (at your option) any later version.

       This program is distributed in the hope that it will be useful,
       but WITHOUT ANY WARRANTY; without even the implied warranty of
       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
       GNU General Public License for more details.

       You should have received a copy of the GNU General Public License
       along with this program; if not, write to the Free Software
       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
       MA 02110-1301, USA.

       Revisions by Caitlin Laughrey and Loretta E Laughrey in 2016.
"""
"""
 ---------------------------------------------------------------------------------   imports
"""
import wx, os
import ConfigParser                     # configuration file handler
from inspect import currentframe        # debug call tracer                                                              # debug
from db import debugprt                 # debug call tracer
import datetime
from dateutil import parser

"""
--------------------------------------------------------------------------   Developer Settings
"""
call_tracking = False  # if True each function will report it's beginning and end
show_imgs = False  # if true, show images
pgm = 'pvg_common.py'                   # identifies file name to debug call tracer


# -------------------------------------------------------------------------------  Config Object
class Configuration:
    """
    Handles program configuration
    Uses ConfigParser to store and retrieve
    From gg's toolbox
    """
    def __init__(self, filename=None):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')        
        """
        filename    the name of the configuration file
        config      configuration class object
                    options     pertain to program operation
                    monitors    pertain to video source
        self.config dictionary containing all config parameters and their values, indexed on 'section, key'

        read        reads configuration file and creates config dictionary
        getValue    retrieves value from the configuration class object using section and key
        setValue    sets an new value for a key from config dictionary
        save        saves configuration to a file
        """

        self.DEFAULT_data_dir = '\\Documents\\GitHub\\LL-DAM-Analysis\\Data\\Working_files\\'
        self.DEFAULT_configfile = 'pysolo_video.cfg'

    # start with the default config directory for pDir
        self.pDir = os.environ['USERPROFILE'] + self.DEFAULT_data_dir

    # make sure we have a full_path filename
        if filename == None :
            self.full_filename =  os.path.join(self.pDir, self.DEFAULT_configfile)
        elif filename == os.path.split(filename)[1] :
            self.full_filename = os.path.join(self.pDir, filename)
            
    # make sure file is accessible & if not create the directory & make a new config file there
        if not os.access(self.pDir, os.W_OK):
            os.makedirs(self.pDir)
            self.configOptsFromScratch(self.full_filename)
        elif not os.access(self.full_filename, os.W_OK):
            self.configOptsFromScratch(self.full_filename)

        self.config_obj = ConfigParser.RawConfigParser()            # read the config file
        self.config_obj.read(self.full_filename)

        # create configuration dictionary
        self.configDict = {}
    # Options
        self.opt_keys = ['webcams', 'thumbnailsize', 'fullsize',  'fps_preview', 'monitors', 'pDir']
        for key in self.opt_keys:
            value = self.getValue('Options', key)               # TODO:  are we doing this twice without need?
            indexStr = 'Options, ' + key
            self.configDict[indexStr] = value
    #Monitors
        self.mon_keys = ['sourcetype','issdmonitor', 'source','fps_recording','start_datetime','track','tracktype','maskfile','output_folder']
        if self.getValue('Options','monitors') > 0 :
            for mon_num in range(1, self.getValue('Options','monitors')+1 ):
                mon_name = 'Monitor%d' % mon_num
                for key in self.mon_keys:
                    value = self.getValue(mon_name, key)
                    indexStr = mon_name + ', ' + key
                    self.configDict[indexStr] = value
        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')

# %% ----------------------------------------------------------  Create configuration options from scratch and create file
    def configOptsFromScratch(self, full_filename):

        config_obj = ConfigParser.RawConfigParser()            # read the config file

        config_obj.add_section('Options')
        defaultOptions = {
            'webcams':0,
            'thumbnailSize': (320, 240),
            'fullsize': (640, 480),
            'fps_preview': 5,
            'monitors': 0,
            'pDir': (os.path.split(full_filename)[0])
        }
        for key in defaultOptions:
            config_obj.set('Options', key, defaultOptions[key])

        config_obj.add_section('Monitor1')
        defaultMonitor = {
            'sourcetype': 1,
            'issdmonitor': False,
            'source': None,
            'fps_recording': 1,
            'start_datetime': datetime.datetime.now(),
            'track': False,
            'tracktype': 0,
            'maskfile': None,
            'output_folder': None
        }
        for key in defaultMonitor:
            config_obj.set('Monitor1', key, defaultMonitor[key])

    # save to file
        with open(full_filename, 'wb') as configfile:
            config_obj.write(configfile)
# %% ----------------------------------------------------------------------------   Set options from menu
    def onOptionSet(self):
        print('set options from menu')      # TODO: write this function
# %%  ----------------------------------------------------------------------------  Save config file
    def Save_config(self, config_obj, config, full_filename):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')        
        """
        Saves the configuration to full_filename.
        """
    # update configuration object with current config dictionary
        opt_keys = ['webcams', 'thumbnailsize', 'fullsize', 'fps_preview', 'monitors', 'pDir']
        for key in opt_keys:
            self.setValue('Options', key, config['Options, '+key])

        mon_keys = ['sourcetype','issdmonitor', 'source','fps_recording','start_datetime','track','tracktype','maskfile','output_folder']
        if config['Options, monitors'] > 0:
            for mon_num in range(1, config['Options, monitors']):
                mon_name = 'Monitor%d' % mon_num
                for key in mon_keys:
                    self.setValue(mon_name, key, config[mon_name + ', '+key])
    # save to file
        with open(full_filename, 'wb') as configfile:
            self.config_obj.write(configfile)

        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')
# %% ----------------------------------------------------------  Set Values in Config
    def setValue(self, section, key, value):
        if call_tracking: debugprt(self,currentframe(),pgm,'begin     ')                                # debug
        """
        changes or adds a configuration value in config file
        """
        if not self.config_obj.has_section(section):
            self.config_obj.add_section(section)
        if not self.config_obj.has_option(section, key):
            self.config_obj.add_option(section, key)

        self.config_obj.set(section, key, value)

        if call_tracking: debugprt(self,currentframe(),pgm,'end   ')
    # %%  -----------------------------------------------------------------------------------  Get values from config
    def getValue(self, section, key):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        get value from config file based on section and keyword
        Does some sanity checking to return tuple, integer and strings, datetimes, as required.
        """
        r = self.config_obj.get(section, key)

            # check input types:
        if key == 'start_datetime' and type(r) == type(''):                     # datetime values
            try: r = parser.parse(r)
            except: r = datetime.datetime.now()

            if call_tracking: debugprt(self, currentframe(), pgm, 'end   ')
            return r

    # look for string characteristics to figure out what type they should be
        if r == 'True' or r == 'False' :                                         # boolean
            if r == 'False' :
                r = False
            elif r == 'True' :
                r = True
            if call_tracking: debugprt(self,currentframe(),pgm,'end   ')
            return r

        try:
            int(r) == int(0)                                                   # int as text
            if call_tracking: debugprt(self, currentframe(), pgm, 'end   ')
            return int(r)
        except:
            None

        try:
            float(r) == float(1.1)                                              # float as text
            if call_tracking: debugprt(self, currentframe(), pgm, 'end   ')
            return float(r)
        except:
            None

        if ',' in r:                                                         # tuple of two integers
            r = tuple(r[1:-1].split(','))
            r = (int(r[0]), int(r[1]))
            if call_tracking: debugprt(self,currentframe(),pgm,'end   ')
            return r

        return r                                                                # all else has failed:  return as string
    # %% ------------------------------------------------------------------------------------ Save file as
    def onFileSaveAs(self, config_obj, configDict):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Opens the save file window
        """

        # set file types for find dialog
        wildcard = "PySolo Video config file (*.cfg)|*.cfg|" \
                   "All files (*.*)|*.*"                            # adding space in here will mess it up!

        dlg = wx.FileDialog(None,
            message="Save file as ...", defaultDir=configDict['Options, pDir'],
            defaultFile=os.path.split(self.full_filename)[1], wildcard=wildcard,
            style=(wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        )

        if dlg.ShowModal() == wx.ID_OK:  # show the save window
            path = dlg.GetPath()  # gets the path from the save dialog
            self.Save_config(config_obj, configDict, path)                          # TODO:  save is writing a blank file

        dlg.Destroy()
        if call_tracking: debugprt(self, currentframe(), pgm, 'end   ')

        # %%
    # %% ------------------------------------------------------------------------------------ Open file
    def onFileOpen(self):  # viewing all files is not an option
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """                                                                    # .cfg files don't show.  you can ask for it, but it doesn't load
        Opens the open file window                                              # no complaints about non-existent files
        """
        #  set file types for find dialog
        wildcard = "pySolo Video config file (*.cfg)|*.cfg|" \
                   " All files (*.*)|*.*"  # don't add any spaces!

        dlg = wx.FileDialog(  # make an open-file window
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
        )

        if dlg.ShowModal() == wx.ID_OK:  # show the open-file window
            path = dlg.GetPath()
            self.__init__(path)

        dlg.Destroy()
        if call_tracking: debugprt(self, currentframe(), pgm, 'end   ')




        

