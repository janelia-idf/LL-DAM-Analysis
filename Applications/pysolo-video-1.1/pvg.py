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
#


import wx, os
from win32api import GetSystemMetrics  # to get screen resolution
from pvg_panel_one import panelOne
from pvg_options import pvg_OptionsPanel
from pvg_panel_two import panelLiveView
from pvg_common import options, DEFAULT_CONFIG

from pysolovideo import pySoloVideoVersion


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Main Notebook

class mainNotebook(wx.Notebook):
    """
    The main notebook containing all the panels for data displaying and analysis
    """
    def __init__(self, *args, **kwds):
        # begin wxGlade: propertiesNotebook.__init__
        kwds["style"] = wx.NB_LEFT
        wx.Notebook.__init__(self, *args, **kwds)       # initialize notebook

        self.panelOne = panelOne(self)                  # create thumbnail pg
        self.AddPage(self.panelOne, "Thumbnails")

        self.panelTwo = panelLiveView(self)             # create live view pg
        self.AddPage(self.panelTwo, "Live View")

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

        self.Layout()

# %%
    def OnPageChanging(self, event):
        """
        Switches between notebook pages.
        """
        self.panelOne.StopPlaying()                    # see pvg_panel_one.py
        self.panelTwo.StopPlaying()                    # see pvg_panel_two.py

# %%
    def updateUI(self):
        """
        Refreshes all pages of notebook.
        """
        print('updateUI function')                                              # print debug
        self.panelOne.onRefresh()                    # see pvg_panel_one.py
        self.panelTwo.onRefresh()                    # see pvg_panel_two.py
        self.Layout()                                                           # where is layout()?

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Main Frame

class mainFrame(wx.Frame):
    """
    Creates the main window of the application.
    """
    def __init__(self, *args, **kwds):

        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.__set_properties("pySolo Video",0.9)   # set title , size, position
        self.__menubar__()
        self.__do_layout()

# %%
    def __set_properties(self, window_title, size_ratio ):
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

# %%        
    def __do_layout(self):
        """
        Puts a notebook in the main window.
        """
        self.videoNotebook = mainNotebook(self, -1)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(self.videoNotebook, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)


# %%
    def __menubar__(self):
        """
        Creates menu bar at top of window.
        """

        """ Give new IDs to the menu voices in the menubar """
        ID_FILE_OPEN = wx.NewId()
        ID_FILE_SAVE = wx.NewId()
        ID_FILE_SAVE_AS = wx.NewId()
        # ID_FILE_CLOSE =  wx.NewId()
        ID_FILE_EXIT = wx.NewId()
        ID_HELP_ABOUT = wx.NewId()
        ID_OPTIONS_SET = wx.NewId()

        """ Create file-menu objects  ( '&' indicates shortcut key) """
        filemenu =  wx.Menu()
        filemenu. Append(ID_FILE_OPEN, '&Open File', 
                         'Open a file')
        #filemenu. Append(ID_FILE_SAVE, '&Save File', 
        #                  'Save current file')
        filemenu. Append(ID_FILE_SAVE_AS, '&Save as...',
                         'Save current data in a new file')
        #filemenu. Append(ID_FILE_CLOSE, '&Close File', 
        #               'Close')
        filemenu. AppendSeparator()           # draws horizontal separater line
        filemenu. Append(ID_FILE_EXIT, 'E&xit Program', 'Exit')

        """ Create options-menu objects """
        optmenu =  wx.Menu()
        optmenu. Append(ID_OPTIONS_SET, 'Confi&gure', 
                        'View and change settings')

        """  Create help-menu objects """
        helpmenu =  wx.Menu()
        helpmenu. Append(ID_HELP_ABOUT, 'Abou&t', 'About pySolo Video')

        """ Apply the Menu Bar Object """
        menubar =  wx.MenuBar(style = wx.SIMPLE_BORDER)

        """ Populate the MenuBar """
        menubar. Append(filemenu, '&File')
        menubar. Append(optmenu, '&Options')
        menubar. Append(helpmenu, '&Help')

        """ Apply the menu to the window """
        self.SetMenuBar(menubar)

        """ Connect the menu objects to their functions """
        wx.EVT_MENU(self, ID_FILE_OPEN, self.onFileOpen)
