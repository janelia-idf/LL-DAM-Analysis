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

"""
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Imports
"""
import wx, os
import pvg_common

"""
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Settings
"""

pgm = 'pvg_acquire.py'

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



class panelLiveView(wx.Panel):
    """
    Panel Number 2
    Live view of selected camera
    """
    def __init__(self, parent, cfg):
        """
        Shows fullsize video and a mask making panel
        """

        wx.Panel.__init__(self, parent, -1)

        self.cfg = cfg
        self.config_obj = self.cfg.config_obj
        self.configDict = self.cfg.configDict
        self.full_filename = self.cfg.full_filename

        self.n_mons = self.configDict['Options, monitors']
        self.fs_size = self.configDict['Options, fullsize']
        self.monitor_name = 'Monitor1'

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)

        #Static box1: monitor input
        sb_1 = wx.StaticBox(self, wx.ID_ANY, "Select Monitor")
        self.sbSizer_1 = wx.StaticBoxSizer (sb_1, wx.VERTICAL)
        if self.n_mons >0:
            self.MonitorList = ['Monitor %s' % (int(m)) for m in range(1, self.n_mons)]
        else: self.MonitorList = 'Monitor1'
        self.thumbnailNumber = wx.ComboBox(self, wx.ID_ANY, choices=self.MonitorList, style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind(wx.EVT_COMBOBOX, self.onChangeMonitor, self.thumbnailNumber)

        self.sourceTXTBOX =  wx.TextCtrl (self, wx.ID_ANY, "No monitor selected", style=wx.TE_READONLY)

        self.sbSizer_1.Add ( self.thumbnailNumber, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        self.sbSizer_1.Add ( self.sourceTXTBOX, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )

        #Static box2: mask parameters
        sb_2 = wx.StaticBox(self, wx.ID_ANY, "Mask Editing")
        sbSizer_2 = wx.StaticBoxSizer (sb_2, wx.VERTICAL)
        fgSizer_1 = wx.FlexGridSizer( 0, 2, 0, 0 )

        self.btnClear = wx.Button( self, wx.ID_ANY, label="Clear All")
        self.Bind(wx.EVT_BUTTON, self.onClearAll, self.btnClear)

        self.btnClearLast = wx.Button( self, wx.ID_ANY, label="Clear selected")
        self.Bind(wx.EVT_BUTTON, self.onClearLast, self.btnClearLast)


        self.btnAutoFill = wx.Button( self, wx.ID_ANY, label="Auto Fill")
        self.Bind(wx.EVT_BUTTON, self.onAutoMask, self.btnAutoFill)

        fgSizer_1.Add (self.btnClear)
        fgSizer_1.Add (self.btnClearLast)
        fgSizer_1.Add (self.btnAutoFill)

        sbSizer_2.Add (fgSizer_1)


        #Static box3: mask I/O
        sb_3 = wx.StaticBox(self, wx.ID_ANY, "Mask File")
        sbSizer_3 = wx.StaticBoxSizer (sb_3, wx.VERTICAL)

        self.currentMaskTXT = wx.TextCtrl (self, wx.ID_ANY, "No Mask Loaded", style=wx.TE_READONLY)

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
        sb_4 = wx.StaticBox(self, wx.ID_ANY, "Help")
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
            t = wx.StaticText(self, wx.ID_ANY, title); t.SetFont(titleFont)
            sbSizer_4.Add( t, 0, wx.ALL, 2 )
            sbSizer_4.Add(wx.StaticText(self, wx.ID_ANY, text) , 0 , wx.ALL, 2 )
            sbSizer_4.Add ( (wx.StaticLine(self)), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

        sizer_4.Add(self.sbSizer_1, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
        sizer_4.Add(sbSizer_2, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
        sizer_4.Add(sbSizer_3, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
        sizer_4.Add(sbSizer_4, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )


        sizer_3.Add(sizer_4, 0, wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        sizer_1.Add(sizer_3, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )


        self.SetSizer(sizer_1)

        self.Bind( wx.EVT_CHAR, self.onKeyPressed )

    def onClearAll(self):
        print('Clear All clicked')  # TODO: write this function

    def onClearLast(self):
        print('Clear Last clicked')  # TODO: write this function

    def onAutoMask(self):
        print('Auto Mask clicked')  # TODO: write this function

    def onKeyPressed(self):
        print('Key Pressed')  # TODO: write this function

    def StopPlaying(self):
        """
        """
        if self.fsPanel and self.fsPanel.isPlaying: self.fsPanel.Stop()


    def onChangeMonitor(self, event):


        if self.fsPanel.isPlaying: self.fsPanel.Stop()

        self.monitor_name = event.GetString()
        self.monitor_number = self.MonitorList.index( self.monitor_name )

        n_cams = configDict['Options, webcams']
        WebcamsList = [ 'Webcam %s' % (int(w) +1) for w in range( n_cams ) ]

        if options.HasMonitor(self.monitor_number):
            sourceType, source, start_datetime, track, mask_file, trackType, isSDMonitor = options.GetMonitor(self.monitor_number)      # $$$$$$ add start_datetime?
            self.fsPanel.setMonitor( source )
            self.fsPanel.Play()

            print("$$$$$$ pvg_panel_two; 181; onChangeMonitor; mask_file = ", mask_file)
            if mask_file:
                self.fsPanel.mon.loadROIS(mask_file)
                self.currentMaskTXT.SetValue(os.path.split(mask_file)[1] or '')

            if sourceType == 0:
                self.sourceTXTBOX.SetValue( WebcamsList[source] )
            else:
                self.sourceTXTBOX.SetValue( os.path.split(source)[1] )

        else:
            sourceType, source, start_datetime, track, mask_file, trackType = [0, '', datetime.datetime.now(), False, '', 1]
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
        options.SetValue(mn, 'mask_file', path)
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

    def onRefresh(self, configDict):
        if self.monitor_number != configDict['Options, Monitors']:
            self.monitor_number = configDict['Options, Monitors']
            self.sbSizer_1.Hide(0)
            self.sbSizer_1.Remove(0)
            self.MonitorList = ['Monitor %s' % (int(m) + 1) for m in range(self.monitor_number)]
            self.thumbnailNumber = wx.ComboBox(self, wx.ID_ANY, choices=self.MonitorList, style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
            self.sbSizer_1.Insert (1, self.thumbnailNumber, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
            self.sbSizer_1.Layout()
