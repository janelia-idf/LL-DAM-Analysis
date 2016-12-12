# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 22:23:09 2016

@author: Lori
"""
import wx
import os
from ConfigParser import SafeConfigParser as scp
from pvy_panel_two import panelLiveView             ##  use PySolo functions to display masks & thumbnail

class mainFrame(wx.Frame):
    """
    Creates the main window of the application.
    """

    def __init__(self, *args, **kwds):

        wx.Panel.__init__(self, parent, wx.ID_ANY)              # prepare a panel for the window
        # ------------------------------------------------------------------------------------------------------------
        # Static box1: Video File Input

        self.videotxt = wx.StaticBox(self, -1, "Video File")  # , size=(250,-1))    # title
        self.sizer_filename = wx.StaticBoxSizer(in_file, wx.HORIZONTAL)                # text input box
        self.btnBrowser = FileBrowseButton(self, -1, labelText='Browse')            # browse button

        self.sizer_video.Add(self.videotxt, 0, wx.ALIGN_LEFT,5)                     # row sizer
        self.sizer_video.Add(self.sizer_filename, 0, wx.ALIGN_CENTER, 5)
        self.sizer_video.Add(self.btnBrowser, 0, wx.ALIGN_RIGTH, 5)

        Sizer_Whole.Add ( self.video_sizer , 0, wx.ALIGN_LEFT, 5 )                  # add to whole sizer

        # # ------------------------------------------------------------------------------------------------------------
        #
        # # Sizer_3.Add ( self.activateTracking , 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        # sbSizer_3.Add ( sbSizer_31 , 0, wx.ALIGN_LEFT, 5 )
        # sbSizer_3.Add ( self.pickMaskBrowser , 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
        # self.Bind(wx.EVT_BUTTON, self.onSaveMask, self.btnSave)
        #
        # # Static box2: mask parameters
        # sb_2 = wx.StaticBox(self, -1, "Mask Editing")  # , size=(250,-1))
        # sbSizer_2 = wx.StaticBoxSizer(sb_2, wx.VERTICAL)
        # fgSizer_1 = wx.FlexGridSizer(0, 2, 0, 0)
        #
        # self.btnClear = wx.Button(self, wx.ID_ANY, label="Clear All")
        # self.Bind(wx.EVT_BUTTON, self.fsPanel.ClearAll, self.btnClear)
        #
        # self.btnClearLast = wx.Button(self, wx.ID_ANY, label="Clear selected")
        # self.Bind(wx.EVT_BUTTON, self.fsPanel.ClearLast, self.btnClearLast)
        #
        # self.btnAutoFill = wx.Button(self, wx.ID_ANY, label="Auto Fill")
        # self.Bind(wx.EVT_BUTTON, self.fsPanel.AutoMask, self.btnAutoFill)
        #
        # fgSizer_1.Add(self.btnClear)
        # fgSizer_1.Add(self.btnClearLast)
        # fgSizer_1.Add(self.btnAutoFill)
        #
        # sbSizer_2.Add(fgSizer_1)
        #
        # # Static box3: mask I/O
        # sb_3 = wx.StaticBox(self, -1, "Mask File")  # , size=(250,-1))
        # sbSizer_3 = wx.StaticBoxSizer(sb_3, wx.VERTICAL)
        #
        # self.currentMaskTXT = wx.TextCtrl(self, -1, "No Mask Loaded", style=wx.TE_READONLY)
        #
        # btnSizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        # self.btnLoad = wx.Button(self, wx.ID_ANY, label="Load Mask")
        # self.Bind(wx.EVT_BUTTON, self.onLoadMask, self.btnLoad)
        # self.btnSave = wx.Button(self, wx.ID_ANY, label="Save Mask")
        # self.Bind(wx.EVT_BUTTON, self.onSaveMask, self.btnSave)
        # self.btnSaveApply = wx.Button(self, wx.ID_ANY, label="Save and Apply")
        # self.Bind(wx.EVT_BUTTON, self.onSaveApply, self.btnSaveApply)
        #
        # btnSizer_1.Add(self.btnLoad)
        # btnSizer_1.Add(self.btnSave)
        # btnSizer_1.Add(self.btnSaveApply)
        #
        # sbSizer_3.Add(self.currentMaskTXT, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 5)
        # sbSizer_3.Add(btnSizer_1, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        #
        # ##
        #
        # # Buttons:  Apply, Clear, Save
        # btnSizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        # self.btnApply = wx.Button( self, wx.ID_ANY, label="Apply")
        # self.Bind(wx.EVT_BUTTON, self.onLoadMask, self.btnApply)
        # self.btnClear = wx.Button( self, wx.ID_ANY, label="Load Mask")
        # self.Bind(wx.EVT_BUTTON, self.onLoadMask, self.btnLoad)
        # self.btnSave = wx.Button( self, wx.ID_ANY, label="Save Mask")
        # self.Bind(wx.EVT_BUTTON, self.onSaveMask, self.btnSave)
        #
        # btnSizer_1.Add(self.btnLoad)
        # btnSizer_1.Add(self.btnSave)
        # btnSizer_1.Add(self.btnSaveApply)
        #
        # sbSizer_3.Add ( self.currentMaskTXT, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )
        # sbSizer_3.Add (btnSizer_1, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        #
        # for title, text in instr:
        #     t = wx.StaticText(self, -1, title);
        #     t.SetFont(titleFont)
        #     sbSizer_4.Add(t, 0, wx.ALL, 2)
        #     sbSizer_4.Add(wx.StaticText(self, -1, text), 0, wx.ALL, 2)
        #     sbSizer_4.Add((wx.StaticLine(self)), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        #
        # sizer_4.Add(self.sbSizer_1, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 5)
        # sizer_4.Add(sbSizer_2, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 5)
        # sizer_4.Add(sbSizer_3, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 5)
        # sizer_4.Add(sbSizer_4, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 5)
        #
        # sizer_3.Add(self.fsPanel, 0, wx.LEFT | wx.TOP, 20)
        # sizer_3.Add(sizer_4, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        #
        # sizer_1.Add(sizer_3, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        # sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        self.SetSizer(sizer_1)
        print wx.Window.FindFocus()

        self.Bind(wx.EVT_CHAR, self.fsPanel.onKeyPressed)




    # %%%%%%%%%%%%%%%%%%%% Write Mask
    def writemsk(config_file, rows, columns, out_file):


        parser = SafeConfigParser()                             # open config file that contains ROI coordinate information
        parser.read(config_file)

        ## read configuration information. Values are in pixels.
        x1 = parser.get('X', 'x1')                      # starting x-position
        x_len = parser.get('X', 'x_len')                # length of ROI in x-direction
        x_sep = parser.get('X', 'x_sep')                # space between ROIs in x-direction
        x_tilt = parser.get('X', 'x_tilt')              # difference in starting x-position for next row.

        y1 = parser.get('Y', 'y1')
        y_len = parser.get('Y', 'y_len')
        y_sep = parser.get('Y', 'y_sep')
        y_tilt = parser.get('Y', 'y_tilt')

        ## open the output file.
        fh = open(out_file, 'w')

        ROI = 1

        for row in range(0, rows):  # y-coordinates change through rows
            ax = x1 + row * x_tilt  # x for upper left corner of ROI; reset x-coordinate at start of row
            bx = ax + x_len         # x for upper right corner of ROI
            cx = bx                 # x for lower right corner of ROI
            dx = ax                 # x for lower left corner of ROI

            if row == 0:            # y for first row starts at y1
                ay = y1
            else:
                ay = y1 + row * (y_len + y_sep)  # y upper left corner of next row
            by = ay                 # y for upper right corner of ROI
            cy = ay + y_len         # y for lower right corner of ROI
            dy = cy                 # y for lower left corner of ROI


            for col in range(0, columns):       # write each pair of coordinates into the mask file for this ROI
                if (col == 0 and row == 0):     # first ROI has different format from remaining ROIs
                    fh.write('(lp1\n((I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\n' % (ax, ay, bx, by, cx, cy, dx, dy))
                    print('(lp1\n((I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\n' % (ax, ay, bx, by, cx, cy, dx, dy))
                else:
                    fh.write('ttp%d\na((I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\n' % (ROI, ax, ay, bx, by, cx, cy, dx, dy))
                    print('ttp%d\na((I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\n' % (ROI, ax, ay, bx, by, cx, cy, dx, dy))

                ax = bx + x_sep             # increment the (x,y) pairs for the next ROI
                bx = ax + x_len
                cx = bx
                dx = ax
                ay = ay + y_tilt
                by = ay
                cy = ay + y_len
                dy = cy
                ROI = ROI + 1


        fh.write('ttp%d\na.(lp1\nI1\n' % (ROI+1))       # write end of file information
        fh.write('aI1\n'*(rows*columns-1))
        fh.write('a.\n\n\n')                            # PySolo can't read it without the extra line feed characters at the end

        fh.close()


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Main

out_file = 'C:\\Users\\laughreyl\\Documents\\GitHub\\LL-DAM-Analysis\\Data\\Working_files\\automask.msk'
rows = 8                    #  Chrimson/+ section
columns = 6

if __name__ == "__main__":

    app = wx.App()
    wx.InitAllImageHandlers()

    frame_1 = mainFrame(None, -1, "")           # Create the main window.
    app.SetTopWindow(frame_1)                   # Makes this window the main window
    frame_1.Show()                              # Shows the main window
    app.MainLoop()                              # Begin user interactions.
