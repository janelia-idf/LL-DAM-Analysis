#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       pvg.py pysolovideogui
#
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
# -------------------------------------------------------------------------------- imports
"""
import wx, os, sys
import pvg_common as cmn
import pvg_panel_one as p1
import pvg_panel_two as p2
#from pvg_options import pvg_OptionsPanel
#from pysolovideo import pySoloVideoVersion
from win32api import GetSystemMetrics                       # to get screen resolution
from inspect import currentframe                                                                     # debug

"""
# -------------------------------------------------------------------------  developer  Settings
""" 

pgm = 'pvg.py'
console_to_file = False             # controls whether console output goes to console or a file

"""
# %%                                                screen height & width

Get screen_width & screen_height:   Screen resolution information
      Allows all object sizes to be sized relative to the display.
"""

screen_width = GetSystemMetrics(0)   # get the screen resolution of this monitor
screen_height = GetSystemMetrics(1)

# -------------------------------------------------------------------------------------  Main Notebook
class mainNotebook(wx.Notebook):
    """
    The main notebook containing all the panels for data displaying and analysis
    """

    def __init__(self, parent, cfg):
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug

        self.cfg = cfg
        self.config_obj = self.cfg.config_obj
        self.configDict = self.cfg.configDict
        self.full_filename = self.cfg.full_filename

    # create a notebook

        wx.Notebook.__init__(self, parent, wx.ID_ANY, style = wx.NB_LEFT)

        self.panelOne = p1.panelOne(self, self.cfg)                        # create thumbnail pg;
        self.AddPage(self.panelOne, 'Thumbnails')
        mon_num = self.panelOne.mon_num

        self.panelTwo = p2.maskPanel(self, mon_num, self.cfg)             # create mask maker pg
        self.AddPage(self.panelTwo, 'Mask Maker')

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

        self.Layout()
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                    Page changing
    def OnPageChanging(self, event):
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Switches between notebook pages.
        """
        p1.StopPlaying()                    # see pvg_panel_one.py
        p2.StopPlaying()                    # see pvg_panel_two.py
        
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        Refresh all pages
    def updateUI(self):
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Refreshes all pages of notebook.
        """
        self.p1.onRefresh()                    # see pvg_panel_one.py
        self.p2.onRefresh(self.cfg)                    # see pvg_panel_two.py
        self.Layout()
        
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

        
# --------------------------------------------------------------------------------------- Main Window
class mainFrame(wx.Frame):
    """
    Creates the main window of the application.
    """
    def __init__(self, *args, **kwds):
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug

        self.full_filename = os.path.join(cmn.pDir, cmn.DEFAULT_configfile)

        self.cfg = cmn.Configuration(self.full_filename)
        self.config_obj = self.cfg.config_obj
        self.configDict = self.cfg.configDict
        self.full_filename = self.cfg.full_filename

        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.__set_properties("pySolo Video",0.9)   # set title and frame/screen ratio
        self.__menubar__()
        self.__do_layout()

        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                      Set window properties
    def __set_properties(self, window_title, size_ratio ):
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Set the title of the main window.
        Set the size of the main window relative to the size of the user's display.
        Center the window on the screen.
        """
        # begin wxGlade: mainFrame.__set_properties
        self.SetTitle(window_title)                    # set window title
        self.SetSize((screen_width*size_ratio,
                      screen_height*size_ratio))     # set size of window
        self.Center()                               # center the window

        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                  Put notebook in window.
    def __do_layout(self):
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Puts a notebook in the main window.
        """
        self.videoNotebook = mainNotebook(self, self.cfg)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(self.videoNotebook, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)

        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')


# %%                                                            Create Menubar
    def __menubar__(self):
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Creates menu bar at top of window.
        """
# %%                                                              Create IDs
        """ Give new IDs to the menu voices in the menubar """
        ID_FILE_OPEN = wx.NewId()
        ID_FILE_SAVE = wx.NewId()
        ID_FILE_SAVE_AS = wx.NewId()
        ID_FILE_EXIT = wx.NewId()
        ID_OPTIONS_SET = wx.NewId()
        ID_HELP_ABOUT = wx.NewId()

