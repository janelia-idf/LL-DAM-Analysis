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
- turn this on/off by replacing 'debugprt(' with '# debugprt(' or vice versa.
"""
from inspect import currentframe        
from db import debugprt                 
pgm = 'pvg_panel_one.py'

# %%                                                            imports
import wx, os
import wx.lib.newevent
ThumbnailClickedEvt, EVT_THUMBNAIL_CLICKED = wx.lib.newevent.NewCommandEvent()
from wx.lib.filebrowsebutton import FileBrowseButton, DirBrowseButton

from pvg_common import previewPanel, options, myConfig

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Thumbnail Panel
class thumbnailPanel(previewPanel):
    """
    A small preview Panel to be used as thumbnail
    """
    def __init__( self, parent, monitor_number, ThumbnailSize=(320,240) ):           
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug

        previewPanel.__init__(self, parent, size=ThumbnailSize, keymode=False)

        self.number = int(monitor_number)
        self.allowEditing = False

        self.displayNumber()

        self.Bind(wx.EVT_LEFT_UP, self.onLeftClick)
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                Show Monitor Numbers            
    def displayNumber(self):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
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
        text1 = wx.StaticText( self, wx.ID_ANY, '%s' % (self.number+1), pos)
        text1.SetFont(font1)
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        Left Click
    def onLeftClick(self, evt):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Event handler for thumbnail being clicked on
        Send signal around that the thumbnail was clicked
        """
        event = ThumbnailClickedEvt(self.GetId())

        event.id = self.GetId()
        event.number = self.number
        event.thumbnail = self

        self.GetEventHandler().ProcessEvent(event)
        debugprt(self,currentframe(),pgm,'end   ')

        
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Panel Grid View        
class panelGridView(wx.ScrolledWindow):
    """
    The scrollable grid of monitor thumbnails on panel one                      # number in monitors not always there
    """
    def __init__(self, parent, gridSize, ThumbnailSize=(320,240) ): 
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        
        print('$$$$$$ pvg_panel_one:  panelGridView:  line 102:  gridSize = ',gridSize)

# %%                                                  Set up scrolling window
        wx.ScrolledWindow.__init__(self, parent, wx.ID_ANY, size=(-1,600))
        self.SetScrollbars(1, 1, 1, 1)
        self.SetScrollRate(10, 10)

        self.parent = parent
        self.ThumbnailSize = ThumbnailSize
        self.grid_mainSizer = wx.GridSizer(6,3,2,2)

# %%                                              Populate the thumbnail grid
        self.previewPanels = []
        for i in range(0, int(gridSize)):
            self.previewPanels.append ( thumbnailPanel(self, monitor_number=i,
                ThumbnailSize=self.ThumbnailSize) )
            self.grid_mainSizer.Add(self.previewPanels[i])

