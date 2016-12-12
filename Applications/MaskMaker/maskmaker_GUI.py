# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 22:23:09 2016

@author: Lori
"""
import wx
import os
from wx.lib.filebrowsebutton import FileBrowseButton, DirBrowseButton
from ConfigParser import SafeConfigParser as scp

class mainFrame(wx.Frame):
    """
    Creates the main window of the application.
    """

    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((600, 400))
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.do_layout()

    def do_layout(self):
        self.sizer_Whole = wx.FlexGridSizer(3,1,5,5)  # contains whole display

        #------------------------------------------------------------------------------------------------------------
        # Section 1: Video File Input

        self.sizer_filename = wx.BoxSizer(wx.HORIZONTAL)                            # text input box
        self.btnBrowser = FileBrowseButton(self, -1, labelText='Video File')            # browse button

        self.sizer_filename.Add(self.btnBrowser)

        self.sizer_Whole.Add ( self.btnBrowser , 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND)               # add to whole sizer

        # ------------------------------------------------------------------------------------------------------------
        # Section 2: Coordinates Input Title

        self.title = wx.StaticText(self, -1, "Measurements: (See figure below)")         # title

        self.sizer_Whole.Add(self.title, 0, wx.ALIGN_LEFT)  # add to whole sizer


        # ------------------------------------------------------------------------------------------------------------
        # Section 3:  Coordinates Input Grid

        self.sizer_table = wx.FlexGridSizer(5,1,1,1)
        self.sizer_coord_size = wx.FlexGridSizer(5,5,1,1)                                # rows & columns

        self.description = wx.StaticText(self, -1, "Number of columns and rows of ROIs:")
        self.columns_txt = wx.StaticText(self, -1, "    columns = ")
        self.columns = wx.TextCtrl(self, -1, "")
        self.rows_txt = wx.StaticText(self, -1, "    rows = ")
        self.rows = wx.TextCtrl(self, -1, "")

        self.sizer_coord_size.Add(self.description)
        self.sizer_coord_size.Add(self.columns_txt)
        self.sizer_coord_size.Add(self.columns)
        self.sizer_coord_size.Add(self.rows_txt)
        self.sizer_coord_size.Add(self.rows)

        self.sizer_table.Add(self.sizer_coord_size, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND)                  # add to whole sizer

        self.sizer_coord_origin = wx.FlexGridSizer(5,5,1,1)                                # coordinates (x1,y1)

        self.description = wx.StaticText(self, -1, "Coordinates of top left corner of top left ROI: ")
        self.columns_txt = wx.StaticText(self, -1, "    X = ")
        self.columns = wx.TextCtrl(self, -1, "")
        self.rows_txt = wx.StaticText(self, -1, "    Y = ")
        self.rows = wx.TextCtrl(self, -1, "")

        self.sizer_coord_origin.Add(self.description)
        self.sizer_coord_origin.Add(self.columns_txt)
        self.sizer_coord_origin.Add(self.columns)
        self.sizer_coord_origin.Add(self.rows_txt)
        self.sizer_coord_origin.Add(self.rows)

        self.sizer_table.Add(self.sizer_coord_origin, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND)                  # add to whole sizer

        self.sizer_coord_lengths = wx.FlexGridSizer(5,5,1,1)                                # lengths of sides

        self.description = wx.StaticText(self, -1, "Lengths of ROI sides: ")
        self.columns_txt = wx.StaticText(self, -1, "    X = ")
        self.columns = wx.TextCtrl(self, -1, "")
        self.rows_txt = wx.StaticText(self, -1, "    Y = ")
        self.rows = wx.TextCtrl(self, -1, "")

        self.sizer_coord_lengths.Add(self.description)
        self.sizer_coord_lengths.Add(self.columns_txt)
        self.sizer_coord_lengths.Add(self.columns)
        self.sizer_coord_lengths.Add(self.rows_txt)
        self.sizer_coord_lengths.Add(self.rows)

        self.sizer_table.Add(self.sizer_coord_lengths, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND)                  # add to whole sizer

        self.sizer_coord_tilt = wx.FlexGridSizer(5,5,1,1)                                # tilt

        self.description = wx.StaticText(self, -1, "Tilt: ")
        self.columns_txt = wx.StaticText(self, -1, "    X = ")
        self.columns = wx.TextCtrl(self, -1, "")
        self.rows_txt = wx.StaticText(self, -1, "    Y = ")
        self.rows = wx.TextCtrl(self, -1, "")

        self.sizer_coord_tilt.Add(self.description)
        self.sizer_coord_tilt.Add(self.columns_txt)
        self.sizer_coord_tilt.Add(self.columns)
        self.sizer_coord_tilt.Add(self.rows_txt)
        self.sizer_coord_tilt.Add(self.rows)

        self.sizer_table.Add(self.sizer_coord_tilt, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND)

        self.sizer_Whole.Add(self.sizer_table, 0, wx.EXPAND)# add to whole sizer

        self.SetSizer(self.sizer_Whole)
        print wx.Window.FindFocus()

        """




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

"""
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Main

out_file = 'C:\\Users\\laughreyl\\Documents\\GitHub\\LL-DAM-Analysis\\Data\\Working_files\\automask.msk'
rows = 8                    #  Chrimson/+ section
columns = 6

if __name__ == "__main__":

    app = wx.App(0)

    frame_1 = mainFrame(None, -1, "")           # Create the main window.
    app.SetTopWindow(frame_1)                   # Makes this window the main window
    frame_1.Show()                              # Shows the main window
    app.MainLoop()                              # Begin user interactions.