#        wx.EVT_MENU(self, ID_FILE_SAVE, self.onFileSave)
        wx.EVT_MENU(self, ID_FILE_SAVE_AS, self.onFileSaveAs)
        # wx.EVT_MENU(self, ID_FILE_CLOSE, self.onFileClose)
        wx.EVT_MENU(self, ID_FILE_EXIT, self.onFileExit)
        wx.EVT_MENU(self, ID_OPTIONS_SET, self.onConfigure)
        wx.EVT_MENU(self, ID_HELP_ABOUT, self.onAbout)

    def onAbout(self, event):
        """
        Shows the about dialog.
        """
        
        """ Text for the dialog box. """
        about = 'pySolo-Video - v %s\n' % pySoloVideoVersion
        about += 'by Giorgio F. Gilestro\n'
        about += 'Visit http://www.pysolo.net for more information'

        """ Put the message, and information icon, and an ok button in a window. """
        dlg = wx.MessageDialog(self, about, 'About', 
                               wx.OK | wx.ICON_INFORMATION)

        """ Show the about dialog. """        
        dlg.ShowModal()
        dlg.Destroy()

# %%  
#    def onFileSave(self, event):                                               # what's the point of a one line function?
#        """                                                                    # FUNCTION NOT IN USE
#        Calls the save function.
#        """
#        options.Save()                              # see pvg_common.py
#
# %%
    def onFileSaveAs(self, event):                                              
        """                                                                     
        Opens the save file window
        """
        filename = DEFAULT_CONFIG                   # see pvg_common.py
        
        # set file types for find dialog
        wildcard = "PySolo Video config file (*.cfg)|*.cfg|" \
                 "All files (*.*)|*.*"    # adding space in here will mess it up!


        print("filename1 = " + filename)
        dlg = wx.FileDialog(                    # make a save window
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile=filename, wildcard=wildcard, 
            style=(wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            )

        print("filename2 = " + filename)
        #dlg.SetFilterIndex(2)

        if dlg.ShowModal() == wx.ID_OK:         # show the save window
            path = dlg.GetPath()                # gets the path from the save dialog
            options.Save(filename=path)
            print("filename3 = "+ filename)
        
        print("filename4 = "+ filename)
           
            
        dlg.Destroy()

# %%
    def onFileOpen(self, event):                                                # viewing all files is not an option
        """                                                                     # .cfg files don't show.  you can ask for it, but it doesn't load
        Opens the open file window                                              # no complaints about non-existent files
        """
        #  set file types for find dialog
        wildcard = "pySolo Video config file (*.cfg)|*.cfg|" \
                   " All files (*.*)|*.*"    # don't add any spaces!

        dlg = wx.FileDialog(                    # make an open-file window
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:         # show the open-file window
            path = dlg.GetPath()
            options.New(path)

        dlg.Destroy()

# %%
    def onFileExit(self, event):
        """
        Calls close function
        """
        self.Close()                            # from wxpython

# %%
    def onConfigure(self, event):
        """
        opens configure dialog box
        """
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

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Main Program

"""
Set global variables:
    screen_width & screen_height:   Screen resolution information. 
        Allows all object sizes to be sized relative to the display.
"""
screen_width = GetSystemMetrics(0)   # get the screen resolution of this monitor
screen_height = GetSystemMetrics(1) 
 

if __name__ == "__main__":

    app = wx.App()
    wx.InitAllImageHandlers()
    
    frame_1 = mainFrame(None, -1, "")           # Create the main window.
    app.SetTopWindow(frame_1)
    frame_1.Show()                              # Show the main window
    app.MainLoop()                              # Begin user interactions.