# %%                                              Make elements visible in UI
        self.SetSizer(self.grid_mainSizer)
        # Set up listener for clicking on thumbnails
        self.Bind(EVT_THUMBNAIL_CLICKED, self.onThumbnailClicked)
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                    Thumbnail Clicked
    def onThumbnailClicked(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Event handler that makes clicking a thumbnail update the dropdown menu
        Relay event to sibling panel
        """
        wx.PostEvent(self.parent.lowerPanel, event)
        event.Skip()
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        Update Monitors
    # Should be working
    def updateMonitors(self, old, now):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Changes number of monitor thumbnails.
        """     
        diff = old - now    
        i = diff
        while i != 0:                   # Adding monitors to grid
            if diff < 0:
                i += 1
                # Make a new thumbnail and add to list
                self.previewPanels.append ( thumbnailPanel(self, monitor_number=old,
                        ThumbnailSize = self.ThumbnailSize) )
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

        debugprt(self,currentframe(),pgm,'end   ')
        
# %%                                                    Change Thumbnail size
    def updateThumbs(self, old, new):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        self.ThumbnailSize = new
        # print('$$$$$$ pvg_panel_one:  panelGridView:  line 173:  gridSize = ',gridSize)

        
#        for i in range(0, self.gridSizer):                                                  # not working
#            self.previewPanels[i].SetThumbnailSize(new)
#            self.grid_mainSizer.Layout()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Panel Configuration
class panelConfigure(wx.Panel):    
    """
    The lower half of panel one with the configuration settings                 # this panel could be shorter to cover less of the monitors
    """
    def __init__(self, parent):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(-1,300),
            style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)
        self.parent = parent

        self.thumbnail = None
        self.mask_file = None
        self.source = None
        self.sourceType = None
        self.track = None
        self.trackType = None

        lowerSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Static box1 (LEFT)
        sb_1 = wx.StaticBox(self, -1, "Select Monitor")#, size=(250,-1))
        self.sbSizer_1 = wx.StaticBoxSizer (sb_1, wx.VERTICAL)

        n_monitors = options.GetOption("Monitors")
        self.MonitorList = ['Monitor %s' % (int(m) + 1) for m in range( n_monitors )]
        self.thumbnailNumber = wx.ComboBox(self, -1, size=(-1,-1) , choices=self.MonitorList, style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind ( wx.EVT_COMBOBOX, self.onChangingMonitor, self.thumbnailNumber)

        self.currentSource = wx.TextCtrl (self, -1, "No Source Selected", style=wx.TE_READONLY)

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

        self.n_cams = options.GetOption("Webcams")
        self.WebcamsList = [ 'Webcam %s' % (int(w) +1) for w in range( self.n_cams ) ]
        rb1 = wx.RadioButton(self, -1, 'Camera', style=wx.RB_GROUP)
        source1 = wx.ComboBox(self, -1, size=(285,-1) , choices = self.WebcamsList, style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind(wx.EVT_COMBOBOX, self.sourceCallback, source1)

        rb2 = wx.RadioButton(self, -1, 'File' )
        source2 = FileBrowseButton(self, -1, labelText='', size=(300,-1), changeCallback = self.sourceCallback)

        rb3 = wx.RadioButton(self, -1, 'Folder' )
        source3 = DirBrowseButton (self, style=wx.DD_DIR_MUST_EXIST, labelText='', size=(300,-1), changeCallback = self.sourceCallback)


        self.controls = []
        self.controls.append((rb1, source1))
        self.controls.append((rb2, source2))
        self.controls.append((rb3, source3))

        for radio, source in self.controls:
            self.grid2.Add( radio , 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2 )
            self.grid2.Add( source , 0, wx.ALIGN_CENTRE|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2 )
            self.Bind(wx.EVT_RADIOBUTTON, self.onChangeSource, radio )
            source.Enable(False)

        self.controls[0][1].Enable(True)

        # grid2.Add(wx.StaticText(self, -1, ""))

        self.sbSizer_2.Add( self.grid2 )
        lowerSizer.Add(self.sbSizer_2, 0, wx.EXPAND|wx.ALL, 5)

        # Static box3 (RIGHT)
        sb_3 = wx.StaticBox(self, -1, "Set Tracking Parameters")
        sbSizer_3 = wx.StaticBoxSizer (sb_3, wx.VERTICAL)

        sbSizer_31 = wx.BoxSizer (wx.HORIZONTAL)

        self.activateTracking = wx.CheckBox(self, -1, "Activate Tracking")
        self.activateTracking.SetValue(False)
        self.activateTracking.Bind ( wx.EVT_CHECKBOX, self.onActivateTracking)

        self.isSDMonitor = wx.CheckBox(self, -1, "Sleep Deprivation Monitor")
        self.isSDMonitor.SetValue(False)
        self.isSDMonitor.Bind ( wx.EVT_CHECKBOX, self.onSDMonitor)
        self.isSDMonitor.Enable(False)

        sbSizer_31.Add (self.activateTracking, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        sbSizer_31.Add (self.isSDMonitor, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        self.pickMaskBrowser = FileBrowseButton(self, -1, labelText='Mask File')

        # sbSizer_3.Add ( self.activateTracking , 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        sbSizer_3.Add ( sbSizer_31 , 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        sbSizer_3.Add ( self.pickMaskBrowser , 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )

        # trackingTypeSizer = wx.Sizer(wx.HORIZONTAL)
        self.trackDistanceRadio = wx.RadioButton(self, -1, "Activity as distance traveled", style=wx.RB_GROUP)
        self.trackVirtualBM = wx.RadioButton(self, -1, "Activity as midline crossings count")
        self.trackPosition = wx.RadioButton(self, -1, "Only position of flies")
        sbSizer_3.Add (wx.StaticText ( self, -1, "Calculate fly activity as..."), 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        sbSizer_3.Add (self.trackDistanceRadio, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
        sbSizer_3.Add (self.trackVirtualBM, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
        sbSizer_3.Add (self.trackPosition, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 2 )

        lowerSizer.Add(sbSizer_3, -1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(lowerSizer)
        self.Bind(EVT_THUMBNAIL_CLICKED, self.onThumbnailClicked)
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                     Input source
    def __getSource(self):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        check which source is ticked and what is the associated value
        Returns the selected source type and its value
        """

        for (r, s), st in zip(self.controls,range(3)):
            if r.GetValue():
                source = s.GetValue()
                sourceType = st
        debugprt(self,currentframe(),pgm,'end   ')

        return source, sourceType

# %%                                                Input tracking type
    def __getTrackingType(self):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        return which type of tracking we are chosing
        ['DISTANCE','VBS','XY_COORDS']
        """
        if self.trackDistanceRadio.GetValue(): trackType = 0  #  "DISTANCE"
        elif self.trackVirtualBM.GetValue(): trackType = 1    #  "VBS"
        elif self.trackPosition.GetValue(): trackType = 2     #  "XY_COORDS"

        debugprt(self,currentframe(),pgm,'end   ')
        return trackType                                                        # this isn't getting written to config file correctly

# %%                                                            play button
    def onPlay (self, event=None):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        # Event handler for the play button
        """
        
        if self.thumbnail:
            self.thumbnail.Play()
            self.btnStop.Enable(True)
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                            Stop Button
    def onStop (self, event=None):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Event handler for the stop button
        """
        if self.thumbnail and self.thumbnail.isPlaying:
            self.thumbnail.Stop()
            self.btnStop.Enable(False)
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                    Click Thumbnail
    def onThumbnailClicked(self, evt):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Picking thumbnail by clicking on it
        Event handler for changing monitor via clicking on thumbnail
        """
        self.monitor_number = evt.number #+ 1
        self.thumbnail = evt.thumbnail
        self.thumbnailNumber.SetValue(self.MonitorList[self.monitor_number]) # -1
        self.updateThumbnail()
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                    Monitor dropdown box
    def onChangingMonitor(self, evt):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Picking thumbnail by using the dropbox
        Event handler for changing monitor via dropdown box
        """
        sel = evt.GetString()
        self.monitor_number = self.MonitorList.index(sel) #+ 1
        self.thumbnail = self.parent.scrollThumbnails.previewPanels[self.monitor_number]         #this is not very elegant
        self.updateThumbnail()
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                            Refresh thumbnail and controls
    def updateThumbnail(self):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Refreshing thumbnail data
        """
        # If monitor exists, get info. Else, set to null/default values.
        if options.HasMonitor(self.monitor_number):
            sourceType, source, track, mask_file, trackType, isSDMonitor = options.GetMonitor(self.monitor_number)
        else:
            sourceType, source, track, mask_file, trackType, isSDMonitor = [0, '', False, '', 1, False]

        # If monitor is playing a camera
        if sourceType == 0 and source != '':
            source = self.WebcamsList[source]

        # Ensure source and type match throughout program
        self.source = self.thumbnail.source = source
        self.sourceType = self.thumbnail.sourceType = sourceType
        self.thumbnail.track = track
        if self.thumbnail.hasMonitor():
                self.thumbnail.mon.isSDMonitor = isSDMonitor

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
        self.isSDMonitor.SetValue(isSDMonitor)
        self.pickMaskBrowser.SetValue(mask_file or '')
        [self.trackDistanceRadio, self.trackVirtualBM, self.trackPosition][trackType].SetValue(True)
        debugprt(self,currentframe(),pgm,'end   ')

# %% 
    def sourceCallback (self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        self.applyButton.Enable(True)
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        Radio buttons
    def onChangeSource(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        # Determine which radio button was selected
        radio_selected = event.GetEventObject()

        # Enable the selected source, disable all others
        for radio, source in self.controls:
            if radio is radio_selected:
                source.Enable(True)
            else:
                source.Enable(False)

        self.applyButton.Enable(True)
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                    Apply Button
    def onApplySource(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
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
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                Save Monitor Config
    def saveMonitorConfiguration(self):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        options.SetMonitor(self.monitor_number,
                           self.thumbnail.sourceType,
                           self.thumbnail.source, #self.thumbnail.source+1 in dev code
                           self.thumbnail.track,
                           self.mask_file,
                           self.trackType,                                      # this is not being saved correctly
                           self.thumbnail.mon.isSDMonitor
                           )
        options.Save()
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        Activate Tracking        
    def onActivateTracking(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        if self.thumbnail:
            self.thumbnail.track = event.IsChecked()
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                        
    def onSDMonitor(self, event):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        if self.thumbnail:
            self.thumbnail.mon.isSDMonitor = event.IsChecked()
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                Update monitor dropdown box
    def updateMonitors(self, old, now):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
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
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                Update webcam dropdown box
    def updateWebcams(self, old, now):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """
        Updates the dropdown box of cameras on lower half of panel one
        """
        # Generate the list of webcams
        self.WebcamsList = [ 'Webcam %s' % (int(w) +1) for w in range(new) ]

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
        debugprt(self,currentframe(),pgm,'end   ')

        
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Panel One
class panelOne(wx.Panel):
    """
    Panel number One:  All the thumbnails
    """
    def __init__(self, parent):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        wx.Panel.__init__(self, parent)

        # Retrieve settings
        self.monitor_number = options.GetOption("Monitors")
        self.tn_size = options.GetOption("ThumbnailSize")
        self.n_cams = options.GetOption("Webcams")

        self.temp_source  = ''
        self.source = ''
        self.sourceType = -1

        # Create a grid of thumbnails and a configure panel

        print('$$$$$$ pvg_panel_one:  panelOne:  line 603:  gridSize = ',self.monitor_number)

        self.scrollThumbnails = panelGridView(self, gridSize=self.monitor_number, ThumbnailSize=self.tn_size)
        self.lowerPanel = panelConfigure(self)
        # Display elements
        self.PanelOneSizer = wx.BoxSizer(wx.VERTICAL)
        self.PanelOneSizer.Add(self.scrollThumbnails, 1, wx.EXPAND, 0)
        self.PanelOneSizer.Add(self.lowerPanel, 0, wx.EXPAND, 0)
        self.SetSizer(self.PanelOneSizer)
        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                         Stop Playing
    def StopPlaying(self):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        self.lowerPanel.onStop()

        debugprt(self,currentframe(),pgm,'end   ')

# %%                                                            Refresh   
    def onRefresh(self):
        debugprt(self,currentframe(),pgm,'begin     ')                                          # debug
        """ 
        Checks for changes to be made to UI and implements them.
        """
        # Check number of monitors
        if self.monitor_number != options.GetOption("Monitors"):
            self.scrollThumbnails.updateMonitors(self.monitor_number, options.GetOption("Monitors"))
            self.lowerPanel.updateMonitors(self.monitor_number, options.GetOption("Monitors"))
            self.monitor_number = options.GetOption("Monitors")

        # Check thumbnail size
        if self.tn_size != options.GetOption("ThumbnailSize"):
            self.scrollThumbnails.updateThumbs(self.tn_size, options.GetOption("ThumbnailSize"))
            self.tn_size = options.GetOption("ThumbnailSize")

        # Check number of webcams
        if self.n_cams != options.GetOption("Webcams"):
            self.lowerPanel.updateWebcams(self.n_cams, options.GetOption("Webcams"))
            self.n_cams = options.GetOption("Webcams")

        # Show changes to UI
        self.PanelOneSizer.Layout()
