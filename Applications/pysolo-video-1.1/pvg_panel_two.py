#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#       untitled.py
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

import wx, os
import pysolovideo as pv
import pvg_common as cmn
import pvg_panel_one as pv1

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Global Variables
# get root dir name for all file operations
#
import ctypes.wintypes
CSIDL_PERSONAL = 5       # My Documents
SHGFP_TYPE_CURRENT = 0   # Get current, not default value
buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)  # get user document folder path
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
root_dir = buf.value + '\\GitHub\\LL-DAM-Analysis\\'


data_dir = root_dir + 'Data\\Working_files\\'
DEFAULT_CONFIG = 'pysolo_video.cfg'
pgm = 'pvg_acquire.py'
#start_dt = datetime.datetime(2016,8,23,13,52,17)
#t = datetime.time(19, 1, 00)                    # get datetime for adjusting from 31 Dec 1969 at 19:01:00
#d = datetime.date(1969, 12, 31)
#zero_dt = datetime.datetime.combine(d, t)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



class panelLiveView(wx.Panel):
    """
    Panel Number 2
    Live view of selected camera
    """
    def __init__(self, parent, cfg, mon_num):

        self.cfg = cfg
        self.config_obj = self.cfg.config_obj
        self.configDict = self.cfg.configDict

        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.monitor_number = self.mon_num = mon_num
        self.mon_name = 'Monitor%d' % self.mon_num
        self.fs_size = self.configDict['Options, fullsize']


        self.fsPanel = pv1.previewPanel(self, self.cfg, self.mon_num, self.fs_size)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)

        #Static box1: monitor input
        sb_1 = wx.StaticBox(self, -1, "Select Monitor")#, size=(250,-1))
        self.sbSizer_1 = wx.StaticBoxSizer (sb_1, wx.VERTICAL)
        self.MonitorList = ['Monitor %s' % (int(m) + 1) for m in range(self.monitor_number)]
        self.thumbnailNumber = wx.ComboBox(self, -1, size=(-1,-1) , choices=self.MonitorList, style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind(wx.EVT_COMBOBOX, self.onChangeMonitor, self.thumbnailNumber)

        self.sourceTXTBOX =  wx.TextCtrl (self, -1, "No monitor selected", style=wx.TE_READONLY)

        self.sbSizer_1.Add ( self.thumbnailNumber, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        self.sbSizer_1.Add ( self.sourceTXTBOX, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )

        #Static box2: mask parameters
        sb_2 = wx.StaticBox(self, -1, "Mask Editing")#, size=(250,-1))
        sbSizer_2 = wx.StaticBoxSizer (sb_2, wx.VERTICAL)
        fgSizer_1 = wx.FlexGridSizer( 0, 2, 0, 0 )

        self.btnClear = wx.Button( self, wx.ID_ANY, label="Clear All")
        self.Bind(wx.EVT_BUTTON, self.fsPanel.ClearAll, self.btnClear)

        self.btnClearLast = wx.Button( self, wx.ID_ANY, label="Clear selected")
        self.Bind(wx.EVT_BUTTON, self.fsPanel.ClearLast, self.btnClearLast)


        self.btnAutoFill = wx.Button( self, wx.ID_ANY, label="Auto Fill")
        self.Bind(wx.EVT_BUTTON, self.fsPanel.AutoMask, self.btnAutoFill)

        fgSizer_1.Add (self.btnClear)
        fgSizer_1.Add (self.btnClearLast)
        fgSizer_1.Add (self.btnAutoFill)

        sbSizer_2.Add (fgSizer_1)


        #Static box3: mask I/O
        sb_3 = wx.StaticBox(self, -1, "Mask File")#, size=(250,-1))
        sbSizer_3 = wx.StaticBoxSizer (sb_3, wx.VERTICAL)

        self.currentMaskTXT = wx.TextCtrl (self, -1, "No Mask Loaded", style=wx.TE_READONLY)

        btnSizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.btnLoad = wx.Button( self, wx.ID_ANY, label="Load Mask")
        self.Bind(wx.EVT_BUTTON, self.onLoadMask, self.btnLoad)
        self.btnSave = wx.Button( self, wx.ID_ANY, label="Save Mask")
        self.Bind(wx.EVT_BUTTON, self.onSaveMask, self.btnSave)
        self.btnSaveApply = wx.Button( self, wx.ID_ANY, label="Save and Apply")
        self.Bind(wx.EVT_BUTTON, self.onSaveApply, self.btnSaveApply)

        btnSizer_1.Add(self.btnLoad)
        btnSizer_1.Add(self.btnSave)
        btnSizer_1.Add(self.btnSaveApply)

        sbSizer_3.Add ( self.currentMaskTXT, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
        sbSizer_3.Add (btnSizer_1, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        ##

        #Static box4: help
        sb_4 = wx.StaticBox(self, -1, "Help")
        sbSizer_4 = wx.StaticBoxSizer (sb_4, wx.VERTICAL)
        titleFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        instr = [ ('Left mouse button - single click outside ROI', 'Start dragging ROI. ROI will be a perfect rectangle'),
                  ('Left mouse button - single click inside ROI', 'Select ROI. ROI turns red.'),
#                  ('Left mouse button - double click', 'Select corner of ROI.\nWill close ROI after fourth selection'),
                  ('Left mouse button - double click', 'Add currently selected ROI. ROI turns white.'),
#                  ('Middle mouse button - single click', 'Add currently selected ROI. ROI turns white.'),
                  ('Right mouse button - click', 'Remove selected currently selected ROI'),
                  ('Auto Fill', 'Will fill 32 ROIS (16x2) to fit under the last two\nselected points. To use select first upper left corner,\n then the lower right corner, then use "Auto Fill".')
                  ]

        for title, text in instr:
            t = wx.StaticText(self, -1, title); t.SetFont(titleFont)
            sbSizer_4.Add( t, 0, wx.ALL, 2 )
            sbSizer_4.Add(wx.StaticText(self, -1, text) , 0 , wx.ALL, 2 )
            sbSizer_4.Add ( (wx.StaticLine(self)), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

        sizer_4.Add(self.sbSizer_1, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
        sizer_4.Add(sbSizer_2, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
        sizer_4.Add(sbSizer_3, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
        sizer_4.Add(sbSizer_4, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )


        sizer_3.Add(self.fsPanel, 0, wx.LEFT|wx.TOP, 20 )
        sizer_3.Add(sizer_4, 0, wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        sizer_1.Add(sizer_3, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )


        self.SetSizer(sizer_1)
        print wx.Window.FindFocus()

        self.Bind( wx.EVT_CHAR, self.fsPanel.onKeyPressed )

    def StopPlaying(self):
        """
        """
        if self.fsPanel and self.fsPanel.isPlaying: self.fsPanel.Stop()


    def onChangeMonitor(self, event):
        """
        FIX THIS
        this is a mess
        """

        if self.fsPanel.isPlaying: self.fsPanel.Stop()

        self.monitor_name = event.GetString()
        self.monitor_number = self.MonitorList.index( self.monitor_name )

        n_cams = options.GetOption("Webcams")
        WebcamsList = [ 'Webcam %s' % (int(w) +1) for w in range( n_cams ) ]

        if options.HasMonitor(self.monitor_number):
            sourceType, source, track, mask_file, trackType, isSDMonitor = options.GetMonitor(self.monitor_number)
            self.fsPanel.setMonitor( source )
            self.fsPanel.Play()

            if mask_file:
                self.fsPanel.mon.loadROIS(mask_file)
                self.currentMaskTXT.SetValue(os.path.split(mask_file)[1] or '')

            if sourceType == 0:
                self.sourceTXTBOX.SetValue( WebcamsList[source] )
            else:
                self.sourceTXTBOX.SetValue( os.path.split(source)[1] )

        else:
            sourceType, source, track, mask_file, trackType = [0, '', False, '', 1]
            self.sourceTXTBOX.SetValue('No Source for this monitor')


    def onSaveMask(self, event):
        """
        Save ROIs to File
        """

        filename = '%s.msk' % self.monitor_name.replace(' ','_')
        wildcard = "pySolo mask file (*.msk)|*.msk"

        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile=filename, wildcard=wildcard, style=wx.SAVE
            )

        #dlg.SetFilterIndex(2)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.fsPanel.mon.saveROIS(path)
            self.currentMaskTXT.SetValue(os.path.split(path)[1])

        dlg.Destroy()
        return path

    def onSaveApply(self, event):
        """
        Save ROIs to file and apply to current monitor
        """
        path = self.onSaveMask(None)
        mn = self.monitor_name.replace(' ','')
        options.SetValue(mn, 'maskfile', path)
        options.Save()

    def onLoadMask(self, event):
        """
        Load Mask from file
        """

        wildcard = "pySolo mask file (*.msk)|*.msk"

        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.fsPanel.mon.loadROIS(path)
            self.currentMaskTXT.SetValue(os.path.split(path)[1])

        dlg.Destroy()

    def onRefresh(self):
        if self.monitor_number != options.GetOption("Monitors"):
            self.monitor_number = options.GetOption("Monitors")
            self.sbSizer_1.Hide(0)
            self.sbSizer_1.Remove(0)
            self.MonitorList = ['Monitor %s' % (int(m) + 1) for m in range(self.monitor_number)]
            self.thumbnailNumber = wx.ComboBox(self, -1, size=(-1,-1) , choices=self.MonitorList, style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
            self.sbSizer_1.Insert (1, self.thumbnailNumber, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
            self.sbSizer_1.Layout()
