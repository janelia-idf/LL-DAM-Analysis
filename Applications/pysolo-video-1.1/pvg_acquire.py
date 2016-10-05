#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       pvg_acquire.py
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

__author__ = "Giorgio Gilestro <giorgio@gilest.ro>"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/08/16 21:57:19 $"
__copyright__ = "Copyright (c) 2011 Giorgio Gilestro"
__license__ = "Python"

import inspect                                                                       

import os, optparse, sys

from pvg_common import pvg_config, acquireThread, DEFAULT_CONFIG

import wx
from wx.lib.filebrowsebutton import FileBrowseButton
import wx.grid as gridlib

# Not present in dev version
class customDataTable(gridlib.PyGridTableBase):
    def __init__(self, colLabels, dataTypes, useValueCleaner=True):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        gridlib.PyGridTableBase.__init__(self)
        self.useValueCleaner = useValueCleaner
        self.colLabels = colLabels
        self.dataTypes = dataTypes
        self.data = [['']*len(self.dataTypes)]

    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface

    def GetNumberRows(self):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        # print('inspect not working in customdatatable getnumberrows')               # debug
        try:
            return len(self.data)
        except:
            return 0

    def GetNumberCols(self):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        # print('inspect not working in customdatatable getnumbercols')
        return len (self.colLabels)

    def IsEmptyCell(self, row, col):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        # print('inspect not working in customdatatable isemptycell')
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    def Reset(self, colLabels, dataTypes):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Re-initialise the table
        reset(colLabels, dataTypes)
        """
        n_col = self.GetNumberCols()-len(colLabels)
        if n_col > 0:
            self.GetView().ProcessTableMessage(
                        gridlib.GridTableMessage(self,
                        gridlib.GRIDTABLE_NOTIFY_COLS_DELETED,
                        1, n_col ))

            self.colLabels = colLabels
            self.dataTypes = dataTypes

        self.ClearTable()


    def ClearTable(self):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Clear the table
        """
        self.GetView().ProcessTableMessage(
                gridlib.GridTableMessage(self,
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,
                0, self.GetNumberRows() ))
        self.data = []


    def GetValue(self, row, col):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        # print('inspect not working in customdatatable getvalue')                        # debug
        """
        (row, col)
        Get value at given coordinates
        """
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def InsertColumn(self, col_pos, col_type=gridlib.GRID_VALUE_FLOAT+':6,2', col_label=''):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Add one grid column before col_pos, with type set to col_type and label col_label
        """
    def transpose(whole_table):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        return map(lambda *row: list(row), *whole_table)

        empty_col = [''] * self.GetNumberCols()

        if self.GetNumberRows() > 0:
            t_data = transpose(self.data)
            t_data.insert(col_pos, empty_col)
            self.data = transpose(t_data)

        self.dataTypes.insert(col_pos, col_type)
        self.colLabels.insert(col_pos, col_label)


        self.GetView().ProcessTableMessage(
                gridlib.GridTableMessage(self,
                gridlib.GRIDTABLE_NOTIFY_COLS_INSERTED,
                col_pos, 1         ))

    def Sort(self, bycols, descending=False):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        sort the table by multiple columns
            bycols:  a list (or tuple) specifying the column numbers to sort by
                   e.g. (1,0) would sort by column 1, then by column 0
            descending: specify sorting order
        """

        import operator

        table = self.data

        for col in reversed(bycols):
            table = sorted(table, key=operator.itemgetter(col))

        if descending:
           table.reverse()

        self.data = table

        msg=wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        self.GetView().ProcessTableMessage(msg)


    def AddRow (self, rows):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Add one or more rows at the bottom of the table / sheet
        row can be an array of values or a 2-dimenstional array of rows and values
        """

        rows = self.cleanFromMask(rows)

        if type(rows[0]) == list:
            n_rows = len (rows)
            for row in rows: self.data.append(row)
        else:
            self.data.append(rows)
            n_rows = 1

        self.GetView().ProcessTableMessage(
                gridlib.GridTableMessage(self,
                gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED,
                n_rows         ))


    def RemRow (self, rows):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Remove one or more rows
        """

        [self.data.pop(int(x)-1) for x in rows]

        self.GetView().ProcessTableMessage(
                gridlib.GridTableMessage(self,
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,
                len(rows)         ))


    def SetData(self, data=None):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Set the whole content of the table to data
        """
        data = self.cleanFromMask(data)
        self.ClearTable()
        self.data = data
        n_rows = self.GetNumberRows()
        self.GetView().ProcessTableMessage(
                gridlib.GridTableMessage(self,
                gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED,
                n_rows ))

        self.GetView().ProcessTableMessage(
                gridlib.GridTableMessage(None,
                gridlib.GRIDTABLE_REQUEST_VIEW_GET_VALUES))

    def SetRow (self, row, data):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        data = self.cleanFromMask(data)
        try:
            self.data[row] = data
        except:
            self.AddRow(data)

    def SetValue(self, row, col, value):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        # print('inspect not working in setvalue')                                             # debug        
        """
        (row, col, value)
        Set Value for cell at given coordinates
        """
        try:
            self.data[row][col] = value
        except IndexError:
            # add a new row
            self.data.append([''] * self.GetNumberCols())
            self.SetValue(row, col, value)

            # tell the grid we've added a row
            self.GetView().ProcessTableMessage(
                    gridlib.GridTableMessage(self,
                    gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED,
                    1                    ) )
    #--------------------------------------------------
    # Some optional methods

    def GetColLabelValue(self, col):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        # print('inspect not working in getcollabelvalue')
        """
        Called when the grid needs to display labels
        """
        return self.colLabels[col]



    def GetTypeName(self, row, col):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        # print('inspect not working in customdatatable gettypename')                         # debug
        """
        Called to determine the kind of editor/renderer to use by
        default, doesn't necessarily have to be the same type used
        natively by the editor/renderer if they know how to convert.
        """
        return self.dataTypes[col]


    def CanGetValueAs(self, row, col, typeName):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        # print('inspect not working in cangetvalueas')                           # debug
        """
        Called to determine how the data can be fetched and stored by the
        editor and renderer.  This allows you to enforce some type-safety
        in the grid.
        """
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        # print('inspect not working in cansetvalueas')                                             # debug
        return self.CanGetValueAs(row, col, typeName)

    def cleanFromMask(self, l):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Goes through the list l and make sure it doesn't contain
        any masked value
        """
        if self.useValueCleaner:
            try:
                if type(l[0]) == list:

                    for r in range(len(l)):
                        l[r] = self.cleanFromMask(l[r])
                else:

                    for c in range (len(l)):
                        if np.ma.getmask(l[c]): l[c] = '--'
                        if type(l[c]) != str and l[c] >= 999999: l[c] = '--'
            except:
                pass

        return l