# %%                                                      Create menu options
        """ Create file-menu objects  ( '&' indicates shortcut key) """
        filemenu = wx.Menu()
        filemenu. Append(ID_FILE_OPEN, '&Open File', 'Open a file')
        filemenu. Append(ID_FILE_SAVE, '&Save File', 'Save current file')
        filemenu. Append(ID_FILE_SAVE_AS, '&Save as...',
                         'Save current data in a new file')
        filemenu. AppendSeparator()         # draws horizontal separater line
        filemenu. Append(ID_FILE_EXIT, 'E&xit Program', 'Exit')

        """ Create options-menu objects """
        optmenu =  wx.Menu()
        optmenu. Append(ID_OPTIONS_SET, 'Confi&gure',
                        'View and change settings')

        """  Create help-menu objects """
        helpmenu =  wx.Menu()
        helpmenu. Append(ID_HELP_ABOUT, 'Abou&t', 'About pySolo Video')

# %%                                                        Apply menubar
        """ Apply the Menu Bar Object """
        menubar =  wx.MenuBar(style = wx.SIMPLE_BORDER)

        """ Populate the MenuBar """
        menubar. Append(filemenu, '&File')
        menubar. Append(optmenu, '&Options')
        menubar. Append(helpmenu, '&Help')

        """ Apply the menu to the window """
        self.SetMenuBar(menubar)

# %%                                          connect menu objects to functions        
        """ Connect the menu objects to their functions """
        self.Bind(wx.EVT_MENU, self.cfg.onFileOpen, id=ID_FILE_OPEN)
        self.Bind(wx.EVT_MENU, self.cfg.save_Config, id=ID_FILE_SAVE)
        self.Bind(wx.EVT_MENU, self.cfg.onFileSaveAs, id=ID_FILE_SAVE_AS)
        self.Bind(wx.EVT_MENU, self.onFileExit, id=ID_FILE_EXIT)
        self.Bind(wx.EVT_MENU, self.cfg.onOptionSet, id=ID_OPTIONS_SET)
        self.Bind(wx.EVT_MENU, self.onAbout, id=ID_HELP_ABOUT)

        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                              About        
    def onAbout(self, event):
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Shows the about dialog.
        """

        """ Text for the dialog box. """
        about = 'pySolo-Video - v %s\n\n' % 'Laughrey Development'
        about += 'by Giorgio F. Gilestro\n'
        about += 'updated by Caitlin Laughrey and Loretta E Laughrey in 2016\n\n'
        about += 'Visit http://www.pysolo.net for more information'

        """ Put the message, and information icon, and an ok button in a window. """
        dlg = wx.MessageDialog(self, about, 'About',
                               wx.OK | wx.ICON_INFORMATION)

        """ Show the about dialog. """
        dlg.ShowModal()
        dlg.Destroy()
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                            Save File
    """
    def onFileSave(self, event):                                               
        """ """
        Calls the save function.
        """"""
        options.Save()                              # see pvg_common.py
    """

# %%
    def onFileExit(self, event):
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Calls close function
        """
        self.Close()                            # from wxpython
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')

# %%                                                                # TODO:  used?
    """
    def onConfigure(self, event):
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """"""
        opens configure dialog box                                                  $$$$$$  configuration?
        """"""
        frame_opt = pvg_OptionsPanel(self)      # see pvg_options.py
        #frame_opt.Show()
        res = frame_opt.ShowModal()             # displays the dialog box
        if res == wx.ID_OK:
            print "applying any changes"                                        # prints to console
            frame_opt.onSave()                  # see pvg_options.py
            self.videoNotebook.updateUI()       # refreshes notebook panels
        elif res == wx.ID_CANCEL:
            print "no changes were made"                                        # prints to console
        frame_opt.Destroy()
        if cmn.call_tracking: cmn.debugprt(self,currentframe(),pgm,'end   ')
    """
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Main Program

if __name__ == "__main__":
    if console_to_file:
        console_file = os.path.join(cmn.pDir, 'stdout.txt')
        sys.stdout = open(console_file, 'w')          # send console output to file

    app = wx.App()
    wx.InitAllImageHandlers()

    frame_1 = mainFrame(None, -1, "")           # Create the main window.
    app.SetTopWindow(frame_1)                   # Makes this window the main window
    frame_1.Show()                              # Shows the main window
    app.MainLoop()                              # Begin user interactions.