class CustTableGrid(gridlib.Grid):
    """
    This class describes a CustomGrid. Data are handled thorough a table but
    functions for the table are proxied from here
    """
    def __init__(self, parent, colLabels, dataTypes, enableEdit = False, useValueCleaner=True, useMenu=True):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug

        gridlib.Grid.__init__(self, parent, -1)
        self.table = customDataTable(colLabels, dataTypes, useValueCleaner)
        self.SetTable(self.table, True)
        self.EnableEditing(enableEdit)
        self.SetColMinimalAcceptableWidth(0)
        self.SetRowMinimalAcceptableHeight(0)
        self.checkableItems = self.table.dataTypes.count('bool') > 0

        self.sortedColumn=1
        self.sortedColumnDescending=False
        self.CtrlDown = False

        # we draw the column headers
        # code based on original implementation by Paul Mcnett
        #wx.EVT_PAINT(self.GetGridColLabelWindow(), self.OnColumnHeaderPaint)

        self.SetRowLabelSize(30)
        self.SetMargins(0,0)
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnSort)
        #self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnLeftClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        #self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnLeftDClick)

        if useMenu: self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnContextMenu)

    def OnColumnHeaderPaint(self, evt):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        w = self.GetGridColLabelWindow()
        dc = wx.PaintDC(w)
        clientRect = w.GetClientRect()
        font = dc.GetFont()

        # For each column, draw it's rectangle, it's column name,
        # and it's sort indicator, if appropriate:
        #totColSize = 0
        totColSize = -self.GetViewStart()[0]*self.GetScrollPixelsPerUnit()[0] # Thanks Roger Binns
        for col in range(self.GetNumberCols()):
            dc.SetBrush(wx.Brush("WHEAT", wx.TRANSPARENT))
            dc.SetTextForeground(wx.BLACK)
            colSize = self.GetColSize(col)
            rect = (totColSize,0,colSize,32)
            dc.DrawRectangle(rect[0] - (col<>0 and 1 or 0), rect[1],
                             rect[2] + (col<>0 and 1 or 0), rect[3])
            totColSize += colSize

            if col == self.sortedColumn:
                font.SetWeight(wx.BOLD)
                # draw a triangle, pointed up or down, at the
                # top left of the column.
                left = rect[0] + 3
                top = rect[1] + 3

                dc.SetBrush(wx.Brush("WHEAT", wx.SOLID))
                if self.sortedColumnDescending:
                    dc.DrawPolygon([(left,top), (left+6,top), (left+3,top+4)])
                else:
                    dc.DrawPolygon([(left+3,top), (left+6, top+4), (left, top+4)])
            else:
                font.SetWeight(wx.NORMAL)

            dc.SetFont(font)
            dc.DrawLabel("%s" % self.GetTable().colLabels[col],
                     rect, wx.ALIGN_CENTER | wx.ALIGN_TOP)

    def Clear(self, *args, **kwargs):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Clear the table empty
        """
        self.table.ClearTable(*args, **kwargs)
        self.AutoSizeColumns()


    def Reset(self, *args, **kwargs):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Reinitialize the table
        """

        self.table.Reset(*args, **kwargs)
        self.AutoSizeColumns()

    def InsertCol (self, *args, **kwargs):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        (self, col_pos, col_type=gridlib.GRID_VALUE_FLOAT+':6,2', col_label='')
        Add one grid column before col_pos, with type set to col_type and label col_label
        """

        self.table.InsertColumn (*args, **kwargs)
        self.AutoSizeColumns()


    def SetColsSize(self, cols_size):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        for col in range(len(cols_size)):
            self.SetColSize(col, cols_size[col])

    def GetData (self):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Return a bidimensional array with a copy
        of the data in the spreadsheet
        """
        all_data = self.table.data
        for row in range(len(all_data)):
            for col in range (len(all_data[row])):
                try:
                    all_data[row][col] = all_data[row][col].strip()
                except:
                    pass

        return all_data

    def SetData(self, *kargs, **kwargs):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        (data)
        Set the data of the table to the given value
        data is a bidimensional array
        """
        self.table.SetData(*kargs, **kwargs)
        self.AutoSizeColumns()

    def GoToEnd(self):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Go to the end of the table
        """
        while self.MovePageDown():
            pass

    def AddRow(self, *kargs, **kwargs):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Add one or more rows at the bottom of the table / sheet
        row can be an array of values or a 2-dimenstional array of rows and values
        """

        self.table.AddRow(*kargs, **kwargs)
        self.AutoSizeColumns()
        #row = self.GetNumberRows()
        #self.GoToEnd()

    def RemRow(self, *kargs, **kwargs):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Add one or more rows at the bottom of the table / sheet
        row can be an array of values or a 2-dimenstional array of rows and values
        """

        self.table.RemRow(*kargs, **kwargs)
        self.AutoSizeColumns()
        row = self.GetNumberRows()

    def GetNumberRows(self, *kargs, **kwargs):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Return the number of Rows
        """
        return self.table.GetNumberRows ()

    def GetNumberCols(self, *kargs, **kwargs):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Return the number of cols
        """
        return self.table.GetNumberCols ()

    def HideCol(self, col):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        (col)
        Hide the specified column by setting its size to 0
        """
        self.SetColSize(col, 0)

    def OnKeyUp(self, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Records whether the Ctrl Key is up or down
        """
        if event.GetKeyCode() == 308:
            self.CtrlDown = False
        event.Skip()

    def OnKeyDown(self, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Responds to the following keys:
        Enter -> Jumps to next cell
        Ctrl-C -> Copy selected cells
        """

        if event.GetKeyCode() == 308:
            self.CtrlDown = True
            event.Skip()

        if self.CtrlDown and event.GetKeyCode() == 67:
            self.OnCopySelected(event)
            event.Skip()

        if event.GetKeyCode() != wx.WXK_RETURN:
            event.Skip()
            return

        if event.ControlDown():   # the edit control needs this key
            event.Skip()
            return

        self.DisableCellEditControl()

        while 1 == 1:
            success = self.MoveCursorRight(event.ShiftDown())
            size_of_current_col = self.GetColSize(self.GetGridCursorCol())
            if size_of_current_col != 0 or not success: break

        if not success:
            newRow = self.GetGridCursorRow() + 1

            if newRow < self.GetTable().GetNumberRows():
                self.SetGridCursor(newRow, 0)
                self.MakeCellVisible(newRow, 0)
            else:
                #Add a new row here?
                pass

    def OnLeftClick(self, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        On mouse click checks if the cell contain a checkbox and if it does
        will change its status
        """
        self.ForceRefresh()

    def OnSort(self, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Clicking on the label of the columns sorts data in one order, a second click reverses the order.
        """
        col = event.GetCol()
        if col >= 0:
            if col==self.sortedColumn:
                self.sortedColumnDescending=not self.sortedColumnDescending
            else:
                self.sortedColumn=col
                self.sortedColumnDescending=False

            sorting_order = range(self.GetNumberCols())
            sorting_order.pop(col)
            sorting_order = [col] + sorting_order

            self.table.Sort( sorting_order, self.sortedColumnDescending)
            self.Refresh()


    def OnContextMenu(self, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Creates and handles a popup menu
        """
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnCopyAll, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnCopyRow, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnCopyCol, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnCopySelected, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnExportToFile, id=self.popupID5)


        # make a menu
        menu = wx.Menu()
        menu.Append(self.popupID1, "Copy All")
        menu.Append(self.popupID2, "Copy Current Row")
        menu.Append(self.popupID3, "Copy Current Column")
        menu.Append(self.popupID4, "Copy Selected")
        menu.Append(self.popupID5, "Export All to file")

        #Add this voice only if the table has checkable items
        if self.checkableItems:
            self.popupID6 = wx.NewId()
            self.popupID7 = wx.NewId()
            self.Bind(wx.EVT_MENU, partial(self.OnCheckUncheckItems, True ), id=self.popupID6)
            self.Bind(wx.EVT_MENU, partial(self.OnCheckUncheckItems, False ), id=self.popupID7)
            menu.AppendSeparator()
            menu.Append(self.popupID6, "Check Selected")
            menu.Append(self.popupID7, "Uncheck Selected")
            #menu.Append(self.popupID8, "Remove Selected")


        self.PopupMenu(menu)
        menu.Destroy()

    def OnCopyCol(self, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Copy to clipboard the content of the entire currently
        selected column, including the column label
        """
        self.SelectCol(self.GetGridCursorCol())
        content = wx.TextDataObject()
        content.SetText(self.DataToCSV('\t', onlySel = True))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(content)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")

    def OnCopyRow(self, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Copy to clipboard the content of the entire currently
        selected row
        """
        self.SelectRow(self.GetGridCursorRow())
        content = wx.TextDataObject()
        content.SetText(self.DataToCSV('\t', onlySel = True))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(content)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")

    # I do this because I don't like the default behaviour of not starting the
    # cell editor on double clicks, but only a second click.
    def OnLeftDClick(self, evt):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        if self.CanEnableCellControl():
            self.EnableCellEditControl()

    def OnCopyAll(self, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Copy the all table to clipboard
        """
        content = wx.TextDataObject()
        content.SetText(self.DataToCSV('\t'))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(content)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")

    def OnCopySelected(self, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Copy selected cells to system clipboard
        """
        content = wx.TextDataObject()
        content.SetText(self.DataToCSV('\t', onlySel = True))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(content)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")

    def OnExportToFile(self, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Save away the content of the grid as CSV file
        """
        wildcard = 'CSV files (*.csv)|*.csv|All files (*.*)|*.*'
        dlg = wx.FileDialog(self, 'Choose a file', '', '', wildcard, wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            filename=dlg.GetFilename()
            dirname=dlg.GetDirectory()
            filehandle=open(os.path.join(dirname, filename),'w')
            filehandle.write(self.DataToCSV(','))
            filehandle.close()
        dlg.Destroy()

    def DataToCSV(self, separator=',', onlySel = False):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Convert the data in the grid to CSV value format (or equivalent)
        """
        csv = ''
        r, c = 0, 0

        all_content = [self.table.colLabels] + self.table.data

        for row in all_content:
            c = 0
            notEmptyLine = ''
            for cell in row:
                if not(onlySel) or self.IsInSelection(r-1, c):
                    csv += str(cell)+separator
                    notEmptyLine = '\n'
                c+=1
            csv += notEmptyLine
            r +=1
        return csv

    def OnCheckUncheckItems(self, check_value, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        Check uncheck all checkable items in the selected rows
        """
        c = self.table.dataTypes.index('bool')
        r = 0

        for row in self.table.data:
            if self.IsInSelection(r,c):
                self.table.SetValue(r,c, check_value)
            r += 1
        self.ForceRefresh()

class pvg_AcquirePanel(wx.Panel):
    def __init__(self, parent):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug

        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.parent = parent

        os.chdir('c:\\Users\\laughreyl\\Documents\\DAM_Analysis\\Data\\Output\\')                    # debug
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.FBconfig = FileBrowseButton(self, -1, labelText='Pick file', size=(300,-1), changeCallback = self.configCallback)

        colLabels = ['Monitor', 'Source', 'Mask', 'Output', 'Track type', 'Track']

        dataTypes = [gridlib.GRID_VALUE_NUMBER,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_BOOL,
                          ]

        self.grid = CustTableGrid(self, colLabels, dataTypes, enableEdit=True, useMenu=False)
        self.grid.Clear()

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.startBtn = wx.Button(self, wx.ID_ANY, 'Start')
        self.stopBtn = wx.Button(self, wx.ID_ANY, 'Stop')
        self.stopBtn.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.onStop, self.stopBtn)
        self.Bind(wx.EVT_BUTTON, self.onStart, self.startBtn)
        btnSizer.Add (self.startBtn, 0, wx.ALL, 5)
        btnSizer.Add (self.stopBtn, 0, wx.ALL, 5)


        mainSizer.Add(self.FBconfig, 0, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(self.grid, 1, wx.EXPAND, 0)
        mainSizer.Add(btnSizer, 0, wx.ALL, 5)
        self.SetSizer(mainSizer)

    def configCallback(self, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        self.loadFile( self.FBconfig.GetValue() )


    def loadFile(self, filename):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        self.options = pvg_config(filename)
        self.updateTable()
        self.parent.sb.SetStatusText('Loaded file %s' % filename)

        return True

    def updateTable(self):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        monitorsData = self.options.getMonitorsData()

        self.grid.Clear()
        self.monitors = {}

        for mn in monitorsData:

            m = monitorsData[mn]

            try:
                s = os.path.split( m['source'] )[1]
            except:
                s = 'Camera %02d' % ( m['source'] + 1 )

            mf = os.path.split(m['mask_file'])[1]
            df = 'Monitor%02d.txt' % (mn+1)
            row = [mn+1, s, mf, df, m['track_type'], m['track'] ]
            self.grid.AddRow(row)


        for mn in monitorsData:    # collects specs for monitors from config
            m = monitorsData[mn]
            self.monitors[mn] = ( acquireThread(mn, m['source'], 
                                                m['resolution'], 
                                                m['mask_file'], 
                                                m['track'], 
                                                m['track_type'], 
                                                m['dataFolder']) )
#            print(mn, self.monitors[mn], m)                                                 # debug
            
    def isToTrack(self, monitor):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        d = self.grid.GetData()
        for row in d:
            if monitor == row[0]: return row[-1]

    def onStart(self, event=None):
#        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        # print('inspect not working in onstart')                                             # debug
        """
        """
        self.acquiring = True
        self.stopBtn.Enable(self.acquiring)
        self.startBtn.Enable(not self.acquiring)
        c = 0

        for mon in self.monitors:
            if self.isToTrack(mon):
                self.monitors[mon].doTrack()
                c+=1

        self.parent.sb.SetStatusText('Tracking %s Monitors' % c)

    def onStop(self, event):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        self.acquiring = False
        self.stopBtn.Enable(self.acquiring)
        self.startBtn.Enable(not self.acquiring)
        for mon in self.monitors:
            self.monitors[mon].halt()

        self.parent.sb.SetStatusText('All tracking is now stopped')

class acquireFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        # print('inspect not working in acquireframe __init__')                           # debug
        kwargs["size"] = (800, 600)

        wx.Frame.__init__(self, *args, **kwargs)

        self.sb = wx.StatusBar(self, wx.ID_ANY)
        self.SetStatusBar(self.sb)

        self.acq_panel =  pvg_AcquirePanel(self)

    def loadConfig(self, filename=None):
        """
        """
#        print inspect.currentframe().f_back.f_locals['self']                                    # debug
        # print('inspect not working in acquireframe loadConfig '+filename)                   # debug
        if ~os.path.isfile(filename):
            
#        if filename is None:
#            print(os.environ['HOME'])
#            pDir = os.environ['HOME']
#            filename = os.path.join (pDir, DEFAULT_CONFIG)
            filename = DEFAULT_CONFIG

        self.acq_panel.loadFile(filename)

        return True

    def Start(self):
        # print inspect.currentframe().f_back.f_locals['self']                                    # debug
        """
        """
        self.acq_panel.onStart()



if __name__ == '__main__':
    sys.stdout = open('d:\\DAM_Analysis\\stdout.txt', 'w')                                                  # DEBUG
    
    
    parser = optparse.OptionParser(usage='%prog [options] [argument]', version='%prog version 1.0')
    parser.add_option('-c', '--config', dest='config_file', metavar="CONFIG_FILE", help="The full path to the config file to open")
    parser.add_option('--acquire', action="store_true", default=False, dest='acquire', help="Start acquisition when the program starts")
    parser.add_option('--nogui', action="store_false", default=True, dest='showgui', help="Do not show the graphical interface")

    (options, args) = parser.parse_args()
    print('main')
    app=wx.PySimpleApp(0)
    frame_acq = acquireFrame(None, -1, "")           # Create the main window.
    app.SetTopWindow(frame_acq)
    frame_acq.Show(options.showgui)

#    configfile = options.config_file or DEFAULT_CONFIG
    configfile = 'c:\Users\laughreyl\Documents\DAM_Analysis\Data\Output\myconfig_w_msks.msk'
    print(configfile)    
    cfgloaded = frame_acq.loadConfig(configfile)

    if cfgloaded and options.acquire:
        frame_acq.Start()

    app.MainLoop()
